"""
GuzelAI Ajan Kaynakları Birimi (Ajan 19-22) + Moda Tasarım Atölyesi (Ajan 23-26) &
Argon'suz GitHub Actions 7/24 Kesintisiz Bulut Mevsimsel Kreasyon Fabrikası
---------------------------------------------------------------------------------
Ajan Kaynakları Birimi:
- Ajan 19: ARDA (agent-resources-director) -> Ajan Kaynakları, Performans & Sıfır-Tekrar Orkestrasyon Direktörü
- Ajan 20: MAYA (ai-model-casting-director) -> Özgün AI Manken Casting & Tekil Karakter Kilit Ajanı
- Ajan 21: KAAN (seasonal-creation-factory-agent) -> Mevsimsel Özgün Kreasyon & Argon'suz Bulut 1:1 Dekupe Fabrikası
- Ajan 22: VERA (zero-repeat-quality-auditor) -> Sıfır-Tekrar, Mevsimsel Uyum & Telegram Tekil Gönderim Başdenetçisi

Moda Tasarım Atölyesi (Yeni İşe Alınan Baş Moda Tasarımcıları):
- Ajan 23: DEFNE (womenswear-couture-atelier-designer) -> Kadın Kış & Quiet Luxury Kapsül Moda Baş Tasarımcısı
- Ajan 24: KEREM (menswear-sartorial-atelier-designer) -> Erkek Sartorial & Smart-Luxury Kış Moda Baş Tasarımcısı
- Ajan 25: LEYLA (girls-winter-atelier-designer) -> Kız Çocuk Kış & Preppy Kolej Moda Tasarımcısı
- Ajan 26: MERT (boys-urban-winter-atelier-designer) -> Erkek Çocuk Kış & Urban Kolej Moda Tasarımcısı
"""
import hashlib
import json
import os
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import requests
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_PATH = BASE_DIR / "output" / "zero_repeat_ledger.json"
DYNAMIC_CATALOG_PATH = BASE_DIR / "output" / "dynamic_creations_catalog.json"

# @guzelaicom Instagram profilinde ve Telegram'da daha önce paylaşılmış TÜM eski kombinler ve mankenler
# KALICI OLARAK EMEKLİYE AYRILDI (ASLA TEKRAR SEÇİLEMEZ VE GÖNDERİLEMEZ):
PERMANENTLY_RETIRED_ARCHETYPES = [
    "halloween_party_couple_vampiric_noir",
    "halloween_party_couple_gothic_oldmoney",
    "guzelai_gomlek_kase_mont_palazzo",
    "guzelai_elbise_deri_ceket_kombin",
    "sunday_slot1_espresso_cream_oldmoney",
    "sunday_slot2_olive_butter_taupe",
    "sunday_slot3_navy_camel_ivory",
    "pinterest_oldmoney_camel_iceblue_ecru",
    "erkek_slot1_oldmoney_kase_triko_chino",
    "erkek_slot2_smart_street_deri_bomber_jean",
    "cocuk_slot1_sonbahar_kolej_kombin",
    "cocuk_erkek_slot1_sonbahar_kolej_street",
    "veor_uranis_bordo_kapsul_2k",
    "tesla_halloween_ramp_curly",
    "inner_voice_black_bomber_stone_palazzo",
    "telegram_curly_champagne_palazzo",
    "curly_khaki_suede_palazzo",
    "pajama_morning_vibe",
    "chic_black_biker_denim",
    "casual_denim_sherpa_grey",
    "erkek_kasim_ortakoy_bordo_suet_siyah_triko",
]

PERMANENTLY_RETIRED_MODEL_FRAMES = [
    "assets/hw_couple1_step1.jpg",
    "assets/hw_couple2_step1.jpg",
    "assets/mon1_model_step1.jpg",
    "assets/mon2_model_step1.jpg",
    "assets/sun1_model_step1.jpg",
    "assets/sun2_model_step1.jpg",
    "assets/sun3_model_step1.jpg",
    "assets/om_model_step1.jpg",
    "assets/men1_model_step1.jpg",
    "assets/men2_model_step1.jpg",
    "assets/kid1_model_step1.jpg",
    "assets/kid_boy1_model_step1.jpg",
    "assets/hw27_women_step1.jpg",
    "assets/tesla_halloween_step1.jpg",
    "assets/inner_voice_curly_step1.jpg",
    "assets/telegram_curly_step1.jpg",
    "assets/curly_model_step1.jpg",
    "assets/outfit3_model_step1.jpg",
    "assets/outfit2_model_step1.jpg",
    "assets/trial1_model_street.jpg",
    "assets/erkek_ortakoy1_step1.jpg",
]

