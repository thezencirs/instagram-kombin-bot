"""
GüzelAI Holding A.Ş. — Küresel Moda Gündemi (Fashion Agenda) & Stil Önerisi Motoru
+ Telegram Özel Kombin Segment Algılayıcı (Kadın / Erkek / Kız Çocuk / Erkek Çocuk)
+ %100 Fotogerçekçi Gerçek AI İnsan Model (Sıfır Animasyon/3D) Sentez Motoru
----------------------------------------------------------------------------------
Görevli Ajanlar:
- Ajan 1: ADA (Global Fashion Week & Street-Style Trend Radar)
- Ajan 14: KOR (Concept & Proportion Architect)
- Ajan 20: MAYA (Photorealistic AI Human Casting Director — 0% Animated/3D)
- Ajan 23-26: DEFNE (Kadın), KEREM (Erkek), LEYLA (Kız Çocuk), MERT (Erkek Çocuk)
- Ajan 30: DERİN (Optical Skin & Fabric Photorealism Specialist)
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
AGENDA_REPORT_JSON = BASE_DIR / "output" / "fashion_agenda_report.json"
AGENDA_REPORT_MD = BASE_DIR / "output" / "fashion_agenda_report.md"


GLOBAL_FASHION_AGENDA_2026_2027: Dict[str, List[Dict[str, Any]]] = {
    "kadin": [
        {
            "agenda_id": "fw26_milan_paris_burgundy_mocha_couture",
            "agenda_title": "Milano & Paris 2026/27 Kış Gündemi: 'Burgundy Oxblood & Mocha Mousse' Quiet Luxury",
            "hud_badge": "» MODA GÜNDEMİ: OXBLOOD BORDO & MOCHA KAŞMİR «",
            "hud_styling_tip": "STİL ÖNERİSİ: Yüksek Bel Palazzo + Açık Kruvaze Kaban ile 1/3–2/3 Altın Oran",
            "proportion_tip": "Yüksek bel geniş paça yün pantolonun içine fit boğazlı triko yerleştirip diz altı kruvaze kabanı açık bırakarak dikey 1/3 - 2/3 boy uzatma illüzyonu yaratın.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 koyu bordo/kahve ana silüet, %30 sıcak fildişi/ekru kaşmir aydınlığı, %10 gold tokalı deri çanta ve gözlük vurgusu.",
            "fabric_tip": "Mat İtalyan yün kaşe dokusunu yumuşak saf kaşmir triko ve tok kapitone deri aksesuarla birleştirerek sessiz lüks (Quiet Luxury) derinliği yakalayın.",
        },
        {
            "agenda_id": "fw26_paris_nisantasi_emerald_ivory_prestige",
            "agenda_title": "Paris & Nişantaşı 2026/27 Kış Gündemi: 'Zümrüt Kaşe, Fildişi Kaşmir & Espresso Terzilik'",
            "hud_badge": "» MODA GÜNDEMİ: ZÜMRÜT KAŞE & FİLDİŞİ KAŞMİR «",
            "hud_styling_tip": "STİL ÖNERİSİ: Koyu Dış Giyim + Açık Yaka Triko ile Yüz Aydınlatma Tekniği",
            "proportion_tip": "Omuzları net kruvaze uzun kaşe kaban ile yüksek bel pileli palazzo pantolonu eşleştirerek hem ofisten sokağa hem akşam davetine uyumlu kesintisiz silüet kurun.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 zümrüt yeşili ve koyu espresso zemin, %30 yüzü aydınlatan fildişi boğazlı katman, %10 tortoise/gold aksesuar dengesi.",
            "fabric_tip": "Tok yün kaşe, ince fitilli kaşmir ve süet detaylı deri sneaker kontrastı ile gün boyu zahmetsiz lüks konfor sağlayın.",
        },
        {
            "agenda_id": "fw26_nyc_london_anthracite_plum_monochrome",
            "agenda_title": "Londra & New York 2026/27 Kış Gündemi: 'Antrasit Mimari Kesim & Mürdüm Vurgu'",
            "hud_badge": "» MODA GÜNDEMİ: MİMARİ ANTRASİT & MÜRDÜM LÜKSÜ «",
            "hud_styling_tip": "STİL ÖNERİSİ: Nötr Kış Tonlarını Tek Bir Mücevher Rengi (Mürdüm/Bordo) İle Canlandırın",
            "proportion_tip": "Geniş omuzlu antrasit kabanın altında dar kesim dikey fitilli balıkçı yaka triko kullanarak üst gövdeyi daha ince ve uzun gösterin.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 antrasit ve ekru nötr taban, %30 mürdüm/erik triko ve çanta uyumu, %10 gümüş/siyah kemik gözlük dokunuşu.",
            "fabric_tip": "Dikey fitilli merinos triko ile akışkan yün palazzo kumaşın birlikte hareket etmesi videoda ve sokakta üst düzey dinamizm üretir.",
        },
    ],
    "erkek": [
        {
            "agenda_id": "fw26_milan_savile_row_charcoal_cognac",
            "agenda_title": "Milano & Savile Row 2026/27 Erkek Kış Gündemi: 'İtalyan Sartorial Kaşe & Merinos Katmanlama'",
            "hud_badge": "» MODA GÜNDEMİ: SARTORIAL KAŞE & MERİNOS TRİKO «",
            "hud_styling_tip": "STİL ÖNERİSİ: Gömlek Yerine İnce Fitilli Boğazlı Merinos İle Modern Sartorial Duruş",
            "proportion_tip": "Kruvaze uzun yün kaşe kabanı açık kullanıp içeride vücuda oturan boğazlı merinos triko ve tek pileli flanel pantolonla V-gövde (omuzları geniş, beli dar) oranı oluşturun.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 kömür siyahı/antrasit veya konyak-haki kaşe, %30 kontrast ekru/gece laciverti merinos, %10 hakiki deri hafta sonu çantası ve metal gözlük.",
            "fabric_tip": "Tok İtalyan yün kaşe, ince merinos yünü, tok flanel pantolon ve pebbled (grenli) deri çanta dörtlüsü erkek kış stilinde en üst düzey dokusal kaliteyi verir.",
        },
        {
            "agenda_id": "fw26_paris_mens_suede_shearling_noir",
            "agenda_title": "Paris & Bebek 2026/27 Erkek Kış Gündemi: 'Kürklü Süet Shearling & Monokrom Merinos'",
            "hud_badge": "» MODA GÜNDEMİ: SHEARLING SÜET & MONOKROM MERİNOS «",
            "hud_styling_tip": "STİL ÖNERİSİ: İç Triko ve Pantolonda Yakın Koyu Tonlar Kullanarak Boyu Uzatın",
            "proportion_tip": "Kalça hizasında biten kürklü yaka süet montu düz kesim flanel yün pantolonla tamamlayarak bacak boyunu maksimum uzunlukta gösterin.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 koyu merinos ve antrasit flanel, %30 konyak/bordo süet dış giyim, %10 temiz beyaz tabanlı deri sneaker kontrastı.",
            "fabric_tip": "Mat süet, yumuşak kürk yaka ve pürüzsüz merinos triko birleşimi soğuk kış günlerinde hem sıcak hem karizmatik bir şehir profili çizer.",
        },
    ],
    "kiz_cocuk": [
        {
            "agenda_id": "fw26_kids_girl_nordic_editorial_lookbook",
            "agenda_title": "2026/27 Kız Çocuk Kış Editoryal Gündemi: 'Yumuşak Peluş/Kaşe & İskandinav Triko Katmanlama'",
            "hud_badge": "» MODA GÜNDEMİ: KIZ ÇOCUK KIŞ EDİTORYAL STİLİ «",
            "hud_styling_tip": "STİL ÖNERİSİ: Yumuşak Pamuk/Yün İç Katman + Hafif ve Sıcak Dış Giyim Dengesi",
            "proportion_tip": "Hareket özgürlüğü sağlayan rahat kesim kışlık pantolonu sıcak tutan örgü kazak ve diz üstü kaban/mont ile tamamlayın.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 sıcak krem/indigo ana tonlar, %30 bordo/pastel kış rengi vurgu, %10 uyumlu bere ve sırt çantası.",
            "fabric_tip": "Çocuk cildine dost pamuk-yün karışımlı yumuşak triko ve rüzgar kesen sıcak kışlık dış giyim dokuları.",
        },
    ],
    "erkek_cocuk": [
        {
            "agenda_id": "fw26_kids_boy_urban_preppy_lookbook",
            "agenda_title": "2026/27 Erkek Çocuk Kış Editoryal Gündemi: 'Urban Preppy Parka & Renk Bloklu Triko'",
            "hud_badge": "» MODA GÜNDEMİ: ERKEK ÇOCUK URBAN PREPPY KIŞ STİLİ «",
            "hud_styling_tip": "STİL ÖNERİSİ: Renk Bloklu Pamuklu Triko + Fonksiyonel Kışlık Mont & Chino Uyumu",
            "proportion_tip": "Kapüşonlu kışlık mont veya kolej kaban altında renk bloklu pamuklu kazak ve rahat kesim chino pantolonla hem okul hem hafta sonu şıklığı yakalayın.",
            "color_rule_tip": "60-30-10 Renk Kuralı: %60 lacivert/haki/taş beji temel tonlar, %30 hardal/kiremit enerjik kış dokunuşu, %10 uyumlu bere ve sneaker.",
            "fabric_tip": "Nefes alan pamuklu örgü triko, dayanıklı pamuklu gabardin/chino ve su itici kışlık dış katman.",
        },
    ],
}


def detect_telegram_outfit_segment(
    text: str = "",
    urls: Optional[List[str]] = None,
    items: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Telegram'dan gelen kombin mesajı, başlık, ürün linkleri ve kazınan ürün isimlerinden
    kombinin Kadın ('kadin'), Erkek ('erkek'), Kız Çocuk ('kiz_cocuk') veya Erkek Çocuk ('erkek_cocuk')
    olduğunu otomatik algılar.
    """
    blobs: List[str] = [str(text or "")]
    for u in (urls or []):
        blobs.append(str(u))
    if isinstance(items, dict):
        for v in items.values():
            if isinstance(v, dict):
                blobs.append(str(v.get("name", "")))
                blobs.append(str(v.get("full_name", "")))
                blobs.append(str(v.get("category_label", "")))
                blobs.append(str(v.get("store_url", "")))
                blobs.append(str(v.get("brand", "")))

    combined = " ".join(blobs).lower()
    combined_norm = (
        combined.replace("ı", "i")
        .replace("ğ", "g")
        .replace("ü", "u")
        .replace("ş", "s")
        .replace("ö", "o")
        .replace("ç", "c")
    )

    # 1. Çocuk algılama (Kız Çocuk vs Erkek Çocuk)
    is_kid = any(
        kw in combined_norm
        for kw in [
            "cocuk",
            "kids",
            "bebek",
            "junior",
            "girl",
            "boy",
            "-g3-",
            "/cocuk-",
            "/kiz-cocuk",
            "/erkek-cocuk",
        ]
    )
    if is_kid:
        boy_score = sum(
            combined_norm.count(kw)
            for kw in ["erkek cocuk", "erkek-cocuk", "erkek bebek", "boy", "boys", "oglan"]
        )
        girl_score = sum(
            combined_norm.count(kw)
            for kw in ["kiz cocuk", "kiz-cocuk", "kiz bebek", "girl", "girls", "etek", "elbise", "pembe", "lila", "lavanta"]
        )
        if boy_score > girl_score:
            return "erkek_cocuk"
        if girl_score > boy_score:
            return "kiz_cocuk"
        # Eğer sadece 'çocuk' yazıyorsa erkek/kız ipuçlarına bak
        if "erkek" in combined_norm:
            return "erkek_cocuk"
        return "kiz_cocuk"

    # 2. Yetişkin Erkek vs Kadın algılama
    men_keywords = [
        "erkek",
        "/erkek-",
        "-g2-",
        "zara man",
        "mango man",
        "altinyildiz",
        "kigili",
        "damat",
        "menswear",
        "men's",
        "sakal",
    ]
    women_keywords = [
        "kadin",
        "/kadin-",
        "-g1-",
        "ipekyol",
        "twist",
        "quzu",
        "yargici",
        "palazzo",
        "topuklu",
        "elbise",
        "etek",
        "womenswear",
        "women's",
    ]
    men_score = sum(combined_norm.count(kw) for kw in men_keywords)
    women_score = sum(combined_norm.count(kw) for kw in women_keywords)

    if men_score > women_score:
        return "erkek"
    return "kadin"


