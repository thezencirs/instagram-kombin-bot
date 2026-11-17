"""
Continuous Multi-Agent 2K 9:16 Vertical Kombin Production & Safe Publishing Daemon
(`src/continuous_flow_kombin_daemon.py`)
===================================================================================
Not: Google Flow (`flow.google.com`) kullanıcı talimatıyla %100 devre dışı bırakılmıştır.
Tüm fotoğraf ve videolar %100 dikey 9:16 (1440x2560 2K QHD+) Remotion yay fiziği ve
3 adımlı Hasselblad 85mm f/1.4 gimbal yürüyüş motoru ile üretilir.
"""

import argparse
import datetime
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

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
from instagram_safe_publisher import upload_via_single_trusted_chrome_cdp
from main import build_caption, build_links_comment
from outfit_generator import OUTFIT_ARCHETYPES
from pinterest_publisher import publish_to_pinterest_cdp, save_pinterest_outputs
from publish_guzelai_flow_hybrid_batch import build_outfit_from_arch_id
from render_reels import render_kombin_reel
from telegram_publisher import publish_to_telegram, save_telegram_outputs
from vertical_media_guard import ensure_vertical_photo, ensure_vertical_video
from website_publisher import publish_to_guzelai_website

DAEMON_LOG_PATH = BASE_DIR / "output" / "continuous_vertical_daemon_log.json"
SEGMENT_ROTATION = ["kadin", "erkek", "kiz_cocuk", "erkek_cocuk"]


def _has_verified_vertical_assets(arch: Dict[str, Any]) -> bool:
    mfs = arch.get("model_frames") or []
    cas = list((arch.get("cutout_assets") or {}).values())
    if len(mfs) < 2 or len(cas) < 6:
        return False
    return all((BASE_DIR / p).exists() for p in mfs) and all((BASE_DIR / p).exists() for p in cas)