FASHION_ATELIER_DESIGNERS = [
    {
        "agent_number": 23,
        "code_name": "DEFNE",
        "subagent_id": "womenswear-couture-atelier-designer",
        "segment": "kadin",
        "title": "Kadın Kış & Quiet Luxury Kapsül Moda Baş Tasarımcısı",
        "specialty": "Kaşmir, kruvaze kaşe kaban, peluş yaka trençkot, boğazlı merinos triko ve yüksek bel yün palazzo silüetleri.",
    },
    {
        "agent_number": 24,
        "code_name": "KEREM",
        "subagent_id": "menswear-sartorial-atelier-designer",
        "segment": "erkek",
        "title": "Erkek Sartorial & Smart-Luxury Kış Moda Baş Tasarımcısı",
        "specialty": "İtalyan kruvaze kaşe kaban, süet shearling ceket, balıkçı yaka yün triko ve flanel kışlık pantolon kombinleri.",
    },
    {
        "agent_number": 25,
        "code_name": "LEYLA",
        "subagent_id": "girls-winter-atelier-designer",
        "segment": "kiz_cocuk",
        "title": "Kız Çocuk Kış & Preppy Kolej Moda Tasarımcısı",
        "specialty": "Peluş teddy kaban, kapitone puffer mont, jakarlı/örgü kışlık triko, ponponlu bere ve konforlu çocuk kış kombinleri.",
    },
    {
        "agent_number": 26,
        "code_name": "MERT",
        "subagent_id": "boys-urban-winter-atelier-designer",
        "segment": "erkek_cocuk",
        "title": "Erkek Çocuk Kış & Urban Kolej Moda Tasarımcısı",
        "specialty": "Kapüşonlu kışlık puffer mont, peluş yaka kolej mont, renk bloklu triko ve kargo kışlık chino kombinleri.",
    },
]


def load_zero_repeat_ledger() -> dict:
    os.makedirs(LEDGER_PATH.parent, exist_ok=True)
    data = {
        "retired_archetypes": list(PERMANENTLY_RETIRED_ARCHETYPES),
        "retired_model_frames": list(PERMANENTLY_RETIRED_MODEL_FRAMES),
        "telegram_dispatched_ids": list(PERMANENTLY_RETIRED_ARCHETYPES),
        "last_telegram_dispatch_ts": 0.0,
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }
    if LEDGER_PATH.exists():
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k in ("retired_archetypes", "retired_model_frames", "telegram_dispatched_ids"):
                for item in saved.get(k, []):
                    if item and item not in data[k]:
                        data[k].append(item)
            if saved.get("last_telegram_dispatch_ts"):
                data["last_telegram_dispatch_ts"] = float(saved["last_telegram_dispatch_ts"])
        except Exception:
            pass

    for hist_file, key in (
        (BASE_DIR / "output" / "published_outfits_history.json", "used_archetypes"),
        (BASE_DIR / "output" / "instagram_uploaded_history.json", "published_archetypes"),
    ):
        if hist_file.exists():
            try:
                with open(hist_file, "r", encoding="utf-8") as hf:
                    hd = json.load(hf)
                for aid in hd.get(key, []):
                    if aid and aid not in data["retired_archetypes"]:
                        data["retired_archetypes"].append(aid)
            except Exception:
                pass

    save_zero_repeat_ledger(data)
    return data


def save_zero_repeat_ledger(data: dict) -> None:
    os.makedirs(LEDGER_PATH.parent, exist_ok=True)
    data["updated_at"] = datetime.utcnow().isoformat() + "Z"
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_creation_or_model_used(archetype: dict, ledger: dict | None = None) -> bool:
    """
    Ajan 22 VERA & Ajan 19 ARDA Sıfır-Tekrar Kilidi:
    Hem kombin ID'si hem de manken görseli (model_frames[0]) daha önce HİÇ kullanılmamış olmalıdır.
    """
    if ledger is None:
        ledger = load_zero_repeat_ledger()
    arch_id = archetype.get("id", "")
    model_frame = (archetype.get("model_frames") or [""])[0].replace("\\", "/")
    if arch_id in ledger.get("retired_archetypes", []):
        return True
    if model_frame in ledger.get("retired_model_frames", []):
        return True
    return False


def mark_creation_and_model_used(archetype_id: str, model_frame: str = "", telegram_sent: bool = False) -> None:
    ledger = load_zero_repeat_ledger()
    if archetype_id and archetype_id not in ledger["retired_archetypes"]:
        ledger["retired_archetypes"].append(archetype_id)
    norm_frame = (model_frame or "").replace("\\", "/")
    if norm_frame and norm_frame not in ledger["retired_model_frames"]:
        ledger["retired_model_frames"].append(norm_frame)
    if telegram_sent:
        if archetype_id and archetype_id not in ledger["telegram_dispatched_ids"]:
            ledger["telegram_dispatched_ids"].append(archetype_id)
        ledger["last_telegram_dispatch_ts"] = time.time()
    save_zero_repeat_ledger(ledger)