def build_photorealistic_human_model_prompt(
    segment: str,
    district: str,
    hair_face: str,
    outer_desc: str,
    top_desc: str,
    bottom_desc: str,
    cap_desc: str,
    bag_desc: str,
    shoes_desc: str,
    pose_txt: str,
) -> str:
    """
    %100 FOTOGERÇEKÇİ GERÇEK İNSAN AI MODEL PROMPT MOTORU (SIFIR ANİMASYON / SIFIR 3D CGI):
    Kadın, Erkek, Kız Çocuk ve Erkek Çocuk dahil TÜM segmentlerde animasyon/çizgi/3D CGI karakterleri
    kesin olarak yasaklar; Hasselblad H6D-100c 85mm f/1.4 gerçek stüdyo/sokak insan modeli üretir.
    """
    clean_hair_face = re.sub(
        r"(?i)(3d\s*cgi|virtual\s*fashion\s*catalog\s*character\s*avatar|stylized\s*3d|cartoon|pixar|avatar|mannequin)",
        "photorealistic real human fashion model",
        hair_face or "",
    ).strip()

    if segment == "erkek":
        subject = (
            f"Vertical 9:16 ultra-photorealistic full-body luxury menswear street-style editorial photograph "
            f"of a 100% realistic adult male fashion supermodel ({clean_hair_face or 'charismatic male model with textured dark hair and sharp jawline'})"
        )
    elif segment == "kiz_cocuk":
        subject = (
            f"Vertical 9:16 ultra-photorealistic full-body Zara Kids / Massimo Dutti Kids luxury editorial lookbook photograph "
            f"of a 100% realistic real-looking human child girl fashion model ({clean_hair_face or '9-year-old girl model with natural wavy chestnut hair and warm smile'}, "
            f"real human skin and hair texture, strictly NOT 3D, NOT CGI, NOT cartoon, NOT doll, NOT animated)"
        )
    elif segment == "erkek_cocuk":
        subject = (
            f"Vertical 9:16 ultra-photorealistic full-body Zara Kids / Massimo Dutti Kids luxury editorial lookbook photograph "
            f"of a 100% realistic real-looking human child boy fashion model ({clean_hair_face or '9-year-old boy model with natural short brown hair and confident smile'}, "
            f"real human skin and hair texture, strictly NOT 3D, NOT CGI, NOT cartoon, NOT doll, NOT animated)"
        )
    else:
        subject = (
            f"Vertical 9:16 ultra-photorealistic full-body Vogue street-style luxury fashion editorial photograph "
            f"of a 100% realistic adult female fashion supermodel ({clean_hair_face or 'elegant female supermodel with wavy chestnut hair and hazel eyes'})"
        )

    return (
        f"{subject} walking along {district} in crisp winter golden-hour daylight, {pose_txt}, "
        f"wearing an open {outer_desc} over a {top_desc}, {bottom_desc}, {cap_desc}, carrying a {bag_desc}, "
        f"and wearing {shoes_desc}. Shot on Hasselblad H6D-100c medium format camera, 85mm f/1.4 prime lens, "
        f"authentic human skin micro-texture, natural fabric weave physics, optical depth-of-field bokeh, "
        f"photorealistic live-action commercial photography, zero 3D render, zero cartoon, no text, no watermark"
    )


