"""
GuzelAI 18 Ajanlı (İK Direktörü İREM + 1:1 Görsel Başdenetçisi SARP Onaylı)
%100 Birebir Model-Üst Giyim Uyumlu Telegram Stok Üretim Hattı
"""
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(BASE_DIR)
sys.path.insert(0, str(BASE_DIR / "src"))

os.environ["TELEGRAM_ONLY_MODE"] = "1"
os.environ["IG_ENABLE_UPLOAD"] = "0"

from kombin_agent_swarm import run_hr_agent_trainer_director, run_visual_1to1_match_inspector, run_dispatcher_reporter
import main as main_mod
from instagram_uploader import dispatch_all_channels

# İK & SARP tarafından %100 1:1 model-kıyafet (Kadın, Erkek, Kız Çocuk, Erkek Çocuk) uyumu doğrulanan stok listesi:
VERIFIED_1TO1_STOCK_QUEUE = [
    ("stok_1to1_erkek_cocuk_kolej", "cocuk_erkek_slot1_sonbahar_kolej_street"),
    ("stok_1to1_kiz_cocuk_kolej", "cocuk_slot1_sonbahar_kolej_kombin"),
    ("stok_1to1_erkek_oldmoney", "erkek_slot1_sonbahar_oldmoney_kapsul"),
    ("stok_1to1_erkek_streetwear", "erkek_slot2_streetwear_bomber_samba"),
]


def run_stock_batch():
    print("👩‍💼 [Ajan 17 - İREM & Ajan 18 - SARP] İK Denetimi ve 1:1 Manken-Kombin Görsel Eşleşme Kontrolü Başlatılıyor...")
    v_report = run_visual_1to1_match_inspector()
    hr_report = run_hr_agent_trainer_director()
    run_dispatcher_reporter()

    if not v_report.get("live_scrape_random_override_blocked"):
        raise RuntimeError("KRİTİK HATA: force_live_scrape kilidi aktif değil! Stok üretimi durduruldu.")

    for idx, (slot_label, arch_id) in enumerate(VERIFIED_1TO1_STOCK_QUEUE, start=1):
        print(f"\n==================================================================")
        print(f"📦 [1:1 DOĞRULANMIŞ 4-SEGMENT TELEGRAM STOK PAKETİ {idx}/{len(VERIFIED_1TO1_STOCK_QUEUE)}] {arch_id}")
        print(f"==================================================================")
        os.environ["FORCE_ARCHETYPE_ID"] = arch_id
        os.environ["SLOT_NAME"] = slot_label
        os.environ["TELEGRAM_ONLY_MODE"] = "1"
        os.environ["IG_ENABLE_UPLOAD"] = "0"
        sys.argv = ["main.py", "--output", "output/daily_kombin_reel.mp4"]
        main_mod.main()
        dispatch_all_channels("output/daily_kombin_reel.mp4", reel_url="")

    print("\n✅ [TAMAMLANDI] Tüm 1:1 model-üst giyim uyumlu stok paketleri @guzelaibot'a iletildi!")


if __name__ == "__main__":
    run_stock_batch()