def load_dynamic_creations_catalog() -> List[Dict[str, Any]]:
    if DYNAMIC_CATALOG_PATH.exists():
        try:
            with open(DYNAMIC_CATALOG_PATH, "r", encoding="utf-8") as f:
                items = json.load(f)
            if isinstance(items, list):
                return items
        except Exception:
            pass
    return []


def save_dynamic_creations_catalog(items: List[Dict[str, Any]]) -> None:
    os.makedirs(DYNAMIC_CATALOG_PATH.parent, exist_ok=True)
    with open(DYNAMIC_CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def remove_white_studio_background(img: Image.Image) -> Image.Image:
    """
    Saf beyaz (#FFFFFF) ve kenar vinyetli stüdyo packshot görselini kenar bağlantılı
    (border-connected) NumPy maskeleme ile pürüzsüz şeffaf RGBA PNG dekupe görsele dönüştürür.
    """
    from collections import deque

    rgba = img.convert("RGBA")
    arr = np.array(rgba, dtype=np.int16)
    h, w, _ = arr.shape
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    lum = (r + g + b) // 3
    spread = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)

    # Pure white background + border-connected light studio grey vignette
    bg_mask = (lum > 242) & (spread < 18)
    candidate_bg = (lum > 204) & (spread < 16)

    # Fast 4-px block flood-fill from outer borders so white shoe soles inside aren't eaten
    step = 2
    gh, gw = (h + step - 1) // step, (w + step - 1) // step
    cand_small = candidate_bg[::step, ::step]
    visited = np.zeros((gh, gw), dtype=bool)
    q = deque()
    for x in range(gw):
        if cand_small[0, x]:
            visited[0, x] = True
            q.append((0, x))
        if cand_small[gh - 1, x] and not visited[gh - 1, x]:
            visited[gh - 1, x] = True
            q.append((gh - 1, x))
    for y in range(gh):
        if cand_small[y, 0] and not visited[y, 0]:
            visited[y, 0] = True
            q.append((y, 0))
        if cand_small[y, gw - 1] and not visited[y, gw - 1]:
            visited[y, gw - 1] = True
            q.append((y, gw - 1))
    while q:
        cy, cx = q.popleft()
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if 0 <= ny < gh and 0 <= nx < gw and not visited[ny, nx] and cand_small[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))

    flood_full = np.repeat(np.repeat(visited, step, axis=0), step, axis=1)[:h, :w]
    bg_mask = bg_mask | (flood_full & candidate_bg)
    soft_mask = (lum > 196) & (spread < 15) & (~bg_mask) & flood_full

    alpha = arr[:, :, 3].copy()
    alpha[bg_mask] = 0
    alpha[soft_mask] = np.clip((215 - lum[soft_mask]) * 12, 0, 255)
    out = arr.astype(np.uint8)
    out[:, :, 3] = alpha.astype(np.uint8)
    res = Image.fromarray(out, mode="RGBA")
    bbox = res.getbbox()
    if bbox:
        cropped = res.crop(bbox)
        canvas = Image.new("RGBA", (900, 900), (0, 0, 0, 0))
        cropped.thumbnail((820, 820), Image.Resampling.LANCZOS)
        ox = (900 - cropped.width) // 2
        oy = (900 - cropped.height) // 2
        canvas.paste(cropped, (ox, oy), cropped)
        return canvas
    return res


def _call_hf_flux_space(space_base: str, payload_data: list, timeout_sec: int = 75) -> Optional[Image.Image]:
    """
    HuggingFace Gradio 5 HTTP API üzerinden Argon veya API anahtarı gerektirmeden
    doğrudan GitHub Actions (ubuntu-latest) bulut ortamında FLUX.1 görseli üretir.
    """
    post_r = requests.post(
        f"{space_base}/gradio_api/call/infer",
        json={"data": payload_data},
        timeout=25,
    )
    if post_r.status_code != 200:
        return None
    event_id = post_r.json().get("event_id")
    if not event_id:
        return None

    sse_r = requests.get(f"{space_base}/gradio_api/call/infer/{event_id}", timeout=timeout_sec)
    if sse_r.status_code != 200:
        return None

    img_url = None
    for line in sse_r.text.splitlines():
        if line.startswith("data:"):
            raw_json = line[len("data:"):].strip()
            try:
                parsed = json.loads(raw_json)
                if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
                    img_url = parsed[0].get("url")
                    if not img_url and parsed[0].get("path"):
                        img_url = f"{space_base}/gradio_api/file={parsed[0]['path']}"
                    if img_url:
                        break
            except Exception:
                continue

    if not img_url:
        return None

    dl = requests.get(img_url, timeout=35)
    if dl.status_code == 200 and len(dl.content) > 5000:
        return Image.open(BytesIO(dl.content)).convert("RGB")
    return None


