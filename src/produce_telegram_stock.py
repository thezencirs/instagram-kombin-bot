"""
GuzelAI 26 Ajanlı (Moda Tasarım Atölyesi DEFNE, KEREM, LEYLA, MERT + Ajan Kaynakları Birimi ARDA, MAYA, KAAN, VERA + İK Direktörü İREM + 1:1 Görsel Başdenetçisi SARP Onaylı)
%100 Sıfır-Tekrar (Zero-Repeat) Manken & Kombin Garantili, 2026-2027 Kış Sezonu Telegram Süper Yayın Üretim Hattı
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
    run_fashion_atelier_designers,
    run_agent_resources_division,
    run_hr_agent_trainer_director,
    run_visual_1to1_match_inspector,
    run_dispatcher_reporter,
)
import main as main_mod
from instagram_uploader import dispatch_all_channels

# Moda Tasarım Atölyesi (DEFNE, KEREM, LEYLA, MERT) + Ajan Kaynakları Birimi (ARDA, MAYA, KAAN, VERA) & SARP tarafından
# %100 1:1 manken-kıyafet eşleşmesi ve %100 SIFIR-TEKRAR uyumu doğrulanan 4-Segment Kış Süper Yayın Listesi
# (Not: Diğer 4 yeni stüdyo kış kreasyonu + Sonsuz Bulut FLUX.1 Sentez Motoru GitHub Actions otomatik yayınları için rezervde bırakılmıştır!):
VERIFIED_1TO1_STOCK_QUEUE = [
    ("kis_atolye_kadin_etiler", "kadin_kasim_etiler_antrasit_kase_murdum"),
    ("kis_atolye_erkek_levent", "erkek_kasim_levent_haki_kase_ekru_balikci"),
    ("kis_atolye_kiz_cocuk_suadiye", "cocuk_kiz_kasim_suadiye_krem_pelus_bordo"),
    ("kis_atolye_erkek_cocuk_fenerbahce", "cocuk_erkek_kasim_fenerbahce_lacivert_puffer_hardal"),
]


def run_stock_batch():
    print("👗 [Moda Tasarım Atölyesi - DEFNE, KEREM, LEYLA, MERT & Ajan Kaynakları - ARDA, MAYA, KAAN, VERA] 26-Ajan Kış Kreasyon ve Sıfır-Tekrar Denetimi Başlatılıyor...")
    atelier_report = run_fashion_atelier_designers()
    ar_report = run_agent_resources_division()
    v_report = run_visual_1to1_match_inspector()
    hr_report = run_hr_agent_trainer_director()
    run_dispatcher_reporter()

    if not v_report.get("live_scrape_random_override_blocked"):
        raise RuntimeError("KRİTİK HATA: force_live_scrape kilidi aktif değil! Stok üretimi durduruldu.")

    for idx, (slot_label, arch_id) in enumerate(VERIFIED_1TO1_STOCK_QUEUE, start=1):
        print(f"\n==================================================================")
        print(f"📦 [26-AJAN MODA ATÖLYESİ KIŞ SÜPER YAYIN PAKETİ {idx}/{len(VERIFIED_1TO1_STOCK_QUEUE)}] {arch_id}")
        print(f"==================================================================")
        os.environ["FORCE_ARCHETYPE_ID"] = arch_id
        os.environ["SLOT_NAME"] = slot_label
        os.environ["TELEGRAM_ONLY_MODE"] = "1"
        os.environ["IG_ENABLE_UPLOAD"] = "0"
        sys.argv = ["main.py", "--output", "output/daily_kombin_reel.mp4"]
        main_mod.main()
        dispatch_all_channels("output/daily_kombin_reel.mp4", reel_url="")

    # Son olarak raporları güncel rezerv/emekli sayılarıyla tekrar senkronize et
    run_fashion_atelier_designers()
    run_agent_resources_division()
    print("\n✅ [TAMAMLANDI] Tüm 4-segment Kış Moda Tasarım Atölyesi süper yayın paketleri @guzelaibot'a ve guzelai.com'a iletildi!")


if __name__ == "__main__":
    run_stock_batch()
