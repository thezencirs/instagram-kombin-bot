"""
Continuous Multi-Agent Google Flow 1080p + Kombin Collage Hybrid Production & Publishing Daemon
(`src/continuous_flow_kombin_daemon.py`)
===============================================================================================
Coordinates the GüzelAI Holding Multi-Agent Fashion Design & Cinema Council:
1. Ajan 1 (Moda Tasarım Konseyi — HALUK, FERİDE, DEFNE, KEREM, LEYLA, MERT):
   - Selects the next unshared official `guzelai.com` model archetype or synthesizes a brand-new
     seasonal / Old Money / Quiet Luxury / Sprezzatura 6-piece creation across `kadin`, `erkek`,
     `kiz_cocuk`, and `erkek_cocuk`.
2. Ajan 2 (Cinsiyet & Resmi Manken Başdenetçisi — KADİR & VERA):
   - Enforces 100% official `guzelai.com` model roster lock (`enforce_guzelai_official_model_lock`)
     and zero-tolerance gender compliance (`inspect_and_enforce_gender_compliance`).
3. Ajan 3 (Google Flow 1080p Yürüyüş Sinema Ajanları — KUZEY & ATLAS):
   - Connects to Google Flow (`https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88`),
     uploads the `guzelai.com` model's `step1.jpg` reference photo, and generates a real 1080p
     walking video (`assets/{arch_id}_flow_walk.mp4`).
4. Ajan 4 (1080p Hibrit Birleştirme & Kurgu Ajanı — KORAY):
   - Merges Part 1 (0.0s–5.2s: 6-Piece Kombin Collage with `#1..#6` cutouts & brand/price tags)
     + Part 2 (5.2s–11.0s: Real 1080p Google Flow Walking Video) into a single 1080x1920 @ 30fps
     Master Reel (`output/daily_kombin_reel.mp4`).
5. Ajan 5 (Çok Kanallı Yayın & Algoritma Isınma Ajanları — EMİR, SEDA, BARIŞ):
   - Publishes to Telegram (`@guzelaibot`), `guzelai.com` (`#kombinler`), Pinterest, and (when within
     safe daily cadence) Instagram (`@guzelaicom` via `ig_chrome_trusted` + Pre-Publish Human Browsing).
"""

import argparse
import datetime
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from autonomous_creation_factory import (
    is_creation_or_model_used,
    load_zero_repeat_ledger,
    mark_creation_and_model_used,
    synthesize_autonomous_winter_creation,
)
from fashion_agenda_engine import enrich_outfit_with_fashion_agenda
from gender_style_guardrail import (
    inspect_and_enforce_gender_compliance,
    run_fashion_design_council_session,
)
from google_flow_kombin_walker import ensure_realistic_flow_walk_video
from guzelai_official_models import enforce_guzelai_official_model_lock
from instagram_safe_publisher import upload_via_single_trusted_chrome_cdp
from main import build_caption, build_links_comment
from outfit_generator import OUTFIT_ARCHETYPES, _format_price_tr
from pinterest_publisher import publish_to_pinterest_cdp, save_pinterest_outputs
from publish_guzelai_flow_hybrid_batch import build_outfit_from_arch_id
from render_reels import render_kombin_reel
from telegram_publisher import publish_to_telegram, save_telegram_outputs
from website_publisher import publish_to_guzelai_website

DAEMON_LOG_PATH = BASE_DIR / "output" / "continuous_flow_daemon_log.json"
SEGMENT_ROTATION = ["kadin", "erkek", "kiz_cocuk", "erkek_cocuk"]