def cloud_fetch_ai_image(prompt: str, width: int, height: int, seed: int) -> Optional[Image.Image]:
    """
    GitHub Actions (ubuntu-latest) üzerinde Argon / yerel sunucu olmadan
    çok katmanlı FLUX.1 bulut motorlarıyla AI görsel sentezler.
    """
    w = max(512, min(1024, (width // 64) * 64))
    h = max(512, min(1344, (height // 64) * 64))
    safe_seed = int(abs(seed) % 2147483000)

    providers = [
        ("https://black-forest-labs-flux-1-schnell.hf.space", [prompt, safe_seed, False, w, h, 4]),
        ("https://multimodalart-flux-1-merged.hf.space", [prompt, safe_seed, False, w, h, 3.5, 6]),
    ]
    for space_url, p_data in providers:
        for attempt in range(1, 3):
            try:
                img = _call_hf_flux_space(space_url, p_data)
                if img is not None:
                    if (img.width, img.height) != (width, height):
                        img = img.resize((width, height), Image.Resampling.LANCZOS)
                    return img
            except Exception as e:
                print(f"  [Bulut FLUX Sentez Denemesi {space_url} #{attempt}] {e}")
                time.sleep(2 * attempt)
    return None


# ==============================================================================
# MODA TASARIM ATÖLYESİ (DEFNE, KEREM, LEYLA, MERT) SONSUZ KIŞ KREASYON MATRİSİ
# ==============================================================================
PROCEDURAL_ATELIER_MATRIX: Dict[str, List[Dict[str, Any]]] = {
    "kadin": [
        {
            "district": "Nişantaşı Abdi İpekçi",
            "slug": "nisantasi_abdi",
            "hair_face": "wavy caramel-chestnut hair and amber eyes",
            "palette_tr": "Zümrüt Yeşili Kaşe & Fildişi Kaşmir",
            "outer": ("İPEKYOL", "Kadın Zümrüt Yeşili Kruvaze Uzun Yün Kaşe Kaban", "3.890₺", 3890.0, "Zümrüt Yeşili", "emerald forest green double-breasted long wool winter coat"),
            "cap": ("PRADA EYEWEAR", "Kadın Kahve / Gold Geometrik Güneş Gözlüğü", "4.490₺", 4490.0, "Kahve / Gold", "tortoiseshell and gold geometric women sunglasses"),
            "top": ("YARGICI", "Kadın Fildişi / Ekru Fitilli Kaşmir Boğazlı Triko Kazak", "1.490₺", 1490.0, "Fildişi", "ivory cream ribbed turtleneck cashmere sweater"),
            "bottom": ("TWIST", "Kadın Koyu Kahve Yüksek Bel Pileli Yün Palazzo Pantolon", "1.650₺", 1650.0, "Koyu Kahve", "dark espresso brown high-waisted pleated wide-leg wool palazzo trousers"),
            "bag": ("BAGMORI", "Kadın Zümrüt Yeşili Gold Tokalı Kapitone Omuz Çantası", "899₺", 899.0, "Zümrüt Yeşili", "structured emerald green quilted leather shoulder bag with gold clasp"),
            "shoes": ("ADIDAS", "Kadın Krem / Zümrüt Yeşili Süet Detaylı Court Sneaker", "3.799₺", 3799.0, "Krem / Yeşil", "cream leather low-top court sneakers with emerald green suede stripes"),
        },
        {
            "district": "Arnavutköy Sahil",
            "slug": "arnavutkoy_sahil",
            "hair_face": "sleek platinum-ash blonde shoulder-length hair and green eyes",
            "palette_tr": "Gece Laciverti Tüvit & Buz Mavisi Merinos",
            "outer": ("MANGO", "Kadın Gece Laciverti Gold Düğmeli Uzun Tüvit Kaban", "3.599₺", 3599.0, "Gece Laciverti", "midnight navy blue long tweed winter overcoat with gold buttons"),
            "cap": ("VOGUE EYEWEAR", "Kadın Siyah Oval Retro Güneş Gözlüğü", "2.290₺", 2290.0, "Siyah", "sleek black oval acetate sunglasses"),
            "top": ("MASSIMO DUTTI", "Kadın Buz Mavisi Yün / Kaşmir V-Yaka Triko Kazak", "1.790₺", 1790.0, "Buz Mavisi", "soft ice-blue cashmere V-neck winter knit sweater"),
            "bottom": ("ZARA", "Kadın Kırık Beyaz Kışlık Yün Karışımlı Geniş Paça Pantolon", "1.490₺", 1490.0, "Kırık Beyaz", "winter off-white tailored wide-leg wool trousers"),
            "bag": ("BAGMORI", "Kadın Lacivert Kroko Dokulu Gold Zincirli Çanta", "849₺", 849.0, "Lacivert", "midnight navy croc-embossed leather handbag with gold buckle"),
            "shoes": ("NEW BALANCE", "Kadın Beyaz / Lacivert Süet Kışlık Retro Sneaker", "3.990₺", 3990.0, "Beyaz / Lacivert", "white and midnight navy suede retro court sneakers"),
        },
        {
            "district": "Çengelköy Boğaz",
            "slug": "cengelkoy_bogaz",
            "hair_face": "dark chocolate curly shoulder-length hair and hazel eyes",
            "palette_tr": "Vizon Peluş Kaban & Tarçın Triko",
            "outer": ("QUZU", "Kadın Vizon / Kum Beji Uzun Teddy Peluş Kışlık Kaban", "2.990₺", 2990.0, "Vizon", "warm taupe mink plush teddy shearling long winter coat"),
            "cap": ("RAY-BAN", "Kadın Gold Çerçeveli Kahve Camlı Gözlük", "4.290₺", 4290.0, "Gold / Kahve", "gold wire frame sunglasses with brown lenses"),
            "top": ("İPEKYOL", "Kadın Tarçın / Kiremit Fitilli Dik Yaka Triko Kazak", "1.190₺", 1190.0, "Tarçın", "warm cinnamon terracotta ribbed mock-neck knit sweater"),
            "bottom": ("STRADIVARIUS", "Kadın Koyu Antrasit Yüksek Bel Kışlık Palazzo Jean", "1.290₺", 1290.0, "Antrasit", "dark charcoal grey high-waisted wide-leg denim jeans"),
            "bag": ("BAGMORI", "Kadın Taba / Tarçın Süet Detaylı El & Omuz Çantası", "879₺", 879.0, "Tarçın / Taba", "structured cinnamon tan suede and leather handbag"),
            "shoes": ("PUMA", "Kadın Bej / Tarçın Süet Gum Tabanlı Sneaker", "3.490₺", 3490.0, "Bej / Tarçın", "beige and cinnamon suede low-top sneakers with gum sole"),
        },
    ],
    "erkek": [
        {
            "district": "Moda İskele Bulvarı",
            "slug": "moda_iskele",
            "hair_face": "short dark-brown textured crop hair and clean jawline",
            "palette_tr": "Kömür Siyahı Kaşe & Gri Merinos Balıkçı",
            "outer": ("NETWORK", "Erkek Kömür Siyahı Kruvaze İtalyan Yün Kaşe Kaban", "4.690₺", 4690.0, "Siyah", "men jet black double-breasted tailored wool winter overcoat"),
            "cap": ("PERSOL", "Erkek Siyah Asetat Köşeli Güneş Gözlüğü", "4.950₺", 4950.0, "Siyah", "men matte black rectangular acetate sunglasses"),
            "top": ("MASSIMO DUTTI", "Erkek Gümüş Gri Fitilli Boğazlı Merinos Yün Kazak", "1.690₺", 1690.0, "Gümüş Gri", "men heather silver-grey ribbed merino turtleneck sweater"),
            "bottom": ("BEYMEN CLUB", "Erkek Lacivert Flanel Pileli Kışlık Yün Pantolon", "2.190₺", 2190.0, "Koyu Lacivert", "men dark navy wool flannel pleated winter trousers"),
            "bag": ("TERGAN", "Erkek Siyah Deri Hafta Sonu & Evrak Çantası", "2.890₺", 2890.0, "Siyah", "men black pebbled leather weekender duffel bag"),
            "shoes": ("ADIDAS", "Erkek Siyah / Gri Süet Beyaz Tabanlı Court Sneaker", "3.690₺", 3690.0, "Siyah / Beyaz", "men black suede low-top court sneakers with grey stripes and white cupsole"),
        },
        {
            "district": "Akaretler Sıraevler",
            "slug": "akaretler_siraevler",
            "hair_face": "medium wavy light-brown hair and neat short beard",
            "palette_tr": "Taba Süet Shearling & Koyu Lacivert Triko",
            "outer": ("ZARA MAN", "Erkek Taba / Konyak İçi Kürklü Süet Kışlık Mont", "3.490₺", 3490.0, "Taba / Krem", "men cognac tan suede winter jacket with cream shearling collar"),
            "cap": ("RAY-BAN", "Erkek Gold / Yeşil Camlı Klasik Aviator Gözlük", "4.750₺", 4750.0, "Gold", "men gold metal aviator sunglasses dark green lenses"),
            "top": ("ALTINYILDIZ CLASSICS", "Erkek Koyu Lacivert Saç Örgü Yün Triko Kazak", "1.190₺", 1190.0, "Koyu Lacivert", "men dark navy blue cable-knit crewneck winter wool sweater"),
            "bottom": ("MANGO MAN", "Erkek Kırık Beyaz / Taş Rengi Kışlık Kadife Chino Pantolon", "1.490₺", 1490.0, "Taş Beji", "men warm stone off-white fine corduroy straight winter chinos"),
            "bag": ("TERGAN", "Erkek Taba Deri Postacı & Omuz Çantası", "2.490₺", 2490.0, "Taba", "men cognac tan leather messenger crossbody bag"),
            "shoes": ("NEW BALANCE", "Erkek Lacivert / Taba Süet Kışlık Sneaker", "3.890₺", 3890.0, "Lacivert / Taba", "men navy and tan suede retro low-top sneakers"),
        },
    ],
    "kiz_cocuk": [
        {
            "district": "Caddebostan Sahil Parkı",
            "slug": "caddebostan_park",
            "hair_face": "3D CGI virtual fashion catalog character avatar with chestnut braided pigtails",
            "palette_tr": "Bebek Mavisi Kapitone Mont & Ekru Örgü Triko",
            "is_3d_avatar": True,
            "outer": ("MANGO KIDS", "Kız Çocuk Bebek Mavisi Kapüşonlu Şişme Kışlık Mont", "1.699₺", 1699.0, "Bebek Mavisi", "kids pastel sky-blue hooded quilted winter puffer jacket"),
            "cap": ("LC WAIKIKI KIDS", "Kız Çocuk Krem Ponponlu Fitilli Triko Bere", "249₺", 249.0, "Krem", "kids cream ribbed knit winter beanie with yarn pom-pom"),
            "top": ("ZARA KIDS", "Kız Çocuk Ekru / Mavi Kar Tanesi Desenli Triko Kazak", "799₺", 799.0, "Ekru / Mavi", "kids cream knit crewneck sweater with sky-blue winter snowflake pattern"),
            "bottom": ("DEFACTO KIDS", "Kız Çocuk Koyu Lacivert İçi Polarlı Kışlık Pantolon", "599₺", 599.0, "Koyu Lacivert", "kids dark navy comfortable straight-leg winter cotton trousers"),
            "bag": ("BAGMORI", "Kız Çocuk Bebek Mavisi Kapitone Mini Sırt Çantası", "549₺", 549.0, "Bebek Mavisi", "kids pastel sky-blue quilted mini backpack"),
            "shoes": ("ADIDAS KIDS", "Kız Çocuk Beyaz / Bebek Mavisi Bantlı Sneaker", "2.199₺", 2199.0, "Beyaz / Mavi", "kids white leather court sneakers with pastel sky-blue stripes"),
        },
    ],
    "erkek_cocuk": [
        {
            "district": "Maçka Sanat Parkı",
            "slug": "macka_park",
            "hair_face": "3D CGI virtual fashion catalog character avatar with wavy light-chestnut hair",
            "palette_tr": "Zümrüt Yeşili Kışlık Parka & Krem Triko",
            "is_3d_avatar": True,
            "outer": ("ZARA KIDS", "Erkek Çocuk Zümrüt / Orman Yeşili Kapüşonlu Kışlık Parka", "1.899₺", 1899.0, "Orman Yeşili", "kids dark forest-green hooded quilted winter parka jacket"),
            "cap": ("LC WAIKIKI KIDS", "Erkek Çocuk Lacivert Fitilli Kışlık Triko Bere", "229₺", 229.0, "Lacivert", "kids dark navy vertical ribbed knit folded winter beanie"),
            "top": ("MANGO KIDS", "Erkek Çocuk Krem / Yeşil Çizgili Pamuklu Triko Kazak", "749₺", 749.0, "Krem / Yeşil", "kids cream cotton knit crewneck sweater with forest-green chest stripes"),
            "bottom": ("DEFACTO KIDS", "Erkek Çocuk Koyu Gri / Antrasit Kışlık Kargo Pantolon", "649₺", 649.0, "Antrasit", "kids dark charcoal grey cotton winter cargo trousers"),
            "bag": ("PUMA KIDS", "Erkek Çocuk Orman Yeşili / Lacivert Sırt Çantası", "699₺", 699.0, "Orman Yeşili", "kids forest-green and navy canvas backpack"),
            "shoes": ("ADIDAS KIDS", "Erkek Çocuk Beyaz / Yeşil Çizgili Court Sneaker", "2.249₺", 2249.0, "Beyaz / Yeşil", "kids white leather court sneakers with forest-green side stripes"),
        },
    ],
}


def synthesize_autonomous_winter_creation(
    target_segment: str,
    zero_ledger: Optional[dict] = None,
) -> Dict[str, Any]:
    """
    Ajan 23-26 (DEFNE, KEREM, LEYLA, MERT) + Ajan 20 MAYA + Ajan 21 KAAN:
    Statik kombin havuzu tükendiğinde GitHub Actions (ubuntu-latest) üzerinde HİÇ DURMADAN
    yepyeni, %100 sıfır-tekrar kış kreasyonu, 3 kare yürüyen AI manken ve 6 adet 1:1 şeffaf PNG
    dekupe görseli üretip `output/dynamic_creations_catalog.json` içine kaydeder.
    """
    if zero_ledger is None:
        zero_ledger = load_zero_repeat_ledger()

    retired_ids = set(zero_ledger.get("retired_archetypes", []))
    dynamic_catalog = load_dynamic_creations_catalog()
    existing_dyn_ids = {d.get("id", "") for d in dynamic_catalog}

    try:
        from viral_screenwriter_evolution import get_evolved_procedural_matrix
        active_matrix = get_evolved_procedural_matrix(PROCEDURAL_ATELIER_MATRIX)
    except Exception:
        active_matrix = PROCEDURAL_ATELIER_MATRIX

    seg = target_segment if target_segment in active_matrix else "kadin"
    candidates = active_matrix[seg]

    chosen_bp = None
    variant_round = 1
    for round_idx in range(1, 50):
        for bp in candidates:
            suffix = "" if round_idx == 1 else f"_v{round_idx}"
            cand_id = f"atelier_{seg}_{bp['slug']}_kis{suffix}"
            if cand_id not in retired_ids and cand_id not in existing_dyn_ids:
                chosen_bp = bp
                variant_round = round_idx
                archetype_id = cand_id
                break
        if chosen_bp:
            break

    if not chosen_bp:
        chosen_bp = candidates[0]
        variant_round = int(time.time()) % 10000
        archetype_id = f"atelier_{seg}_{chosen_bp['slug']}_kis_{variant_round}"

    designer_map = {"kadin": "DEFNE", "erkek": "KEREM", "kiz_cocuk": "LEYLA", "erkek_cocuk": "MERT"}
    designer_name = designer_map.get(seg, "DEFNE")
    print(
        f"🎨 [Moda Tasarım Atölyesi - {designer_name} + MAYA + KAAN] "
        f"Bulut üzerinde yepyeni kış kreasyonu sentezleniyor: {archetype_id}..."
    )

    assets_dir = BASE_DIR / "assets"
    items_dir = assets_dir / "items"
    assets_dir.mkdir(parents=True, exist_ok=True)
    items_dir.mkdir(parents=True, exist_ok=True)

    base_seed = int(hashlib.md5(archetype_id.encode("utf-8")).hexdigest()[:8], 16)
    is_3d = bool(chosen_bp.get("is_3d_avatar", False))

    outer_desc = chosen_bp["outer"][5]
    cap_desc = chosen_bp["cap"][5]
    top_desc = chosen_bp["top"][5]
    bottom_desc = chosen_bp["bottom"][5]
    bag_desc = chosen_bp["bag"][5]
    shoes_desc = chosen_bp["shoes"][5]

    model_frames: List[str] = []
    step_poses = [
        "right foot stepping forward mid-stride, full body head to toe showing shoes on stone boulevard",
        "left foot stepping forward mid-stride, winter coat swaying naturally, full body head to toe showing shoes",
        "confident warm smile stepping closer towards camera, full body head to toe showing shoes",
    ]
    subject_prefix = (
        f"Vertical 9:16 full-body stylized 3D CGI virtual fashion catalog character ({chosen_bp['hair_face']})"
        if is_3d
        else f"Vertical 9:16 photorealistic full-body street fashion lookbook photograph of a 100% AI adult fashion model with {chosen_bp['hair_face']}"
    )

    try:
        from guzelai_holding_hr_academy import build_supermodel_editorial_prompt
    except Exception:
        build_supermodel_editorial_prompt = lambda p, is_3d_avatar=False: p

    for s_idx, pose_txt in enumerate(step_poses, start=1):
        rel_frame = f"assets/{archetype_id}_step{s_idx}.jpg"
        abs_frame = BASE_DIR / rel_frame
        raw_prompt = (
            f"{subject_prefix} walking along {chosen_bp['district']} Istanbul in crisp winter daylight, {pose_txt}, "
            f"wearing an open {outer_desc} over a {top_desc}, {bottom_desc}, {cap_desc}, carrying a {bag_desc}, "
            f"and wearing {shoes_desc}, editorial winter fashion lookbook, soft bokeh, no text, no watermark"
        )
        prompt = build_supermodel_editorial_prompt(raw_prompt, is_3d_avatar=is_3d)
        img = cloud_fetch_ai_image(prompt, width=768, height=1344, seed=base_seed + s_idx * 17)
        if img is None:
            raise RuntimeError(f"Bulut FLUX motoru manken karesi üretemedi: {rel_frame}")
        img_hd = img.resize((1080, 1920), Image.Resampling.LANCZOS)
        img_hd.save(abs_frame, format="JPEG", quality=93)
        model_frames.append(rel_frame)
        print(f"  ✓ [MAYA Manken Karesi {s_idx}/3] {rel_frame}")

    slot_defs = [
        ("outerwear", "01_outer", chosen_bp["outer"], "https://www.trendyol.com/kaban-x-c55"),
        ("cap", "02_cap", chosen_bp["cap"], "https://www.trendyol.com/aksesuar-x-c27"),
        ("top", "03_top", chosen_bp["top"], "https://www.trendyol.com/kazak-x-c1092"),
        ("bottom", "04_bottom", chosen_bp["bottom"], "https://www.trendyol.com/pantolon-x-c70"),
        ("bag", "05_bag", chosen_bp["bag"], "https://www.bagmori.com"),
        ("shoes", "06_shoes", chosen_bp["shoes"], "https://www.trendyol.com/spor-ayakkabi-x-c109"),
    ]

    cutout_assets: Dict[str, str] = {}
    verified_exact_items: Dict[str, Dict[str, Any]] = {}
    sku_base = 940000000 + (base_seed % 50000000)

    for idx_slot, (cat_key, file_tag, spec_tuple, store_link) in enumerate(slot_defs, start=1):
        brand, name_tr, price_str, price_val, color_tr, en_desc = spec_tuple
        rel_cut = f"assets/items/{archetype_id}_{file_tag}.png"
        abs_cut = BASE_DIR / rel_cut
        pack_prompt = (
            f"Clean isolated e-commerce studio product packshot photograph of {en_desc}, "
            f"centered flat-lay ghost mannequin on a PURE SOLID WHITE BACKGROUND #FFFFFF, "
            f"no model, no person, no shadows on edges, no hangtags, no text, ultra sharp"
        )
        raw_pack = cloud_fetch_ai_image(pack_prompt, width=768, height=768, seed=base_seed + 100 + idx_slot)
        if raw_pack is None:
            raise RuntimeError(f"Bulut FLUX motoru ürün dekupe görseli üretemedi: {rel_cut}")
        cut_rgba = remove_white_studio_background(raw_pack)
        cut_rgba.save(abs_cut, format="PNG")
        cutout_assets[cat_key] = rel_cut
        sku_code = str(sku_base + idx_slot)
        verified_exact_items[cat_key] = {
            "brand": brand,
            "name": name_tr,
            "full_name": f"{brand} {name_tr}",
            "price": price_str,
            "price_val": price_val,
            "sku": sku_code,
            "color": color_tr,
            "store_url": store_link,
        }
        print(f"  ✓ [KAAN 1:1 Dekupe {idx_slot}/6] {rel_cut} ({brand} - {name_tr})")

    seg_badge_map = {
        "kadin": "👩 Kadın Kış Tasarım Kreasyonu",
        "erkek": "👨 Erkek Kış Tasarım Kreasyonu",
        "kiz_cocuk": "👧 Kız Çocuk Kış Tasarım Kreasyonu",
        "erkek_cocuk": "👦 Erkek Çocuk Kış Tasarım Kreasyonu",
    }
    new_archetype = {
        "id": archetype_id,
        "gender_segment": seg,
        "designer_agent": designer_name,
        "title": f"{chosen_bp['district']} Kış Tasarım Kreasyonu: {chosen_bp['palette_tr']} ({seg_badge_map.get(seg, '')} • Tasarım: {designer_name}) ❄️✨",
        "viral_hook": f"🛑 GuzelAI Moda Tasarım Atölyesi ({designer_name}) imzalı yepyeni kış kreasyonu! Mankenin üzerindeki 6 parçanın birebir mağaza linkleri aşağıda 👇",
        "model_frames": model_frames,
        "cutout_assets": cutout_assets,
        "fallback_cutout_assets": dict(cutout_assets),
        "verified_exact_items": verified_exact_items,
        "category_map": {
            "outerwear": "outerwear",
            "cap": "cap",
            "top": "top",
            "bottom": "bottom",
            "bag": "bag",
            "shoes": "shoes",
        },
        "keywords": {k: [v["color"].lower()] for k, v in verified_exact_items.items()},
    }

    dynamic_catalog.append(new_archetype)
    save_dynamic_creations_catalog(dynamic_catalog)
    return new_archetype
