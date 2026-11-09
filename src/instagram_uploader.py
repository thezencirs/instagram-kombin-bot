import os
import sys
import re
import json
import time
import argparse
from pathlib import Path
from urllib.parse import unquote
import requests
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def upload_via_graph_api(video_path: str, caption: str, access_token: str, ig_user_id: str) -> bool:
    print("[Instagram Graph API] Video geçici bulut bağlantısına yükleniyor...")
    with open(video_path, "rb") as f:
        up_resp = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f}, timeout=60)
    up_resp.raise_for_status()
    raw_url = up_resp.json()["data"]["url"].replace("tmpfiles.org/", "tmpfiles.org/dl/")

    create_url = f"https://graph.facebook.com/v19.0/{ig_user_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": raw_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": access_token,
    }
    r = requests.post(create_url, data=payload, timeout=30)
    r.raise_for_status()
    creation_id = r.json()["id"]
    print(f"[Instagram Graph API] Medya konteyneri oluşturuldu: {creation_id}, işlenmesi bekleniyor...")

    for _ in range(18):
        time.sleep(10)
        status_r = requests.get(
            f"https://graph.facebook.com/v19.0/{creation_id}",
            params={"fields": "status_code", "access_token": access_token},
            timeout=20,
        )
        status_code = status_r.json().get("status_code")
        print(f"  -> Durum: {status_code}")
        if status_code == "FINISHED":
            break
        if status_code == "ERROR":
            raise RuntimeError(f"Instagram medya işleme hatası: {status_r.text}")

    pub_r = requests.post(
        f"https://graph.facebook.com/v19.0/{ig_user_id}/media_publish",
        data={"creation_id": creation_id, "access_token": access_token},
        timeout=30,
    )
    pub_r.raise_for_status()
    print(f"[BAŞARILI] Instagram Reels yayınlandı! Media ID: {pub_r.json().get('id')}")
    return True


