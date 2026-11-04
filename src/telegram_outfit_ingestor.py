"""
GüzelAI Holding A.Ş. — Telegram (@guzelaibot) Çok-Kullanıcılı Özel Kombin Yakalayıcı,
Otomatik Segment Algılayıcı (Kadın / Erkek / Kız Çocuk / Erkek Çocuk) &
%100 Fotogerçekçi Gerçek AI İnsan Model (Sıfır Animasyon/3D) Üretim Motoru
------------------------------------------------------------------------------------
Kullanıcı Direktifleri:
1) "telegramdan verdiğim kombinleri mutlaka yap kadın erkek çocuk olduğunu algıla gerçek ai modellere yap"
2) "botu kulllanan başka kullanıcılarda bir kombin attığında onu mankenle hazırla"
"""
import base64
import hashlib
import json
import os
import re
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from PIL import Image

from autonomous_creation_factory import (
    BASE_DIR,
    PROCEDURAL_ATELIER_MATRIX,
    cloud_fetch_ai_image,
    load_dynamic_creations_catalog,
    remove_white_studio_background,
    save_dynamic_creations_catalog,
)
from fashion_agenda_engine import (
    build_photorealistic_human_model_prompt,
    detect_telegram_outfit_segment,
)

TG_QUEUE_PATH = BASE_DIR / "output" / "telegram_pending_outfits_queue.json"
TG_OVERRIDE_PATH = BASE_DIR / "output" / "telegram_trigger_override.json"
SUBSCRIBERS_FILE = BASE_DIR / "assets" / "telegram_subscribers.json"
DEFAULT_BOT_TOKEN = "8783821353:AAG9m_SIUO4jAxx_fN2pyD1xbtTaTozuB5U"


def _get_bot_token() -> str:
    return os.environ.get("TELEGRAM_BOT_TOKEN", DEFAULT_BOT_TOKEN).strip()


def _tg_call(method: str, payload: Optional[dict] = None) -> dict:
    tok = _get_bot_token()
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/{method}",
            json=payload or {},
            timeout=25,
        )
        return r.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _download_tg_photo(file_id: str, dest: Path) -> bool:
    tok = _get_bot_token()
    try:
        info = _tg_call("getFile", {"file_id": file_id})
        if not info.get("ok"):
            return False
        fp = info["result"]["file_path"]
        r = requests.get(f"https://api.telegram.org/file/bot{tok}/{fp}", timeout=45)
        if r.status_code == 200 and len(r.content) > 1000:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            return True
    except Exception:
        pass
    return False


