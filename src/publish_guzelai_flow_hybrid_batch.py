"""
GuzelAI.com Official Models + 1080p Google Flow Hybrid (Kombin Collage + Real Walk) Publisher
=============================================================================================
Renders and broadcasts the 2 new 1080p Full HD (1080x1920 @ 30fps) Hybrid Reels:
1. `kadin_guzelai_leyla_om01_camel_kasmir_cikolata` (Official guzelai.com Model: Leyla)
2. `erkek_guzelai_kenzo_om01_camel_kase_kronograf` (Official guzelai.com Model: Kenzo Takahashi)
to Telegram (@guzelaibot), Pinterest, and guzelai.com (while respecting today's 24h Instagram curing lock).
"""

import json
import os
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from autonomous_creation_factory import mark_creation_and_model_used
from fashion_agenda_engine import enrich_outfit_with_fashion_agenda
from gender_style_guardrail import (
    inspect_and_enforce_gender_compliance,
    run_fashion_design_council_session,
)
from guzelai_official_models import enforce_guzelai_official_model_lock
from main import build_caption, build_links_comment
from outfit_generator import OUTFIT_ARCHETYPES, _format_price_tr
from pinterest_publisher import publish_to_pinterest_cdp, save_pinterest_outputs
from render_reels import render_kombin_reel
from telegram_publisher import publish_to_telegram, save_telegram_outputs
from website_publisher import publish_to_guzelai_website

ARTIFACT_DIR = Path(r"C:\Users\zenci\.gemini\antigravity\brain\1ad6f174-c6c1-4c51-932c-98014af43950")


def build_outfit_from_arch_id(arch_id: str) -> dict:
    arch = next(a for a in OUTFIT_ARCHETYPES if a["id"] == arch_id)
    items = {}
    for k, v in arch["verified_exact_items"].items():
        it = dict(v)
        sku_str = str(it.get("sku", "")).strip()
        it["guzelai_url"] = f"https://guzelai.com/go/{sku_str}"
        it["product_url"] = f"https://guzelai.com/go/{sku_str}"
        it["local_asset"] = arch["cutout_assets"].get(k)
        it["fallback_asset"] = arch["fallback_cutout_assets"].get(k)
        items[k] = it

    total_price = sum(float(v.get("price_val", 0.0)) for v in items.values())
    total_price_str = _format_price_tr(total_price)

    outfit = {
        "slot": "guzelai_flow_1080p_hybrid",
        "is_trial": False,
        "archetype_id": arch["id"],
        "gender_segment": arch["gender_segment"],
        "ai_model_verified": True,
        "archetype_title": arch["title"],
        "preferred_music_id": arch.get("preferred_music_id", "old_money_violin_orchestra_pov"),
        "hook_title": arch["title"],
        "spoken_hook_text": arch.get("spoken_hook_text", arch["title"]),
        "x_short_hook": arch["title"][:95],
        "yt_short_title": arch["title"],
        "tiktok_hook_title": f"POV: {arch.get('spoken_hook_text', arch['title'])}",
        "pinterest_title": f"{arch['title']} | GuzelAI.com",
        "viral_hook": arch["viral_hook"],
        "video_badge_collage": arch["video_badge_collage"],
        "video_badge_walk": arch["video_badge_walk"],
        "seo_note": arch["seo_note"],
        "items": items,
        "cutout_assets": arch["cutout_assets"],
        "total_price_val": total_price,
        "total_price_str": total_price_str,
        "model_frames": list(arch["model_frames"]),
    }
    enforce_guzelai_official_model_lock(outfit)
    enrich_outfit_with_fashion_agenda(outfit)
    inspect_and_enforce_gender_compliance(outfit, auto_heal=True)
    run_fashion_design_council_session(outfit)
    return outfit


def process_and_publish_single(arch_id: str) -> dict:
    out_dir = str(BASE_DIR / "output")
    os.makedirs(out_dir, exist_ok=True)
    os.environ["REEL_RES_MODE"] = "1080p"

    outfit = build_outfit_from_arch_id(arch_id)
    mp4_path = os.path.join(out_dir, "daily_kombin_reel.mp4")

    print(f"\n==================================================================")
    print(f"🎬 [1080p HİBRİT REEL ÜRETİMİ BAŞLIYOR]: {arch_id}")
    print(f"👤 Resmi Manken: {outfit.get('guzelai_model_badge')}")
    print(f"==================================================================")

    render_kombin_reel(outfit, mp4_path, watermark="@guzelaicom")

    caption = build_caption(outfit)
    links_comment = build_links_comment(outfit)
    with open(os.path.join(out_dir, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(caption + "\n")
    with open(os.path.join(out_dir, "pinned_comment.txt"), "w", encoding="utf-8") as f:
        f.write(links_comment + "\n")
    with open(os.path.join(out_dir, "outfit_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(outfit, f, ensure_ascii=False, indent=2)

    save_telegram_outputs(outfit, out_dir=out_dir)
    save_pinterest_outputs(outfit, out_dir=out_dir)

    # Copy artifacts for user review
    if ARTIFACT_DIR.exists():
        shutil.copy2(os.path.join(out_dir, "hook_cover.jpg"), ARTIFACT_DIR / f"{arch_id}_cover_1080p.jpg")
        shutil.copy2(os.path.join(out_dir, "kombin_collage.png"), ARTIFACT_DIR / f"{arch_id}_collage_1080p.png")

    old_reel_final = os.path.join(out_dir, "reel_final.mp4")
    if os.path.exists(old_reel_final):
        try:
            os.remove(old_reel_final)
        except Exception:
            pass

    # 1) Broadcast to Telegram (@guzelaibot)
    tg_res = publish_to_telegram(outfit, out_dir=out_dir, video_override=mp4_path)
    print(f"📲 [Telegram @guzelaibot Sonucu]: {tg_res}")

    # 2) Publish to GuzelAI.com Website (#kombinler & /go/{sku})
    web_res = publish_to_guzelai_website(outfit, out_dir=out_dir)
    print(f"🌐 [GuzelAI.com Web Vitrin Sonucu]: {web_res.get('status', 'ok')}")

    # 3) Publish to Pinterest
    pin_res = publish_to_pinterest_cdp(outfit, Path(out_dir) / "kombin_collage.png")
    print(f"📌 [Pinterest Pin Sonucu]: {pin_res}")

    mark_creation_and_model_used(
        arch_id,
        (outfit.get("model_frames") or [""])[0],
        telegram_sent=True,
    )
    return {
        "arch_id": arch_id,
        "guzelai_model": outfit.get("guzelai_model_badge"),
        "flow_walk_engine": outfit.get("flow_walk_engine"),
        "flow_walk_video": outfit.get("flow_walk_video"),
        "telegram": tg_res,
        "pinterest": pin_res,
    }


if __name__ == "__main__":
    target_ids = sys.argv[1:] or [
        "kadin_guzelai_leyla_om01_camel_kasmir_cikolata",
        "erkek_guzelai_kenzo_om01_camel_kase_kronograf",
    ]
    results = []
    for tid in target_ids:
        results.append(process_and_publish_single(tid))
    print("\n✅ TÜM 1080p HİBRİT (KOMBİN KOLAJI + GOOGLE FLOW YÜRÜYÜŞ) YAYINLARI TAMAMLANDI:")
    print(json.dumps(results, ensure_ascii=False, indent=2))
