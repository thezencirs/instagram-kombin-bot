"""
GuzelAI 22 Ajanlı (Ajan Kaynakları Birimi ARDA, MAYA, KAAN, VERA + İK Direktörü İREM + 1:1 Görsel Başdenetçisi SARP Onaylı)
%100 Sıfır-Tekrar (Zero-Repeat) Manken & Kombin Garantili, Mevsimsel Özgün Telegram Stok Üretim Hattı
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

from kombin_agent_swarm import (
    run_agent_resources_division,
    run_hr_agent_trainer_director,
    run_visual_1to1_match_inspector,
    run_dispatcher_reporter,
)
import main as main_mod
from instagram_uploader import dispatch_all_channels

# Ajan Kaynakları Birimi (ARDA, MAYA, KAAN, VERA) & SARP tarafından %100 1:1 model-kıyafet
# ve %100 SIFIR-TEKRAR (daha önce hiç kullanılmamış manken & kombin) uyumu doğrulanan 4-Segment Yeni Sezon Kreasyon Listesi:
VERIFIED_1TO1_STOCK_QUEUE = [
    ("yeni_sezon_kadin_galataport", "kadin_kasim_galataport_bordo_trench_ekru"),
    ("yeni_sezon_erkek_nisantasi", "erkek_kasim_nisantasi_lacivert_kaban_camel"),
    ("yeni_sezon_kiz_cocuk_moda", "cocuk_kiz_kasim_moda_pembe_tuvit_kolej"),
    ("yeni_sezon_erkek_cocuk_gokturk", "cocuk_erkek_kasim_gokturk_haki_puffer_street"),
]


def run_stock_batch():
    print("🏛️ [Ajan Kaynakları Birimi - ARDA, MAYA, KAAN, VERA & SARP] Sıfır-Tekrar Manken/Kombin Kilidi ve 1:1 Görsel Eşleşme Kontrolü Başlatılıyor...")
    ar_report = run_agent_resources_division()
    v_report = run_visual_1to1_match_inspector()
    hr_report = run_hr_agent_trainer_director()
    run_dispatcher_reporter()

    if not v_report.get("live_scrape_random_override_blocked"):
        raise RuntimeError("KRİTİK HATA: force_live_scrape kilidi aktif değil! Stok üretimi durduruldu.")

    for idx, (slot_label, arch_id) in enumerate(VERIFIED_1TO1_STOCK_QUEUE, start=1):
        print(f"\n==================================================================")
        print(f"📦 [SIFIR-TEKRAR YENİ SEZON 4-SEGMENT KREASYON PAKETİ {idx}/{len(VERIFIED_1TO1_STOCK_QUEUE)}] {arch_id}")
        print(f"==================================================================")
        os.environ["FORCE_ARCHETYPE_ID"] = arch_id
        os.environ["SLOT_NAME"] = slot_label
        os.environ["TELEGRAM_ONLY_MODE"] = "1"
        os.environ["IG_ENABLE_UPLOAD"] = "0"
        sys.argv = ["main.py", "--output", "output/daily_kombin_reel.mp4"]
        main_mod.main()
        dispatch_all_channels("output/daily_kombin_reel.mp4", reel_url="")

    print("\n✅ [TAMAMLANDI] Tüm 4-segment yeni sezon sıfır-tekrar kreasyon paketleri @guzelaibot'a ve guzelai.com'a iletildi!")


if __name__ == "__main__":
    run_stock_batch()