def enrich_outfit_with_fashion_agenda(outfit: Dict[str, Any]) -> Dict[str, Any]:
    """
    Her kombine canlı Moda & Fashion Gündemi analizini, oran/silüet kuralını,
    60-30-10 renk senfonisini ve doku eşleşmesi önerilerini ekler.
    """
    seg = outfit.get("gender_segment", "kadin")
    agenda_pool = GLOBAL_FASHION_AGENDA_2026_2027.get(seg) or GLOBAL_FASHION_AGENDA_2026_2027["kadin"]
    arch_id = str(outfit.get("archetype_id") or outfit.get("id") or "")
    idx = sum(ord(c) for c in arch_id) % len(agenda_pool) if arch_id else 0
    chosen = dict(agenda_pool[idx])

    items = outfit.get("items") or {}
    outer_name = (items.get("outerwear") or {}).get("name", "Kışlık Dış Giyim")
    top_name = (items.get("top") or {}).get("name", "Triko Üst")
    bottom_name = (items.get("bottom") or {}).get("name", "Pantolon")
    bag_name = (items.get("bag") or {}).get("name", "Çanta")
    shoes_name = (items.get("shoes") or {}).get("name", "Ayakkabı")

    custom_styling_summary = (
        f"✨ MODA GÜNDEMİ & STİL ÖNERİSİ ({chosen['agenda_title']}):\n"
        f"• Silüet & Oran: {outer_name} ile {bottom_name} ikilisini {top_name} katmanıyla birleştirerek 1/3 - 2/3 dikey boy uzatma oranı yakalanır.\n"
        f"• Doku & Renk Uyumu: {chosen['color_rule_tip']} {bag_name} ve {shoes_name} ile kombin bütünlüğü tamamlanır."
    )

    outfit["fashion_agenda"] = {
        **chosen,
        "segment": seg,
        "custom_styling_summary": custom_styling_summary,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    os.makedirs(AGENDA_REPORT_JSON.parent, exist_ok=True)
    with open(AGENDA_REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(outfit["fashion_agenda"], f, ensure_ascii=False, indent=2)

    md_lines = [
        "# 👗 GüzelAI Holding — Canlı Moda & Fashion Gündemi Raporu",
        f"- **Kombin ID:** `{arch_id}`",
        f"- **Segment:** `{seg}`",
        f"- **Gündem Başlığı:** {chosen['agenda_title']}",
        f"- **2K Reels HUD Rozeti:** `{chosen['hud_badge']}`",
        f"- **2K Reels HUD Stil Kuralı:** `{chosen['hud_styling_tip']}`",
        f"- **Oran & Silüet Önerisi:** {chosen['proportion_tip']}",
        f"- **60-30-10 Renk Kuralı:** {chosen['color_rule_tip']}",
        f"- **Kumaş & Doku Kontrastı:** {chosen['fabric_tip']}",
    ]
    with open(AGENDA_REPORT_MD, "w", encoding="utf-8") as mf:
        mf.write("\n".join(md_lines) + "\n")

    return outfit