def pick_or_synthesize_next_outfit(preferred_segment: Optional[str] = None) -> Dict[str, Any]:
    ledger = load_zero_repeat_ledger()
    tg_hist_path = BASE_DIR / "output" / "telegram_sent_history.json"
    tg_sent_ids = set(ledger.get("telegram_dispatched_ids", []))
    if tg_hist_path.exists():
        try:
            tg_obj = json.loads(tg_hist_path.read_text(encoding="utf-8"))
            tg_sent_ids.update(tg_obj.get("sent_archetypes", []))
        except Exception:
            pass

    recent_models = []
    if DAEMON_LOG_PATH.exists():
        try:
            d_hist = json.loads(DAEMON_LOG_PATH.read_text(encoding="utf-8"))
            if isinstance(d_hist, list):
                recent_models = [str(x.get("guzelai_model") or "") for x in d_hist[-3:]]
        except Exception:
            pass

    # 1. Önce son kullanılan mankenden farklı olan, tüm 9:16 dikey fotoğrafları ve 6 dekupesi doğrulanmış özgün kombini seç
    for avoid_recent in (True, False):
        for arch in OUTFIT_ARCHETYPES:
            if preferred_segment and arch.get("gender_segment") != preferred_segment:
                continue
            if arch["id"] not in tg_sent_ids and not is_creation_or_model_used(arch, ledger) and _has_verified_vertical_assets(arch):
                badge = str(arch.get("guzelai_model_badge") or "")
                if avoid_recent and badge and badge in recent_models[-1:]:
                    continue
                return build_outfit_from_arch_id(arch["id"])

        for arch in OUTFIT_ARCHETYPES:
            if arch["id"] not in tg_sent_ids and not is_creation_or_model_used(arch, ledger) and _has_verified_vertical_assets(arch):
                badge = str(arch.get("guzelai_model_badge") or "")
                if avoid_recent and badge and badge in recent_models[-1:]:
                    continue
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
    os.environ["REEL_RES_MODE"] = "2k"
    os.environ["USE_GOOGLE_FLOW_CDP"] = "0"
    os.environ["DISABLE_GOOGLE_FLOW"] = "1"

    outfit = build_outfit_from_arch_id(arch_id) if arch_id else pick_or_synthesize_next_outfit(preferred_segment=preferred_segment)
    outfit.pop("flow_walk_video", None)
    outfit["walk_engine"] = "remotion_2k_vertical_9x16_gimbal"

    active_id = outfit["archetype_id"]
    print("\n======================================================================")
    print(f"🤖 [2K 9:16 DİKEY KOMBİN ORKESTRASYONU BAŞLADI (SIFIR FLOW)]: {active_id}")
    print(f"👤 Resmi GuzelAI.com Mankeni: {outfit.get('guzelai_model_badge')}")
    print("======================================================================")

    mp4_path = os.path.join(out_dir, "daily_kombin_reel.mp4")
    old_reel_final = os.path.join(out_dir, "reel_final.mp4")
    if os.path.exists(old_reel_final):
        try:
            os.remove(old_reel_final)
        except Exception:
            pass

    render_kombin_reel(outfit, mp4_path, watermark="@guzelaicom")
    safe_mp4_path, vid_w, vid_h = ensure_vertical_video(mp4_path)
    mp4_path = str(safe_mp4_path)
    ensure_vertical_photo(Path(out_dir) / "hook_cover.jpg")
    ensure_vertical_photo(Path(out_dir) / "kombin_collage.png")
    ensure_vertical_photo(Path(out_dir) / "pinterest_fashion_collage.jpg")

    caption = build_caption(outfit)
    links_comment = build_links_comment(outfit)
    with open(os.path.join(out_dir, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(caption + "\n")
    with open(os.path.join(out_dir, "pinned_comment.txt"), "w", encoding="utf-8") as f:
        f.write(links_comment + "\n")
    with open(os.path.join(out_dir, "outfit_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(outfit, f, ensure_ascii=False, indent=2)
    with open(os.path.join(out_dir, "outfit_links.json"), "w", encoding="utf-8") as f:
        json.dump(outfit, f, ensure_ascii=False, indent=2)

    save_telegram_outputs(outfit, out_dir=out_dir)
    save_pinterest_outputs(outfit, out_dir=out_dir)

    tg_res = publish_to_telegram(outfit, out_dir=out_dir, video_override=mp4_path)
    web_res = publish_to_guzelai_website(outfit, out_dir=out_dir)
    pin_res = publish_to_pinterest_cdp(outfit, Path(out_dir) / "kombin_collage.png")

    ig_res: Dict[str, Any] = {"status": "skipped"}
    if try_instagram:
        try:
            ig_res = upload_via_single_trusted_chrome_cdp(video_path=mp4_path, caption=caption)
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
        "video_engine": "remotion_2k_vertical_9x16_gimbal",
        "video_dimensions": f"{vid_w}x{vid_h}",
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


def run_continuous_daemon_loop(interval_minutes: int = 240, max_cycles: int = 1000) -> None:
    print(f"🚀 [GÜZELAI 2K 9:16 DİKEY KOMBİN GÜVENLİ DAEMONU (SIFIR FLOW)] Başlatıldı (Aralık: {interval_minutes} dk)")
    for cycle_idx in range(1, max_cycles + 1):
        seg = SEGMENT_ROTATION[(cycle_idx - 1) % len(SEGMENT_ROTATION)]
        try:
            rep = run_single_multi_agent_flow_hybrid_cycle(preferred_segment=seg, try_instagram=True)
            print(f"✅ [Döngü #{cycle_idx} Tamamlandı]: {json.dumps(rep, ensure_ascii=False)}")
        except Exception as err:
            print(f"⚠️ [Döngü #{cycle_idx} Uyarısı]: {err}")
        time.sleep(max(300, interval_minutes * 60))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch-id", default="", help="Belirli bir arketip ID üret ve yayınla")
    parser.add_argument("--batch", nargs="*", help="Birden fazla arketip ID sırayla üret ve yayınla")
    parser.add_argument("--daemon", action="store_true", help="Güvenli üretim döngüsünü başlat")
    parser.add_argument("--interval-min", type=int, default=240, help="Daemon üretim aralığı (dakika)")
    parser.add_argument("--no-ig", action="store_true", help="Instagram adımını atla")
    args = parser.parse_args()

    if args.batch:
        out_list = [run_single_multi_agent_flow_hybrid_cycle(arch_id=aid, try_instagram=not args.no_ig) for aid in args.batch]
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
    elif args.arch_id:
        print(json.dumps(run_single_multi_agent_flow_hybrid_cycle(arch_id=args.arch_id, try_instagram=not args.no_ig), ensure_ascii=False, indent=2))
    elif args.daemon:
        run_continuous_daemon_loop(interval_minutes=args.interval_min)
    else:
        print(json.dumps(run_single_multi_agent_flow_hybrid_cycle(try_instagram=not args.no_ig), ensure_ascii=False, indent=2))