def pick_or_synthesize_next_outfit(preferred_segment: Optional[str] = None) -> Dict[str, Any]:
    """
    Ajan 1 (Moda Tasarım Konseyi):
    1. Checks unshared archetypes in `OUTFIT_ARCHETYPES` first (checking both `zero_repeat_ledger.json`
       and `output/telegram_sent_history.json`).
    2. If all static archetypes are already used, calls
       `synthesize_autonomous_winter_creation` to create a brand-new official `guzelai.com`
       model outfit & 6 studio cutouts.
    """
    ledger = load_zero_repeat_ledger()
    tg_hist_path = BASE_DIR / "output" / "telegram_sent_history.json"
    tg_sent_ids = set(ledger.get("telegram_dispatched_ids", []))
    if tg_hist_path.exists():
        try:
            tg_obj = json.loads(tg_hist_path.read_text(encoding="utf-8"))
            tg_sent_ids.update(tg_obj.get("sent_archetypes", []))
        except Exception:
            pass

    for arch in OUTFIT_ARCHETYPES:
        if preferred_segment and arch.get("gender_segment") != preferred_segment:
            continue
        if arch["id"] not in tg_sent_ids and not is_creation_or_model_used(arch, ledger):
            return build_outfit_from_arch_id(arch["id"])

    for arch in OUTFIT_ARCHETYPES:
        if arch["id"] not in tg_sent_ids and not is_creation_or_model_used(arch, ledger):
            return build_outfit_from_arch_id(arch["id"])

    seg = preferred_segment or SEGMENT_ROTATION[int(time.time() // 3600) % len(SEGMENT_ROTATION)]
    new_arch = synthesize_autonomous_winter_creation(target_segment=seg, zero_ledger=ledger)
    OUTFIT_ARCHETYPES.insert(0, new_arch)
    return build_outfit_from_arch_id(new_arch["id"])


def run_single_multi_agent_flow_hybrid_cycle(
    arch_id: Optional[str] = None,
    preferred_segment: Optional[str] = None,
    try_instagram: bool = True,
) -> Dict[str, Any]:
    out_dir = str(BASE_DIR / "output")
    os.makedirs(out_dir, exist_ok=True)
    os.environ["REEL_RES_MODE"] = "1080p"

    # 1) Ajan 1 & Ajan 2: Moda Tasarım Konseyi + Resmi Manken & Cinsiyet Kilidi
    if arch_id:
        outfit = build_outfit_from_arch_id(arch_id)
    else:
        outfit = pick_or_synthesize_next_outfit(preferred_segment=preferred_segment)

    active_id = outfit["archetype_id"]
    print(f"\n======================================================================")
    print(f"🤖 [AJAN KONSEYİ ORKESTRASYONU BAŞLADI]: {active_id}")
    print(f"👤 Resmi GuzelAI.com Mankeni: {outfit.get('guzelai_model_badge')}")
    print(f"🏛️ Tasarım Konseyi Kararı: {outfit.get('council_summary_line', 'Onaylandı')}")
    print(f"======================================================================")

    # 2) Ajan 3: Google Flow 1080p Gerçekçi Yürüyüş Videosu Üretimi
    walk_mp4 = ensure_realistic_flow_walk_video(outfit, out_dir=out_dir)

    # 3) Ajan 4: 1080p Hibrit Birleştirme (0-5.2s 6 Parçalı Kombin Kolajı + 5.2-11.0s Flow Yürüyüş)
    mp4_path = os.path.join(out_dir, "daily_kombin_reel.mp4")
    old_reel_final = os.path.join(out_dir, "reel_final.mp4")
    if os.path.exists(old_reel_final):
        try:
            os.remove(old_reel_final)
        except Exception:
            pass

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

    # 4) Ajan 5: Çok Kanallı Yayın (Telegram @guzelaibot, GuzelAI.com, Pinterest, Instagram Safe CDP)
    tg_res = publish_to_telegram(outfit, out_dir=out_dir, video_override=mp4_path)
    web_res = publish_to_guzelai_website(outfit, out_dir=out_dir)
    pin_res = publish_to_pinterest_cdp(outfit, Path(out_dir) / "kombin_collage.png")

    ig_res = {"status": "skipped"}
    if try_instagram:
        try:
            ig_res = upload_via_single_trusted_chrome_cdp(
                video_path=mp4_path,
                caption=caption,
            )
        except Exception as ig_e:
            ig_res = {"status": "error", "reason": str(ig_e)}

    mark_creation_and_model_used(
        active_id,
        (outfit.get("model_frames") or [""])[0],
        telegram_sent=True,
    )

    cycle_report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "archetype_id": active_id,
        "gender_segment": outfit.get("gender_segment"),
        "guzelai_model": outfit.get("guzelai_model_badge"),
        "flow_walk_video": walk_mp4,
        "flow_walk_engine": outfit.get("flow_walk_engine", "google_flow_ultra_1080p"),
        "merged_hybrid_reel": mp4_path,
        "telegram": tg_res.get("status") if isinstance(tg_res, dict) else ("published" if tg_res else "failed"),
        "website": web_res.get("status") if isinstance(web_res, dict) else ("published" if web_res else "failed"),
        "pinterest": pin_res.get("status") if isinstance(pin_res, dict) else ("published" if pin_res else "failed"),
        "instagram": ig_res.get("status"),
        "instagram_detail": ig_res,
    }

    try:
        history = []
        if DAEMON_LOG_PATH.exists():
            history = json.loads(DAEMON_LOG_PATH.read_text(encoding="utf-8"))
        history.append(cycle_report)
        DAEMON_LOG_PATH.write_text(json.dumps(history[-100:], ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

    return cycle_report


def run_continuous_daemon_loop(interval_minutes: int = 90, max_cycles: int = 1000) -> None:
    print(f"🚀 [GÜZELAI HOLDİNG SÜREKLİ FLOW + KOMBİN HİBRİT AJAN DAEMONU] Başlatıldı (Aralık: {interval_minutes} dk)")
    for cycle_idx in range(1, max_cycles + 1):
        seg = SEGMENT_ROTATION[(cycle_idx - 1) % len(SEGMENT_ROTATION)]
        try:
            rep = run_single_multi_agent_flow_hybrid_cycle(preferred_segment=seg, try_instagram=True)
            print(f"✅ [Döngü #{cycle_idx} Tamamlandı]: {json.dumps(rep, ensure_ascii=False)}")
        except Exception as err:
            print(f"⚠️ [Döngü #{cycle_idx} Uyarısı]: {err}")
        time.sleep(max(60, interval_minutes * 60))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch-id", default="", help="Belirli bir arketip ID üret ve yayınla")
    parser.add_argument("--batch", nargs="*", help="Birden fazla arketip ID sırayla üret ve yayınla")
    parser.add_argument("--daemon", action="store_true", help="7/24 kesintisiz sürekli üretim döngüsünü başlat")
    parser.add_argument("--interval-min", type=int, default=90, help="Daemon üretim aralığı (dakika)")
    parser.add_argument("--no-ig", action="store_true", help="Instagram adımını atla")
    args = parser.parse_args()

    if args.batch:
        out_list = []
        for aid in args.batch:
            out_list.append(run_single_multi_agent_flow_hybrid_cycle(arch_id=aid, try_instagram=not args.no_ig))
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
    elif args.arch_id:
        rep = run_single_multi_agent_flow_hybrid_cycle(arch_id=args.arch_id, try_instagram=not args.no_ig)
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    elif args.daemon:
        run_continuous_daemon_loop(interval_minutes=args.interval_min)
    else:
        rep = run_single_multi_agent_flow_hybrid_cycle(try_instagram=not args.no_ig)
        print(json.dumps(rep, ensure_ascii=False, indent=2))
