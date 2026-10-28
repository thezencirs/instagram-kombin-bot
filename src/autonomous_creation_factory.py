"""
GuzelAI Ajan Kaynakları Birimi (Agent Resources Division) &
Argon'suz GitHub Actions Otonom Mevsimsel Kreasyon Fabrikası
-------------------------------------------------------------------------
Birim Ajanları:
- Ajan 19: ARDA (agent-resources-director) -> Ajan Kaynakları, Performans & Sıfır-Tekrar Orkestrasyon Direktörü
- Ajan 20: MAYA (ai-model-casting-director) -> Özgün AI Manken Casting & Tekil Karakter Kilit Ajanı
- Ajan 21: KAAN (seasonal-creation-factory-agent) -> Mevsimsel Özgün Kreasyon & Argon'suz Bulut 1:1 Dekupe Fabrikası
- Ajan 22: VERA (zero-repeat-quality-auditor) -> Sıfır-Tekrar, Mevsimsel Uyum & Telegram Tekil Gönderim Başdenetçisi
"""
import hashlib
import json
import os
import urllib.parse
from datetime import datetime
from io import BytesIO
from pathlib import Path
import requests
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
LEDGER_PATH = BASE_DIR / "output" / "zero_repeat_ledger.json"

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
]


def load_zero_repeat_ledger() -> dict:
    os.makedirs(LEDGER_PATH.parent, exist_ok=True)
    data = {
        "retired_archetypes": list(PERMANENTLY_RETIRED_ARCHETYPES),
        "retired_model_frames": list(PERMANENTLY_RETIRED_MODEL_FRAMES),
        "telegram_dispatched_ids": list(PERMANENTLY_RETIRED_ARCHETYPES),
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
        except Exception:
            pass

    # Ayrıca published_outfits_history.json ve instagram_uploaded_history.json içindekileri de ekle
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
    if telegram_sent and archetype_id and archetype_id not in ledger["telegram_dispatched_ids"]:
        ledger["telegram_dispatched_ids"].append(archetype_id)
    save_zero_repeat_ledger(ledger)


# ==============================================================================
# ARGON'SUZ GITHUB ACTIONS BULUT MEVSİMSEL KREASYON SENTEZLEYİCİ (KAAN & MAYA)
# ==============================================================================
DYNAMIC_SEASONAL_BLUEPRINTS = [
    {
        "id": "kadin_kis_etiler_antrasit_kase_murdum_kapsul",
        "gender_segment": "kadin",
        "title": "Etiler Kış Kreasyonu: Antrasit Uzun Kaşe Kaban, Mürdüm Balıkçı Triko & Ekru Yün Palazzo (%100 Özgün AI Manken) ❄️🧥✨",
        "model_prompt": (
            "Vertical 9:16 photorealistic full-body street fashion photograph head to toe showing shoes on stone pavement "
            "of a young female fashion model with sleek dark espresso-black bob hair walking along Etiler Istanbul boulevard "
            "in winter daylight, wearing an open charcoal-anthracite long wool coat over a deep plum-purple turtleneck sweater, "
            "high-waisted cream wide-leg wool palazzo trousers, black cat-eye sunglasses, structured plum leather handbag, "
            "and white-and-plum suede court sneakers"
        ),
        "items_spec": {
            "outerwear": ("İPEKYOL", "Kadın Antrasit Kruvaze Uzun Yün Kaşe Kaban", "3.499₺", 3499.0, "910201001", "Antrasit", "https://www.trendyol.com/kadin-kaban-x-g1-c55", "women charcoal anthracite double breasted long wool coat isolated on pure white background"),
            "cap": ("VOGUE EYEWEAR", "Kadın Siyah / Gümüş Cat-Eye Güneş Gözlüğü", "2.190₺", 2190.0, "910201002", "Siyah", "https://www.trendyol.com/kadin-gunes-gozlugu-x-g1-c101", "women black acetate cat eye sunglasses isolated on pure white background"),
            "top": ("TWIST", "Kadın Mürdüm / Koyu Mor Fitilli Boğazlı Triko Kazak", "899₺", 899.0, "910201003", "Mürdüm", "https://www.trendyol.com/kadin-kazak-x-g1-c1092", "women deep plum purple ribbed turtleneck sweater isolated on pure white background"),
            "bottom": ("YARGICI", "Kadın Ekru Yüksek Bel Pileli Yün Karışımlı Palazzo Pantolon", "1.450₺", 1450.0, "910201004", "Ekru", "https://www.trendyol.com/kadin-pantolon-x-g1-c70", "women cream ecru high waisted pleated wide leg wool palazzo trousers isolated on pure white background"),
            "bag": ("BAGMORI", "Kadın Mürdüm Deri Gold Tokalı Omuz Çantası", "849,90₺", 849.9, "910201005", "Mürdüm", "https://www.bagmori.com", "women structured deep plum leather shoulder handbag gold clasp isolated on pure white background"),
            "shoes": ("ADIDAS", "Kadın Beyaz / Mürdüm Süet Detaylı Court Sneaker", "3.699₺", 3699.0, "910201006", "Beyaz / Mürdüm", "https://www.trendyol.com/kadin-spor-ayakkabi-x-g1-c109", "women white and plum suede low top court sneakers isolated on pure white background"),
        },
    },
    {
        "id": "erkek_kis_levent_haki_parka_ekru_balikci_kapsul",
        "gender_segment": "erkek",
        "title": "Levent Kış Erkek Kreasyonu: Haki Kaşe Kaban, Kırık Beyaz Boğazlı Triko & Füme Kumaş Pantolon (%100 Özgün AI Erkek Manken) 🌲🧥✨",
        "model_prompt": (
            "Vertical 9:16 photorealistic full-body street fashion photograph head to toe showing shoes on stone pavement "
            "of a charismatic male fashion model with wavy dark auburn-brown hair and trimmed beard walking in Levent Istanbul "
            "in winter daylight, wearing an open dark olive-khaki wool overcoat over an off-white ribbed turtleneck sweater, "
            "tailored dark charcoal wool trousers, tortoise sunglasses, dark brown leather weekender bag, and olive-and-white suede sneakers"
        ),
        "items_spec": {
            "outerwear": ("NETWORK", "Erkek Koyu Haki Kruvaze Yün Kaşe Kaban", "4.299₺", 4299.0, "910301001", "Koyu Haki", "https://www.trendyol.com/erkek-kaban-x-g2-c55", "men dark olive khaki wool overcoat isolated on pure white background"),
            "cap": ("RAY-BAN", "Erkek Kahve / Gold Köşeli Güneş Gözlüğü", "4.850₺", 4850.0, "910301002", "Kahve / Gold", "https://www.trendyol.com/erkek-gunes-gozlugu-x-g2-c101", "men tortoise and gold sunglasses isolated on pure white background"),
            "top": ("MASSIMO DUTTI", "Erkek Kırık Beyaz / Ekru Fitilli Boğazlı Yün Triko Kazak", "1.590₺", 1590.0, "910301003", "Ekru", "https://www.trendyol.com/erkek-kazak-x-g2-c1092", "men off white ribbed turtleneck wool sweater isolated on pure white background"),
            "bottom": ("ALTINYILDIZ CLASSICS", "Erkek Füme / Antrasit Pileli Kışlık Yün Pantolon", "1.299₺", 1299.0, "910301004", "Füme / Antrasit", "https://www.trendyol.com/erkek-pantolon-x-g2-c70", "men dark charcoal wool pleated trousers isolated on pure white background"),
            "bag": ("TERGAN", "Erkek Koyu Kahve Deri Evrak & Seyahat Çantası", "2.690₺", 2690.0, "910301005", "Koyu Kahve", "https://www.trendyol.com/erkek-el-cantasi-x-g2-c101461", "men dark brown leather weekender bag isolated on pure white background"),
            "shoes": ("ADIDAS", "Erkek Haki / Beyaz Süet Detaylı Court Sneaker", "3.499₺", 3499.0, "910301006", "Haki / Beyaz", "https://www.trendyol.com/erkek-spor-ayakkabi-x-g2-c109", "men olive khaki and white suede low top court sneakers isolated on pure white background"),
        },
    },
]


def cloud_fetch_ai_image(prompt: str, width: int, height: int, seed: int) -> Image.Image | None:
    """
    GitHub Actions (ubuntu-latest) üzerinde Argon / yerel sunucu olmadan
    doğrudan bulut üzerinden AI görsel sentezler.
    """
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
    for attempt in range(1, 4):
        try:
            resp = requests.get(url, timeout=45)
            if resp.status_code == 200 and len(resp.content) > 10000:
                return Image.open(BytesIO(resp.content)).convert("RGB")
        except Exception as e:
            print(f"  [Bulut AI Sentez Denemesi {attempt}/3] {e}")
    return None