def _pull_remote_history_if_newer(local_file: Path, repo_rel_path: str):
    """Bulut (GitHub Actions) paylaşım yaptığında yerel PC'nin haberdar olması için uzak geçmişi senkronize eder."""
    if (
        os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
        or os.environ.get("LOCAL_ONLY", "0") == "1"
        or os.environ.get("DISABLE_GITHUB_SYNC", "0") == "1"
    ):
        return
    try:
        url = f"https://raw.githubusercontent.com/thezencirs/instagram-kombin-bot/main/{repo_rel_path}?t={int(time.time())}"
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            remote_data = r.json()
            if not local_file.exists():
                local_file.parent.mkdir(parents=True, exist_ok=True)
                local_file.write_text(json.dumps(remote_data, ensure_ascii=False, indent=2), encoding="utf-8")
                return
            local_data = json.loads(local_file.read_text(encoding="utf-8"))
            if isinstance(remote_data, dict) and isinstance(local_data, dict):
                rem_ts = float(remote_data.get("last_upload_timestamp", 0.0) or 0.0)
                loc_ts = float(local_data.get("last_upload_timestamp", 0.0) or 0.0)
                if rem_ts > loc_ts:
                    local_file.write_text(json.dumps(remote_data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _sync_history_file_to_github_repo(local_file: Path, repo_rel_path: str):
    """Yerel PC paylaşım yaptığında GitHub Actions bulut yedeklemesinin haberdar olması için geçmişi depoya yazar."""
    if (
        os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
        or os.environ.get("LOCAL_ONLY", "0") == "1"
        or os.environ.get("DISABLE_GITHUB_SYNC", "0") == "1"
        or not local_file.exists()
    ):
        return
    try:
        import base64
        import shutil
        import subprocess

        gh_exe = r"C:\Users\zenci\.gemini\antigravity\scratch\tools\gh\bin\gh.exe"
        if not os.path.exists(gh_exe):
            gh_exe = shutil.which("gh") or "gh"
        repo = "thezencirs/instagram-kombin-bot"
        sha = ""
        r_get = subprocess.run(
            [gh_exe, "api", f"repos/{repo}/contents/{repo_rel_path}", "--jq", ".sha"],
            capture_output=True,
            text=True,
            timeout=12,
        )
        if r_get.returncode == 0 and r_get.stdout.strip():
            sha = r_get.stdout.strip()
        b64 = base64.b64encode(local_file.read_bytes()).decode("ascii")
        cmd = [
            gh_exe,
            "api",
            "--method",
            "PUT",
            f"repos/{repo}/contents/{repo_rel_path}",
            "-f",
            f"message=chore(sync): update {repo_rel_path} after local upload [skip ci]",
            "-f",
            f"content={b64}",
        ]
        if sha:
            cmd.extend(["-f", f"sha={sha}"])
        subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except Exception:
        pass


def upload_via_instagrapi(
    video_path: str,
    caption: str,
    username: str,
    password: str = "",
    session_str: str = "",
    comment_text: str = "",
) -> str:
    """
    [KALICI OLARAK EMEKLİ EDİLDİ -> SIFIR-İHLAL MOTORUNA YÖNLENDİRİLDİ]
    Resmi olmayan `instagrapi` kütüphanesi (sahte Samsung SM-S918B Android emülasyonu)
    'otomatik davranış' ve 'farklı cihazdan giriş' uyarılarına yol açmaması için %100 kaldırılmıştır.
    Tüm çağrılar `instagram_safe_publisher.publish_instagram_zero_violation` motoruna yönlendirilir.
    """
    try:
        from instagram_safe_publisher import publish_instagram_zero_violation
        return publish_instagram_zero_violation(video_path=video_path, caption=caption)
    except Exception as exc:
        print(f"[Sıfır-İhlal Instagram Motoru Bilgilendirmesi] {exc}")
        return ""



def dispatch_all_channels(video_path: str, reel_url: str = ""):
    """Dispatches and publishes to GuzelAI.com showcase and Telegram Bot (@guzelaibot) in Telegram Stock Mode."""
    out_dir = str(Path(video_path).parent)
    meta_path = os.path.join(out_dir, "outfit_links.json")
    hook_cover_candidate = Path(video_path).parent / "hook_cover.jpg"
    collage_candidate = hook_cover_candidate if hook_cover_candidate.exists() else (Path(video_path).parent / "kombin_collage.png")
    outfit_data = {}
    telegram_only = os.environ.get("TELEGRAM_ONLY_MODE", "1") == "1"

    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as mf:
            outfit_data = json.load(mf)
        if reel_url:
            outfit_data["reel_url"] = reel_url
            with open(meta_path, "w", encoding="utf-8") as mf:
                json.dump(outfit_data, mf, ensure_ascii=False, indent=2)

    # 1. GuzelAI.com (#kombinler & /go/{sku}) e-ticaret link doğrulama ve görselli vitrin yayını
    # (Telegram'dan indirip kanallara yüklediğinizde ürün linklerinin çalışması için vitrin güncellenir)
    try:
        from website_publisher import publish_to_guzelai_website
        web_res = publish_to_guzelai_website(
            outfit_data,
            collage_path=collage_candidate,
            ig_reel_url=reel_url,
            out_dir=out_dir,
        )
        print(f"[GuzelAI.com Görselli Link Vitrini] Durum: {web_res}")
    except Exception as webe:
        print(f"[GuzelAI.com Vitrin Bilgilendirmesi] {webe}")

    # 2. Ajan 15 (LİA) 1080x1920 Pinterest Moda Tasarım Kolajını üret ve Pinterest oturumu aktifse doğrudan Pin yayınla
    try:
        from kombin_agent_swarm import run_pinterest_collage_fashion_designer
        from pinterest_publisher import (
            PINTEREST_PROFILE_DIR,
            publish_to_pinterest_cdp,
            save_pinterest_outputs,
        )
        lia_rep = run_pinterest_collage_fashion_designer()
        lia_collage = Path(lia_rep.get("collage_path", str(Path(out_dir) / "pinterest_fashion_collage.jpg")))
        save_pinterest_outputs(outfit_data, out_dir=out_dir, reel_url=reel_url)
        print(f"[LİA Pinterest Kolajı Hazır] {lia_collage}")
        if PINTEREST_PROFILE_DIR.exists() and os.environ.get("DISABLE_PINTEREST_AUTO_PUBLISH", "0") != "1":
            pin_media = lia_collage if lia_collage.exists() else (Path(out_dir) / "kombin_collage.png")
            pin_res = publish_to_pinterest_cdp(outfit_data, pin_media, reel_url=reel_url)
            print(f"[Pinterest Otomatik Pin Paylaşımı] Durum: {pin_res}")
    except Exception as pne:
        print(f"[Pinterest Kolaj & Paylaşım Bilgilendirmesi] {pne}")

    # 3. Diğer platform metin şablonlarını yerel dosyaya kaydet (otomatik yükleme yapmadan)
    try:
        from threads_publisher import save_threads_outputs
        from youtube_publisher import save_youtube_outputs
        from x_publisher import save_x_outputs
        from facebook_publisher import save_facebook_outputs
        from whatsapp_publisher import save_whatsapp_outputs
        from tiktok_uploader import save_tiktok_outputs
        save_threads_outputs(outfit_data, out_dir=out_dir, reel_url=reel_url)
        save_youtube_outputs(outfit_data, out_dir=out_dir, reel_url=reel_url)
        save_x_outputs(outfit_data, out_dir=out_dir, reel_url=reel_url)
        save_facebook_outputs(outfit_data, out_dir=out_dir, ig_reel_url=reel_url)
        save_whatsapp_outputs(outfit_data, out_dir=out_dir, ig_reel_url=reel_url)
        save_tiktok_outputs(outfit_data, out_dir=out_dir, ig_reel_url=reel_url)
    except Exception as txe:
        print(f"[Metin Şablon Hazırlık Bilgilendirmesi] {txe}")

    # 4. Telegram botunda (@guzelaibot) TAM STOK PAKETİ (2K Video + Kapak + LİA Pinterest Kolajı + Kopyala-Yapıştır Açıklama & Linkler) paylaşımı
    try:
        from telegram_publisher import publish_to_telegram
        tg_res = publish_to_telegram(
            outfit_data,
            out_dir=out_dir,
            reel_url=reel_url,
            video_override=video_path,
        )
        print(f"[Telegram (@guzelaibot) Stok Paketi Gönderimi] Durum: {tg_res}")
    except Exception as tge:
        print(f"[Telegram Paylaşım Bilgilendirmesi] {tge}")

    if telegram_only:
        print(
            "[TELEGRAM STOK MODU AKTİF] Tüm içerikler (2K Reels Video, Hook Kapak, LİA Pinterest Kolajı, "
            "Kopyala-Yapıştır Açıklama ve guzelai.com/go mağaza linkleri) yalnızca @guzelaibot üzerinden "
            "Telegram'a iletildi. Doğrudan sosyal medya yüklemeleri devre dışıdır."
        )
        return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="Yüklenecek MP4 dosyası")
    parser.add_argument("--caption-file", required=True, help="Açıklama metni dosyası")
    parser.add_argument(
        "--all-channels",
        action="store_true",
        help="Telegram stok paketini ve vitrin linklerini hazırla",
    )
    args = parser.parse_args()

    cooldown_flag = Path(args.video).parent / "skip_cooldown_active.flag"
    if cooldown_flag.exists():
        print("🛡️ [BULUT ÇİFT TETİKLEME KORUMASI] Cooldown bayrağı aktif; mükerrer kanal gönderimi güvenle atlandı.")
        return

    reel_url = ""
    if os.environ.get("GITHUB_ACTIONS", "").lower() != "true" and os.environ.get("DISABLE_IG_SAFE_PUBLISHER", "0") != "1":
        try:
            with open(args.caption_file, "r", encoding="utf-8") as f:
                caption = f.read().strip()
            from instagram_safe_publisher import publish_instagram_zero_violation
            reel_url = publish_instagram_zero_violation(args.video, caption) or ""
        except Exception as ig_exc:
            print(f"[Sıfır-İhlal Instagram Motoru Bilgilendirmesi] {ig_exc}")
    else:
        print(
            "[BULUT / TELEGRAM KORUMA MODU AKTİF] Yabancı IP / Bot kısıtlama koruması devrede: "
            "Instagram'a hiçbir dış IP isteği gönderilmiyor, yalnızca Telegram (@guzelaibot) ve vitrin güncelleniyor."
        )

    dispatch_all_channels(args.video, reel_url=reel_url)


if __name__ == "__main__":
    main()