def load_tg_queue() -> List[Dict[str, Any]]:
    os.makedirs(TG_QUEUE_PATH.parent, exist_ok=True)
    local_q: List[Dict[str, Any]] = []
    if TG_QUEUE_PATH.exists():
        try:
            data = json.loads(TG_QUEUE_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                local_q = data
        except Exception:
            pass

    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if gh_token:
        try:
            r = requests.get(
                "https://api.github.com/repos/thezencirs/instagram-kombin-bot/contents/output/telegram_pending_outfits_queue.json",
                headers={"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"},
                timeout=12,
            )
            if r.status_code == 200:
                content_b64 = r.json().get("content", "")
                remote_q = json.loads(base64.b64decode(content_b64).decode("utf-8"))
                if isinstance(remote_q, list):
                    existing_ids = {item.get("request_id") for item in local_q}
                    for rq in remote_q:
                        if rq.get("request_id") and rq.get("request_id") not in existing_ids:
                            local_q.append(rq)
        except Exception:
            pass

    return local_q


def save_tg_queue(queue: List[Dict[str, Any]], sync_github: bool = True) -> None:
    os.makedirs(TG_QUEUE_PATH.parent, exist_ok=True)
    raw_json = json.dumps(queue, ensure_ascii=False, indent=2)
    TG_QUEUE_PATH.write_text(raw_json, encoding="utf-8")

    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if sync_github and gh_token:
        try:
            api_url = "https://api.github.com/repos/thezencirs/instagram-kombin-bot/contents/output/telegram_pending_outfits_queue.json"
            headers = {"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"}
            get_r = requests.get(api_url, headers=headers, timeout=12)
            payload: Dict[str, Any] = {
                "message": "chore(telegram-queue): sync multi-user pending telegram outfit queue [skip ci]",
                "content": base64.b64encode(raw_json.encode("utf-8")).decode("ascii"),
            }
            if get_r.status_code == 200 and get_r.json().get("sha"):
                payload["sha"] = get_r.json()["sha"]
            requests.put(api_url, headers=headers, json=payload, timeout=15)
        except Exception:
            pass


def trigger_cloud_workflow_if_needed() -> bool:
    """Kuyrukta bekleyen kullanıcı kombinleri varsa GitHub Actions iş akışını anında tetikler."""
    gh_token = os.environ.get("GH_TOKEN", "").strip()
    if not gh_token:
        return False
    try:
        r = requests.post(
            "https://api.github.com/repos/thezencirs/instagram-kombin-bot/actions/workflows/daily_reels.yml/dispatches",
            headers={"Authorization": f"Bearer {gh_token}", "Accept": "application/vnd.github+json"},
            json={"ref": "main", "inputs": {"bypass_cooldown": "1", "slot_name": "otomatik"}},
            timeout=15,
        )
        return r.status_code in (200, 201, 204)
    except Exception:
        return False


def poll_and_enqueue_telegram_outfits(acknowledge_users: bool = True) -> List[Dict[str, Any]]:
    """
    Telegram (@guzelaibot) getUpdates kuyruğunu kontrol eder;
    YÖNETİCİ VEYA BOTU KULLANAN HERHANGİ BİR KULLANICI tarafından gönderilen
    tüm ürün linklerini, kombin fotoğraflarını veya kombin açıklamalarını
    KAYIPSIZ olarak `output/telegram_pending_outfits_queue.json` içine kaydeder.
    """
    sub_data = {"chats": {}, "last_update_id": 0}
    if SUBSCRIBERS_FILE.exists():
        try:
            sub_data = json.loads(SUBSCRIBERS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    offset = int(sub_data.get("last_update_id", 0)) + 1
    res = _tg_call("getUpdates", {"offset": offset, "timeout": 1})
    queue = load_tg_queue()
    existing_ids = {q.get("request_id") for q in queue}

    # Eski override dosyası varsa kuyruğa aktar
    if TG_OVERRIDE_PATH.exists():
        try:
            ov = json.loads(TG_OVERRIDE_PATH.read_text(encoding="utf-8"))
            req_id = f"tg_override_{int(time.time())}"
            if req_id not in existing_ids and (ov.get("custom_urls") or ov.get("custom_image") or ov.get("custom_title")):
                seg = detect_telegram_outfit_segment(ov.get("custom_title", ""), ov.get("custom_urls", []))
                queue.append({
                    "request_id": req_id,
                    "requester_chat_id": str(ov.get("requester_chat_id") or "995164733"),
                    "requester_name": str(ov.get("requester_name") or "telegram_user"),
                    "urls": ov.get("custom_urls") or [],
                    "image_path": ov.get("custom_image") or "",
                    "text": ov.get("custom_title") or "",
                    "detected_segment": seg,
                    "created_at": datetime.utcnow().isoformat() + "Z",
                })
                existing_ids.add(req_id)
            TG_OVERRIDE_PATH.unlink(missing_ok=True)
        except Exception:
            pass

    if res.get("ok"):
        updates = res.get("result", [])
        changed_sub = False
        for upd in updates:
            uid = int(upd.get("update_id", 0))
            if uid > int(sub_data.get("last_update_id", 0)):
                sub_data["last_update_id"] = uid
                changed_sub = True

            if "callback_query" in upd:
                cb = upd["callback_query"]
                cb_id = cb.get("id")
                cb_data = cb.get("data", "")
                cb_chat = (cb.get("message") or {}).get("chat") or {}
                cb_cid = str(cb_chat.get("id", ""))
                if cb_id:
                    _tg_call("answerCallbackQuery", {"callback_query_id": cb_id, "text": "✨ Yeni kombin üretimi kuyruğa alındı!"})
                if cb_cid and cb_data == "trigger_new_broadcast":
                    req_id = f"tg_cb_{uid}"
                    if req_id not in existing_ids:
                        queue.append({
                            "request_id": req_id,
                            "update_id": uid,
                            "requester_chat_id": cb_cid,
                            "requester_name": cb_chat.get("username") or cb_chat.get("first_name") or cb_cid,
                            "urls": [],
                            "image_path": "",
                            "text": "",
                            "detected_segment": "kadin",
                            "created_at": datetime.utcnow().isoformat() + "Z",
                        })
                        existing_ids.add(req_id)
                continue

            msg = upd.get("message") or upd.get("channel_post")
            if not isinstance(msg, dict):
                continue
            chat = msg.get("chat") or {}
            cid = str(chat.get("id", ""))
            if not cid:
                continue

            user_title = chat.get("title") or chat.get("username") or chat.get("first_name") or cid
            sub_data.setdefault("chats", {})[cid] = {
                "id": chat.get("id"),
                "type": chat.get("type", "private"),
                "title": user_title,
                "username": chat.get("username", ""),
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            changed_sub = True

            text = (msg.get("text") or "").strip()
            caption = (msg.get("caption") or "").strip()
            combined = text or caption
            urls = re.findall(r"https?://[^\s<>\"']+", combined)
            clean_txt = re.sub(r"https?://[^\s<>\"']+", "", combined)
            for cmd_w in ("/yayinla", "/uret", "/paylas", "/tetikle", "/kombin"):
                clean_txt = clean_txt.replace(cmd_w, "")
            clean_txt = clean_txt.strip()

            img_rel_path = ""
            if msg.get("photo"):
                best_p = msg["photo"][-1]
                dest_p = BASE_DIR / "assets" / f"tg_input_{uid}.jpg"
                if _download_tg_photo(best_p["file_id"], dest_p):
                    img_rel_path = f"assets/tg_input_{uid}.jpg"

            is_pure_info_cmd = text.lower().split("@")[0] in ("/start", "/durum", "/linkler") and not urls and not img_rel_path
            if is_pure_info_cmd:
                continue

            if urls or img_rel_path or clean_txt or text.lower().startswith(("/yayinla", "/uret", "/paylas", "/tetikle")):
                req_id = f"tg_upd_{uid}"
                if req_id not in existing_ids:
                    seg = detect_telegram_outfit_segment(clean_txt, urls)
                    seg_label_tr = {
                        "kadin": "Kadın",
                        "erkek": "Erkek",
                        "kiz_cocuk": "Kız Çocuk",
                        "erkek_cocuk": "Erkek Çocuk",
                    }.get(seg, "Kadın")
                    queue.append({
                        "request_id": req_id,
                        "update_id": uid,
                        "requester_chat_id": cid,
                        "requester_name": user_title,
                        "urls": urls,
                        "image_path": img_rel_path,
                        "text": clean_txt,
                        "detected_segment": seg,
                        "created_at": datetime.utcnow().isoformat() + "Z",
                    })
                    existing_ids.add(req_id)
                    print(
                        f"📥 [ÇOK-KULLANICILI TELEGRAM KOMBİN YAKALAYICI] Kullanıcı={user_title} ({cid}) | "
                        f"İstek={req_id} | Segment={seg_label_tr} | Link={len(urls)} | Görsel={bool(img_rel_path)}"
                    )
                    if acknowledge_users:
                        _tg_call(
                            "sendMessage",
                            {
                                "chat_id": cid,
                                "text": (
                                    f"✨ Kombin talebiniz alındı! ({seg_label_tr} kategorisi algılandı)\n"
                                    f"👗 %100 Gerçekçi AI İnsan Model ve 1:1 ürün dekupeleriyle 2K Reels videonuz hazırlanıyor..."
                                ),
                            },
                        )

        if changed_sub:
            SUBSCRIBERS_FILE.parent.mkdir(parents=True, exist_ok=True)
            SUBSCRIBERS_FILE.write_text(json.dumps(sub_data, ensure_ascii=False, indent=2), encoding="utf-8")

    save_tg_queue(queue, sync_github=bool(queue))
    return queue


def _translate_tr_item_to_en_prompt(name_tr: str, color_tr: str, slot_key: str) -> str:
    """Türkçe ürün adını FLUX.1 modeli için net İngilizce görsel kıyafet tanımına çevirir."""
    low = (f"{color_tr} {name_tr}").lower()
    color_map = [
        ("zümrüt", "emerald green"),
        ("bordo", "deep oxblood burgundy"),
        ("mürdüm", "deep plum mulberry"),
        ("konyak", "rich cognac tan"),
        ("taba", "warm cognac tan"),
        ("camel", "warm camel"),
        ("kamel", "warm camel"),
        ("antrasit", "charcoal anthracite grey"),
        ("füme", "dark smoke grey"),
        ("gri", "heather grey"),
        ("siyah", "jet black"),
        ("lacivert", "midnight navy blue"),
        ("ekru", "warm ecru cream"),
        ("fildişi", "ivory cream"),
        ("krem", "soft cream"),
        ("beyaz", "crisp white"),
        ("kahve", "dark espresso brown"),
        ("çikolata", "dark chocolate brown"),
        ("vizon", "warm mink taupe"),
        ("bej", "warm stone beige"),
        ("haki", "dark olive khaki"),
        ("kırmızı", "ruby red"),
        ("pembe", "soft pastel pink"),
        ("lavanta", "pastel lavender"),
        ("hardal", "mustard ochre"),
        ("kiremit", "terracotta rust"),
    ]
    en_color = "luxury winter neutral"
    for tr_c, en_c in color_map:
        if tr_c in low:
            en_color = en_c
            break

    type_map = {
        "outerwear": "tailored double-breasted wool winter coat",
        "cap": "luxury designer sunglasses",
        "top": "fine ribbed-knit turtleneck cashmere sweater",
        "bottom": "tailored high-waisted pleated wide-leg wool trousers",
        "bag": "structured luxury leather handbag",
        "shoes": "clean leather low-top court sneakers",
    }
    if "mont" in low or "puffer" in low or "şişme" in low:
        type_map["outerwear"] = "quilted winter puffer jacket"
    elif "süet" in low or "shearling" in low or "kürklü" in low:
        type_map["outerwear"] = "suede shearling collar winter jacket"
    elif "deri" in low and slot_key == "outerwear":
        type_map["outerwear"] = "tailored leather winter trench jacket"
    if "bere" in low:
        type_map["cap"] = "ribbed-knit winter beanie hat"
    if "jean" in low or "kot" in low:
        type_map["bottom"] = "straight-leg winter denim jeans"
    elif "chino" in low or "kargo" in low:
        type_map["bottom"] = "tailored winter cotton chino trousers"
    if "bot" in low or "çizme" in low:
        type_map["shoes"] = "luxury leather winter ankle boots"
    elif "loafer" in low:
        type_map["shoes"] = "polished leather winter loafers"

    return f"{en_color} {type_map.get(slot_key, 'luxury fashion piece')}"


def build_telegram_custom_archetype_if_pending(scrape_fn) -> Optional[Dict[str, Any]]:
    """
    Eğer Telegram kuyruğunda yönetici veya başka bir kullanıcıdan bekleyen kombin isteği varsa:
    1) Kuyruktan alır, ürün linklerini kazır (`scrape_fn`) ve/veya yüklenen fotoğrafı analiz eder.
    2) Kombinin Kadın ('kadin'), Erkek ('erkek'), Kız Çocuk ('kiz_cocuk') veya Erkek Çocuk ('erkek_cocuk')
       olduğunu otomatik algılar.
    3) Eksik kalan parçaları aynı segmentin lüks şablonuyla tamamlar.
    4) 6 parçanın 1:1 şeffaf PNG dekupe görsellerini üretir.
    5) %100 FOTOGERÇEKÇİ GERÇEK İNSAN AI MODEL (%0 animasyon/3D!) üzerinde 3 yürüyüş karesi sentezler.
    """
    queue = poll_and_enqueue_telegram_outfits()
    if not queue:
        return None

    req = queue.pop(0)
    save_tg_queue(queue, sync_github=True)

    req_id = str(req.get("request_id") or f"tg_{int(time.time())}")
    requester_cid = str(req.get("requester_chat_id") or "995164733")
    requester_name = str(req.get("requester_name") or "telegram_user")
    urls = req.get("urls") or []
    user_text = str(req.get("text") or "").strip()
    user_img_path = str(req.get("image_path") or "").strip()

    scraped_by_slot: Dict[str, Dict[str, Any]] = {}
    slot_cycle = ["outerwear", "top", "bottom", "bag", "shoes", "cap"]
    for idx, u in enumerate(urls):
        try:
            s_key, s_item = scrape_fn(u, fallback_slot=slot_cycle[idx % len(slot_cycle)])
            if s_key in scraped_by_slot:
                for alt_k in slot_cycle:
                    if alt_k not in scraped_by_slot:
                        s_key = alt_k
                        break
            scraped_by_slot[s_key] = s_item
        except Exception as e:
            print(f"  [Telegram Link Kazıma Uyarısı] {u}: {e}")

    seg = detect_telegram_outfit_segment(user_text, urls, scraped_by_slot)
    print(
        f"🎯 [ÇOK-KULLANICILI TELEGRAM KOMBİN MOTORU] Kullanıcı={requester_name} ({requester_cid}) | "
        f"İstek={req_id} | Algılanan Segment={seg.upper()} | Kazınan Ürün={len(scraped_by_slot)} | "
        f"%100 Gerçekçi AI İnsan Model Sentezleniyor..."
    )

    seg_templates = PROCEDURAL_ATELIER_MATRIX.get(seg) or PROCEDURAL_ATELIER_MATRIX["kadin"]
    bp = seg_templates[0]

    arch_hash = hashlib.md5(f"{req_id}_{time.time()}".encode("utf-8")).hexdigest()[:6]
    archetype_id = f"tg_custom_{seg}_{arch_hash}"
    base_seed = int(arch_hash, 16)

    slot_map_bp = {
        "outerwear": ("01_outer", bp["outer"], "https://www.trendyol.com/kaban-x-c55"),
        "cap": ("02_cap", bp["cap"], "https://www.trendyol.com/gunes-gozlugu-x-c105"),
        "top": ("03_top", bp["top"], "https://www.trendyol.com/kazak-x-c1092"),
        "bottom": ("04_bottom", bp["bottom"], "https://www.trendyol.com/pantolon-x-c70"),
        "bag": ("05_bag", bp["bag"], "https://www.bagmori.com"),
        "shoes": ("06_shoes", bp["shoes"], "https://www.trendyol.com/spor-ayakkabi-x-c109"),
    }

    assets_dir = BASE_DIR / "assets"
    items_dir = assets_dir / "items"
    assets_dir.mkdir(parents=True, exist_ok=True)
    items_dir.mkdir(parents=True, exist_ok=True)

    # Eğer kullanıcı 6'lı bir flat-lay kombin fotoğrafı yüklediyse 6 bölgeyi dekupe et
    uploaded_sub_crops: Dict[str, Image.Image] = {}
    if user_img_path and (BASE_DIR / user_img_path).exists():
        try:
            up_pil = Image.open(BASE_DIR / user_img_path).convert("RGB")
            uw, uh = up_pil.size
            grid_boxes = {
                "outerwear": (0.04, 0.03, 0.46, 0.36),
                "cap": (0.04, 0.36, 0.44, 0.56),
                "bag": (0.03, 0.56, 0.46, 0.96),
                "top": (0.48, 0.03, 0.97, 0.38),
                "bottom": (0.48, 0.38, 0.97, 0.76),
                "shoes": (0.48, 0.76, 0.97, 0.98),
            }
            for g_slot, (x0, y0, x1, y1) in grid_boxes.items():
                uploaded_sub_crops[g_slot] = up_pil.crop((int(uw * x0), int(uh * y0), int(uw * x1), int(uh * y1)))
        except Exception:
            pass

    cutout_assets: Dict[str, str] = {}
    verified_exact_items: Dict[str, Dict[str, Any]] = {}
    en_descriptions: Dict[str, str] = {}
    sku_base = 960000000 + (base_seed % 30000000)

    for idx_slot, (cat_key, (file_tag, bp_tuple, default_store_url)) in enumerate(slot_map_bp.items(), start=1):
        bp_brand, bp_name, bp_price_str, bp_price_val, bp_color, bp_en_desc = bp_tuple
        rel_cut = f"assets/items/{archetype_id}_{file_tag}.png"
        abs_cut = BASE_DIR / rel_cut

        if cat_key in scraped_by_slot:
            sc = scraped_by_slot[cat_key]
            brand = sc.get("brand") or bp_brand
            name_tr = sc.get("name") or bp_name
            price_str = sc.get("price") or bp_price_str
            price_val = float(sc.get("price_val") or bp_price_val)
            color_tr = sc.get("color") or bp_color
            store_url = sc.get("store_url") or sc.get("product_url") or default_store_url
            sku_code = str(sc.get("sku") or (sku_base + idx_slot))
            en_desc = _translate_tr_item_to_en_prompt(name_tr, color_tr, cat_key)

            saved_cut = False
            img_u = sc.get("image_url") or ""
            if img_u.startswith("http"):
                try:
                    ir = requests.get(img_u, timeout=20)
                    if ir.status_code == 200 and len(ir.content) > 2000:
                        raw_im = Image.open(BytesIO(ir.content)).convert("RGB")
                        remove_white_studio_background(raw_im).save(abs_cut, format="PNG")
                        saved_cut = True
                except Exception:
                    pass
            if not saved_cut and cat_key in uploaded_sub_crops:
                remove_white_studio_background(uploaded_sub_crops[cat_key]).save(abs_cut, format="PNG")
                saved_cut = True
            if not saved_cut:
                pack_prompt = (
                    f"Clean isolated e-commerce studio product packshot photograph of {en_desc}, "
                    f"centered flat-lay on a PURE SOLID WHITE BACKGROUND #FFFFFF, no model, no text, ultra sharp"
                )
                raw_pack = cloud_fetch_ai_image(pack_prompt, width=768, height=768, seed=base_seed + 100 + idx_slot)
                if raw_pack is not None:
                    remove_white_studio_background(raw_pack).save(abs_cut, format="PNG")
        else:
            brand, name_tr, price_str, price_val, color_tr, en_desc = bp_tuple
            store_url = default_store_url
            sku_code = str(sku_base + idx_slot)
            if cat_key in uploaded_sub_crops:
                remove_white_studio_background(uploaded_sub_crops[cat_key]).save(abs_cut, format="PNG")
            else:
                pack_prompt = (
                    f"Clean isolated e-commerce studio product packshot photograph of {en_desc}, "
                    f"centered flat-lay on a PURE SOLID WHITE BACKGROUND #FFFFFF, no model, no text, ultra sharp"
                )
                raw_pack = cloud_fetch_ai_image(pack_prompt, width=768, height=768, seed=base_seed + 100 + idx_slot)
                if raw_pack is not None:
                    remove_white_studio_background(raw_pack).save(abs_cut, format="PNG")

        en_descriptions[cat_key] = en_desc
        cutout_assets[cat_key] = rel_cut
        verified_exact_items[cat_key] = {
            "brand": brand,
            "name": name_tr,
            "full_name": f"{brand} {name_tr}",
            "price": price_str,
            "price_val": price_val,
            "sku": sku_code,
            "color": color_tr,
            "store_url": store_url,
            "product_url": f"https://guzelai.com/go/{sku_code}",
            "guzelai_url": f"https://guzelai.com/go/{sku_code}",
        }

    # %100 FOTOGERÇEKÇİ GERÇEK İNSAN AI MODEL (Kadın / Erkek / Kız Çocuk / Erkek Çocuk — SIFIR ANİMASYON!)
    step_poses = [
        "right foot stepping forward mid-stride, full body head to toe clearly showing shoes on stone boulevard",
        "left foot stepping forward mid-stride, winter coat swaying naturally, full body head to toe clearly showing shoes",
        "confident warm smile stepping closer towards camera, full body head to toe clearly showing shoes",
    ]
    model_frames: List[str] = []
    for s_idx, pose_txt in enumerate(step_poses, start=1):
        rel_frame = f"assets/{archetype_id}_step{s_idx}.jpg"
        abs_frame = BASE_DIR / rel_frame
        prompt = build_photorealistic_human_model_prompt(
            segment=seg,
            district=bp["district"],
            hair_face=bp["hair_face"],
            outer_desc=en_descriptions["outerwear"],
            top_desc=en_descriptions["top"],
            bottom_desc=en_descriptions["bottom"],
            cap_desc=en_descriptions["cap"],
            bag_desc=en_descriptions["bag"],
            shoes_desc=en_descriptions["shoes"],
            pose_txt=pose_txt,
        )
        img = cloud_fetch_ai_image(prompt, width=768, height=1344, seed=base_seed + s_idx * 19)
        if img is not None:
            img_hd = img.resize((1080, 1920), Image.Resampling.LANCZOS)
            img_hd.save(abs_frame, format="JPEG", quality=95)
            model_frames.append(rel_frame)
            print(f"  ✓ [GERÇEKÇİ AI İNSAN MODEL {s_idx}/3 - {seg.upper()}] {rel_frame}")

    designer_map = {"kadin": "DEFNE", "erkek": "KEREM", "kiz_cocuk": "LEYLA", "erkek_cocuk": "MERT"}
    designer_name = designer_map.get(seg, "DEFNE")
    seg_title_map = {
        "kadin": "Kadın Kış Moda Gündemi Kreasyonu",
        "erkek": "Erkek Sartorial Kış Moda Gündemi Kreasyonu",
        "kiz_cocuk": "Kız Çocuk Kış Editoryal Kreasyonu",
        "erkek_cocuk": "Erkek Çocuk Kış Editoryal Kreasyonu",
    }
    custom_headline = user_text if len(user_text) > 8 else f"{bp['district']} {seg_title_map.get(seg, 'Kış Kreasyonu')}: {bp['palette_tr']}"

    new_arch = {
        "id": archetype_id,
        "gender_segment": seg,
        "designer_agent": designer_name,
        "is_telegram_custom": True,
        "requester_chat_id": requester_cid,
        "requester_name": requester_name,
        "title": f"{custom_headline} ✨",
        "spoken_hook_text": f"Bu kış stilinde aradığınız o kusursuz {bp['palette_tr']} uyumu!",
        "viral_hook": f"✨ {custom_headline}! Mankenin üzerindeki 6 parçanın stil önerisi ve doğrudan mağaza linkleri aşağıda 👇",
        "video_badge_collage": f"» MODA GÜNDEMİ • {designer_name} KREASYONU «",
        "video_badge_walk": f"» {bp['palette_tr'].upper()[:34]} «",
        "model_frames": model_frames,
        "cutout_assets": cutout_assets,
        "fallback_cutout_assets": dict(cutout_assets),
        "verified_exact_items": verified_exact_items,
        "category_map": {k: k for k in slot_map_bp},
        "keywords": {k: [v["color"].lower()] for k, v in verified_exact_items.items()},
    }

    dyn_cat = load_dynamic_creations_catalog()
    dyn_cat.append(new_arch)
    save_dynamic_creations_catalog(dyn_cat)
    return new_arch
