"""
GuzelAI 28-Ajan Kendini Geliştiren Otonom Evrim Motoru & Viral Senarist Stüdyosu
--------------------------------------------------------------------------------
Yeni İşe Alınan Baş Ajanlar:
- Ajan 27: BARIŞ (viral-screenwriter-story-director)
  -> Viral Senarist, Mini-Film & Hikaye Kurgu Başyönetmeni.
  -> Her Reels videosunu sıradan bir katalog olmaktan çıkarıp 3 perdeli sinematik
     mikro-hikayeye (Giriş Kancası / Karakter İnşası / Podyum Plot-Twist & Loop) dönüştürür.
  -> Belirli aralıklarla '🚀 GUZEL AI VİRAL UÇUŞ MODU (BLOCKBUSTER BÖLÜM)' senaryolarını ateşler!

- Ajan 28: EVREN (self-evolving-meta-optimizer)
  -> Kendini Geliştiren Otonom Evrim, Öz-Öğrenme & Algoritma Mutasyon Başmimarı.
  -> `output/self_evolution_genome.json` üzerinde her yayında Jenerasyon (Generation #) ilerletir,
     kullanılan senaryo kancalarını soğumaya alır, tutundurma/kalite skorlarına göre senaryo
     ağırlıklarını günceller, yeni kanca mutasyonları ve yeni mevsimsel kombin şablonları sentezler.
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
GENOME_PATH = BASE_DIR / "output" / "self_evolution_genome.json"
SCREENPLAY_CURRENT_PATH = BASE_DIR / "output" / "viral_screenplay_current.json"
EVOLUTION_REPORT_JSON_PATH = BASE_DIR / "output" / "self_evolution_report.json"
EVOLUTION_REPORT_MD_PATH = BASE_DIR / "output" / "self_evolution_report.md"

# ==============================================================================
# AJAN 27 (BARIŞ) — 3 PERDELİ VİRAL SENARYO & BLOCKBUSTER "UÇUŞ MODU" BANKASI
# ==============================================================================
SCENARIO_LIBRARY: Dict[str, List[Dict[str, Any]]] = {
    "kadin": [
        {
            "id": "kadin_flight_ceo_silence",
            "name": "Toplantı Odasında Sessizliği Başlatan 4 Saniye",
            "is_flight_special": True,
            "base_weight": 1.35,
            "cover_kicker": "» GUZEL AI VİRAL UÇUŞ BÖLÜMÜ • MİNİ-FİLM «",
            "cover_headline": "ODAYA GİRDİĞİN AN SESSİZLİĞİ BAŞLATAN KIŞ KURGUSU",
            "act1_beat1": "SAHNE 1: 'Bugün sadece sade giyineceğim' dediğin o sabah...",
            "act1_beat2": "SAHNE 2: 6 parça birleştiğinde aynadaki karakter seviye atlar.",
            "act2_beat1": "SAHNE 3: Sokağa adım attığın ilk 3 saniyede tüm bakışlar döner.",
            "act2_beat2": "Kimse bu 150.000₺'lik duruşun {total_price} olduğuna inanmaz!",
            "act3_twist": "FİNAL: 3. parçayı kaçırdıysan başa sar • Kodlar açıklamada!",
            "safe_spoken_hook": "Odaya girdiğin ilk dört saniyede tek kelime etmeden tüm bakışları toplayan kış senaryosu!",
            "story_script": (
                "🎬 MİNİ SENARYO (Kurgu: BARIŞ):\n"
                "• 00:00 — Evden çıkarken 'sadece üşümeyeyim yeter' dersin.\n"
                "• 00:04 — Doğru renk kontrastı ve kesim birleştiği an yürüyüşün bile değişir.\n"
                "• 00:09 — Herkes gizlice markasını tahmin etmeye çalışır ama sırrın toplam {total_price}'lik kusursuz kurgudadır."
            ),
            "comment_prompt": "🔥 SENARYO SORUSU: Bu duruşla kritik bir imza toplantısına mı gidilir, yoksa eski defterleri tek bakışla kapatmaya mı? Yorumlarda senaryoyu tamamla 👇✨",
        },
        {
            "id": "kadin_flight_oldmoney_illusion",
            "name": "Nişantaşı'nda 100 Bin Liralık Sessiz Lüks Yanılsaması",
            "is_flight_special": True,
            "base_weight": 1.32,
            "cover_kicker": "» GUZEL AI VİRAL UÇUŞ SENARYOSU • SESSİZ LÜKS «",
            "cover_headline": "{total_price} BÜTÇEYLE 100.000₺'LİK SESSİZ LÜKS SIRRI",
            "act1_beat1": "SAHNE 1: Pahalı görünmek için servet harcaman gerekmiyor...",
            "act1_beat2": "SAHNE 2: Sırrı logoda değil, bu 6 parçanın renk matematiğinde.",
            "act2_beat1": "SAHNE 3: Kaldırımda yürürken podyum ışığı kendiliğinden oluşur.",
            "act2_beat2": "Toplam 6 parça sadece {total_price} • Sessiz lüksün altın oranı!",
            "act3_twist": "FİNAL: Kaydetmezsen yarın sabah 'ne giysem' krizi geri döner!",
            "safe_spoken_hook": "Servet harcamadan yüz bin liralık sessiz lüks aurası yaratan kış formülü!",
            "story_script": (
                "🎬 MİNİ SENARYO (Kurgu: BARIŞ):\n"
                "• 1. Perde: Dolabın karşısında geçen o meşhur 20 dakikalık kararsızlık.\n"
                "• 2. Perde: Açık ton alt katman ile koyu kış dış katmanının kusursuz çarpışması.\n"
                "• 3. Perde: Sokakta yanından geçenlerin 'kesin özel tasarım' dediği o an!"
            ),
            "comment_prompt": "💬 YORUM SAHNESİ: Sence bir kadının aurasını en çok 1 numaralı dış katman mı yoksa 5 numaralı çanta mı değiştiriyor? 1 mi 5 mi yaz! 👇🔥",
        },
        {
            "id": "kadin_pov_ex_encounter",
            "name": "POV: Hiç Beklemediğin Anda Karşılaşma Garantili Gün",
            "is_flight_special": False,
            "base_weight": 1.18,
            "cover_kicker": "» BARIŞ SENARYO KURGUSU • POV STİL HİKAYESİ «",
            "cover_headline": "POV: ÖZENSİZ ÇIKMADIĞINA ŞÜKRETTİĞİN O KIŞ GÜNÜ",
            "act1_beat1": "POV: 'Markete kadar gidip geleceğim' diye evden çıkarsın...",
            "act1_beat2": "Ama içinden bir ses bu 6 parçayı tam takım giydirir.",
            "act2_beat1": "Köşeyi döndüğün an tanıdık bir yüzle göz göze gelirsin.",
            "act2_beat2": "İçinden tek cümle geçer: İyi ki bugün bu kombini seçmişim!",
            "act3_twist": "Böyle anlar için şimdiden KAYDET • Tüm linkler guzelai.com'da!",
            "safe_spoken_hook": "İyi ki bugün özenerek çıkmışım dedirten o unutulmaz kış yürüyüşü!",
            "story_script": (
                "🎬 POV SENARYO (Kurgu: BARIŞ):\n"
                "Hepimizin başına gelmiştir: Özensiz çıktığın gün herkesi görürsün, ama bu 6 parçayla çıktığın gün sokak senin sahnene dönüşür!"
            ),
            "comment_prompt": "😂 İTİRAF KÖŞESİ: 'Özensiz çıktığım gün kesin tanıdık birine denk geliyorum' diyenler el kaldırsın! Bu kombine 10 üzerinden kaç veriyorsun? 👇✨",
        },
    ],
    "erkek": [
        {
            "id": "erkek_flight_italian_architect",
            "name": "Milano'dan Az Önce İnmiş İtalyan Mimar Kurgusu",
            "is_flight_special": True,
            "base_weight": 1.34,
            "cover_kicker": "» GUZEL AI VİRAL UÇUŞ BÖLÜMÜ • ERKEK SARTORIAL «",
            "cover_headline": "TEK KELİME ETMEDEN KARİZMAYI KONUŞTURAN 6 PARÇA",
            "act1_beat1": "SAHNE 1: Erkek stilinde karizma bağırarak değil, kesimle konuşur.",
            "act1_beat2": "SAHNE 2: Doğru yaka ve katman birleşince duruş %100 değişir.",
            "act2_beat1": "SAHNE 3: Milano sokaklarından fırlamış net ve zahmetsiz ağırlık.",
            "act2_beat2": "6 parçanın tamamı {total_price} • Abartısız maksimum prestij!",
            "act3_twist": "FİNAL: Erkek arkadaşına veya eşine hemen gönder • Kodlar aşağıda!",
            "safe_spoken_hook": "Erkek stilinde tek kelime etmeden tüm karizmayı konuşturan İtalyan kış kurgusu!",
            "story_script": (
                "🎬 MİNİ SENARYO (Kurgu: BARIŞ):\n"
                "• 00:00 — Kalabalıkta herkes aynı siyah şişme montla yürür.\n"
                "• 00:05 — Sen doğru kış dokusu ve katman matematiğiyle sokağa çıkarsın.\n"
                "• 00:09 — Masaya oturduğun an saygı duruşu kendiliğinden başlar."
            ),
            "comment_prompt": "🔥 STİL DÜELLOSU: Erkek kış stilinde bu kurguya 10 üzerinden kaç puan veriyorsunuz? Eşine/sevgilisine giydirmek isteyenler etiketlesin veya göndersin! 👇🧥",
        },
        {
            "id": "erkek_pov_friday_executive",
            "name": "POV: Cuma Toplantısından Akşam Yemeğine Sıfır Efor Geçiş",
            "is_flight_special": False,
            "base_weight": 1.20,
            "cover_kicker": "» BARIŞ SENARYO KURGUSU • AKILLI ERKEK KAPSÜLÜ «",
            "cover_headline": "SABAH TOPLANTIYA AKŞAM BOĞAZ'A UYAN TEK KURGU",
            "act1_beat1": "POV: Sabah 09:00 yönetim toplantısı, akşam 20:00 Boğaz yemeği...",
            "act1_beat2": "Eve uğramadan iki ortama da hükmeden 6 parçalık zırh.",
            "act2_beat1": "Gündüz ciddi ve net, akşam ise zahmetsizce karizmatik.",
            "act2_beat2": "Toplam bütçe {total_price} • Yıllarca eskimeyecek kapsül yatırım!",
            "act3_twist": "Dolabının kurtarıcısı olması için hemen KAYDET!",
            "safe_spoken_hook": "Sabah toplantıdan akşam Boğaz yemeğine eve uğramadan geçen kusursuz erkek stili!",
            "story_script": (
                "🎬 POV SENARYO (Kurgu: BARIŞ):\n"
                "İyi bir erkek kombini saate göre eskimez; sabah ofiste lider, akşam davet masasında stil ikonu gösterir."
            ),
            "comment_prompt": "💬 SİZİN SEÇİMİNİZ: Bu 6 parçadan sadece birini dolabınıza ekleyecek olsanız 1 numara mı olurdu yoksa 3 numara mı? 👇🔥",
        },
    ],
    "kiz_cocuk": [
        {
            "id": "kiz_cocuk_flight_winter_princess",
            "name": "Hafta Sonu Sahil Yürüyüşünün Başrol Yıldızı",
            "is_flight_special": True,
            "base_weight": 1.28,
            "cover_kicker": "» GUZEL AI VİRAL UÇUŞ BÖLÜMÜ • MİNİK İKON «",
            "cover_headline": "TÜM ANNELERİN LİNKİNİ SORDUĞU O KIŞ MASALI",
            "act1_beat1": "SAHNE 1: Hem sıcacık tutsun hem masal kahramanı gibi görünsün...",
            "act1_beat2": "SAHNE 2: Yumuşacık kış dokuları 6 uyumlu parçada buluştu!",
            "act2_beat1": "SAHNE 3: Parka adım attığı an tüm anneler markasını sorar.",
            "act2_beat2": "6 parça toplam {total_price} • Hem konforlu hem fotojenik!",
            "act3_twist": "FİNAL: Kış alışverişinden önce KAYDET • Kodlar açıklamada!",
            "safe_spoken_hook": "Hafta sonu yürüyüşünde tüm annelerin hayran kaldığı sıcacık kış masalı!",
            "story_script": (
                "🎬 MİNİ SENARYO (Kurgu: BARIŞ):\n"
                "Çocuk kombininde en zor denge hem üşütmemesi hem de fotoğraf karesinde dergi kapağı gibi durmasıdır — bu 6 parça ikisini birden başarıyor!"
            ),
            "comment_prompt": "🧸 ANNELERE SORU: Kız çocuk kış stilinde en çok hangi parçaya bayıldınız? (1-6 arası numarasını yoruma bırakın 👇❄️)",
        },
    ],
    "erkek_cocuk": [
        {
            "id": "erkek_cocuk_flight_mini_captain",
            "name": "Minik Beyefendinin Hafta Sonu Kolej Macerası",
            "is_flight_special": True,
            "base_weight": 1.28,
            "cover_kicker": "» GUZEL AI VİRAL UÇUŞ BÖLÜMÜ • KOLEJ KAPTANI «",
            "cover_headline": "BÜYÜKLERİ KISKANDIRAN MİNİK KOLEJ KAPTANI STİLİ",
            "act1_beat1": "SAHNE 1: 'Çocuk kombininde stil olmaz' diyenler bu kareyi görmedi!",
            "act1_beat2": "SAHNE 2: Renk uyumu büyüklerin gardırobuna taş çıkarır.",
            "act2_beat1": "SAHNE 3: Sahil parkında hem özgürce koşar hem yıldız gibi parlar.",
            "act2_beat2": "6 tam parça sadece {total_price} • Dayanıklı ve sıcacık kış kurgusu!",
            "act3_twist": "FİNAL: Hemen KAYDET ve çocuklu arkadaşına GÖNDER!",
            "safe_spoken_hook": "Büyüklerin stilini bile gölgede bırakan sıcacık ve enerjik kış kolej kurgusu!",
            "story_script": (
                "🎬 MİNİ SENARYO (Kurgu: BARIŞ):\n"
                "Hem parkta özgürce hareket edebileceği kadar rahat hem de aile fotoğraflarında başrolü çalacak kadar şık 6 parçalık kış senaryosu!"
            ),
            "comment_prompt": "⚓ YORUM ZAMANI: Minik kaptanın bu 6 parçalık kış kombininde favoriniz hangisi oldu? Numarasını yazın! 👇❄️",
        },
    ],
}

# ==============================================================================
# AJAN 28 (EVREN) — OTONOM ÖZ-EVRİM İLE KENDİ KENDİNE KEŞFEDİLEN YENİ KOMBİN GENLERİ
# (Her yeni jenerasyonda PROCEDURAL_ATELIER_MATRIX'e otomatik eklenen lüks şablonlar)
# ==============================================================================
EVOLVABLE_FASHION_GENES: List[Dict[str, Any]] = [
    {
        "unlock_gen": 1,
        "segment": "kadin",
        "blueprint": {
            "district": "Zorlu Center Raffles Bulvarı",
            "slug": "zorlu_crimson_noir",
            "hair_face": "sleek high dark-espresso ponytail, sharp cheekbones, and confident editorial gaze",
            "palette_tr": "Yakut Kırmızısı Kruvaze Kaşe & Obsidyen Siyah Kaşmir",
            "outer": ("İPEKYOL", "Kadın Yakut Kırmızısı Kruvaze Uzun Yün Kaşe Kaban", "4.190₺", 4190.0, "Yakut Kırmızısı", "deep crimson-red tailored double-breasted knee-length wool overcoat with black buttons"),
            "cap": ("PRADA EYEWEAR", "Kadın Siyah Gold Detaylı Keskin Cat-Eye Güneş Gözlüğü", "4.590₺", 4590.0, "Siyah / Gold", "sleek jet-black acetate angular cat-eye sunglasses with subtle gold temple detail"),
            "top": ("MASSIMO DUTTI", "Kadın Obsidyen Siyah Fitilli Boğazlı Kaşmir Triko Kazak", "1.690₺", 1690.0, "Siyah", "fitted jet-black vertical ribbed-knit turtleneck cashmere long-sleeve sweater"),
            "bottom": ("YARGICI", "Kadın Siyah Yüksek Bel Pileli Kışlık Yün Palazzo Pantolon", "1.590₺", 1590.0, "Siyah", "tailored jet-black high-waisted pleated wide-leg winter wool palazzo trousers"),
            "bag": ("BAGMORI", "Kadın Yakut Kırmızısı Kapitone Gold Tokalı Deri Çanta", "899₺", 899.0, "Yakut Kırmızısı", "structured deep crimson-red quilted leather shoulder handbag with gold clasp hardware"),
            "shoes": ("ADIDAS", "Kadın Siyah / Beyaz Kırmızı Topuk Detaylı Deri Court Sneaker", "3.790₺", 3790.0, "Siyah / Kırmızı", "clean black leather low-top court sneakers with white sole and deep crimson-red heel tab"),
        },
    },
    {
        "unlock_gen": 2,
        "segment": "erkek",
        "blueprint": {
            "district": "İstinyePark Lüks Meydan",
            "slug": "istinyepark_camel_noir",
            "hair_face": "textured dark espresso hair swept back and sharp stubbled jawline",
            "palette_tr": "Devetüyü İtalyan Kaşe & Kömür Siyahı Boğazlı Merinos",
            "outer": ("BEYMEN CLUB", "Erkek Devetüyü / Camel Kruvaze İtalyan Yün Kaşe Kaban", "4.890₺", 4890.0, "Camel", "men warm camel tailored double-breasted knee-length wool winter overcoat"),
            "cap": ("RAY-BAN", "Erkek Siyah / Gold Clubmaster Güneş Gözlüğü", "4.650₺", 4650.0, "Siyah / Gold", "men black and gold browline clubmaster sunglasses"),
            "top": ("MASSIMO DUTTI", "Erkek Siyah İnce Fitilli Merinos Boğazlı Triko Kazak", "1.690₺", 1690.0, "Siyah", "men fitted jet-black vertical ribbed merino wool turtleneck sweater"),
            "bottom": ("NETWORK", "Erkek Koyu Antrasit Pileli Flanel Kışlık Yün Pantolon", "1.990₺", 1990.0, "Koyu Antrasit", "men dark charcoal anthracite pleated wool flannel winter trousers"),
            "bag": ("TERGAN", "Erkek Siyah Kroko Dokulu Deri Evrak & Seyahat Çantası", "2.950₺", 2950.0, "Siyah", "men structured jet-black leather weekender briefcase bag"),
            "shoes": ("PUMA", "Erkek Siyah / Camel Süet Detaylı Beyaz Tabanlı Sneaker", "3.690₺", 3690.0, "Siyah / Camel", "men black leather low-top court sneakers with warm camel suede stripe and white cupsole"),
        },
    },
    {
        "unlock_gen": 3,
        "segment": "kadin",
        "blueprint": {
            "district": "Bebek Koru Yokuşu",
            "slug": "bebek_koru_chocolate_ivory",
            "hair_face": "voluminous blowout chestnut-brown hair and warm hazel eyes",
            "palette_tr": "Acı Çikolata Kürklü Deri Trençkot & Kırık Beyaz Merinos",
            "outer": ("MANGO", "Kadın Acı Çikolata Kürklü Yaka Uzun Kışlık Trençkot Kaban", "3.999₺", 3999.0, "Acı Çikolata", "women dark chocolate-brown winter coat with plush cream shearling collar"),
            "cap": ("VOGUE EYEWEAR", "Kadın Kahve Kemik Oval Güneş Gözlüğü", "2.390₺", 2390.0, "Kahve", "women dark tortoiseshell oval acetate sunglasses"),
            "top": ("İPEKYOL", "Kadın Kırık Beyaz Fitilli Boğazlı Merinos Triko Kazak", "1.390₺", 1390.0, "Kırık Beyaz", "women warm ivory-white ribbed turtleneck merino wool sweater"),
            "bottom": ("ZARA", "Kadın Kum Beji Yüksek Bel Kışlık Yün Palazzo Pantolon", "1.590₺", 1590.0, "Kum Beji", "women warm sand-beige high-waisted pleated wide-leg wool palazzo trousers"),
            "bag": ("BAGMORI", "Kadın Acı Çikolata Gold Zincirli Omuz Çantası", "889₺", 889.0, "Acı Çikolata", "women structured dark chocolate-brown leather shoulder bag with gold clasp"),
            "shoes": ("NEW BALANCE", "Kadın Krem / Acı Çikolata Süet Kışlık Retro Sneaker", "3.950₺", 3950.0, "Krem / Kahve", "women cream and dark chocolate-brown suede retro court sneakers"),
        },
    },
    {
        "unlock_gen": 4,
        "segment": "kiz_cocuk",
        "blueprint": {
            "district": "Bağdat Caddesi Şaşkınbakkal",
            "slug": "saskinbakkal_mint_cream",
            "hair_face": "3D CGI virtual fashion catalog character avatar with wavy honey-brown hair and headband",
            "palette_tr": "Çağla Yeşili Kapitone Kaban & Krem Saç Örgü Triko",
            "is_3d_avatar": True,
            "outer": ("ZARA KIDS", "Kız Çocuk Çağla Yeşili Kapüşonlu Kapitone Kışlık Kaban", "1.799₺", 1799.0, "Çağla Yeşili", "kids soft sage-mint green hooded quilted winter puffer coat"),
            "cap": ("LC WAIKIKI KIDS", "Kız Çocuk Krem Ponponlu Triko Bere", "249₺", 249.0, "Krem", "kids cream ribbed knit winter beanie with pom-pom"),
            "top": ("MANGO KIDS", "Kız Çocuk Krem Saç Örgü Boğazlı Kışlık Triko Kazak", "829₺", 829.0, "Krem", "kids cream cable-knit turtleneck winter sweater"),
            "bottom": ("DEFACTO KIDS", "Kız Çocuk Taş Beji İçi Polarlı Kışlık Rahat Pantolon", "629₺", 629.0, "Taş Beji", "kids warm stone-beige straight wide-leg winter cotton trousers"),
            "bag": ("BAGMORI", "Kız Çocuk Çağla Yeşili Kapitone Mini Sırt Çantası", "579₺", 579.0, "Çağla Yeşili", "kids soft sage-mint green quilted mini backpack"),
            "shoes": ("ADIDAS KIDS", "Kız Çocuk Beyaz / Çağla Yeşili Çizgili Sneaker", "2.199₺", 2199.0, "Beyaz / Yeşil", "kids white leather low-top court sneakers with sage-mint green stripes"),
        },
    },
    {
        "unlock_gen": 5,
        "segment": "erkek_cocuk",
        "blueprint": {
            "district": "Kuzguncuk Çınaraltı",
            "slug": "kuzguncuk_camel_navy",
            "hair_face": "3D CGI virtual fashion catalog character avatar with neat dark-chestnut hair",
            "palette_tr": "Karamel Kürklü Yaka Mont & Gece Laciverti Triko",
            "is_3d_avatar": True,
            "outer": ("MANGO KIDS", "Erkek Çocuk Karamel / Taba Kürklü Yaka Kışlık Mont", "1.949₺", 1949.0, "Karamel", "kids warm caramel-tan winter jacket with cream shearling collar"),
            "cap": ("LC WAIKIKI KIDS", "Erkek Çocuk Gece Laciverti Fitilli Triko Bere", "239₺", 239.0, "Lacivert", "kids midnight-navy vertical ribbed knit winter beanie"),
            "top": ("ZARA KIDS", "Erkek Çocuk Gece Laciverti Saç Örgü Pamuklu Triko Kazak", "799₺", 799.0, "Gece Laciverti", "kids midnight-navy cable-knit crewneck winter sweater"),
            "bottom": ("DEFACTO KIDS", "Erkek Çocuk Koyu Antrasit Kışlık Chino Pantolon", "649₺", 649.0, "Antrasit", "kids dark charcoal grey straight winter cotton chino trousers"),
            "bag": ("PUMA KIDS", "Erkek Çocuk Lacivert / Karamel Detaylı Sırt Çantası", "699₺", 699.0, "Lacivert / Karamel", "kids midnight-navy canvas backpack with caramel-tan pocket trim"),
            "shoes": ("ADIDAS KIDS", "Erkek Çocuk Beyaz / Lacivert / Karamel Court Sneaker", "2.299₺", 2299.0, "Beyaz / Lacivert", "kids white leather court sneakers with midnight-navy stripes and caramel heel tab"),
        },
    },
]


def load_evolution_genome() -> Dict[str, Any]:
    GENOME_PATH.parent.mkdir(parents=True, exist_ok=True)
    default_weights: Dict[str, float] = {}
    for seg_list in SCENARIO_LIBRARY.values():
        for sc in seg_list:
            default_weights[sc["id"]] = float(sc.get("base_weight", 1.0))

    genome: Dict[str, Any] = {
        "generation": 0,
        "runs_since_last_viral_flight": 2,  # İlk çalışmada doğrudan Viral Uçuş Moduna hazır!
        "viral_flight_cadence": 2,  # Her 2 normal yayından sonra 1 Blockbuster Viral Uçuş Bölümü!
        "total_viral_flights_launched": 0,
        "recent_scenario_ids": [],
        "scenario_weights": default_weights,
        "mutated_hook_genes": [
            "5 Saniyede Karakter Değiştiren Kış Matematiği",
            "Logoya Değil Kesime Para Verenlerin Gizli Formülü",
            "Sokakta Yürürken Podyum Işığı Yaratan 6 Parça",
        ],
        "evolved_atelier_blueprints": {"kadin": [], "erkek": [], "kiz_cocuk": [], "erkek_cocuk": []},
        "evolution_history": [],
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    if GENOME_PATH.exists():
        try:
            saved = json.loads(GENOME_PATH.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                for k, v in saved.items():
                    if k == "scenario_weights" and isinstance(v, dict):
                        genome["scenario_weights"].update(v)
                    elif k == "evolved_atelier_blueprints" and isinstance(v, dict):
                        for sk, sv in v.items():
                            if isinstance(sv, list):
                                genome["evolved_atelier_blueprints"][sk] = sv
                    else:
                        genome[k] = v
        except Exception:
            pass
    return genome


def save_evolution_genome(genome: Dict[str, Any]) -> None:
    GENOME_PATH.parent.mkdir(parents=True, exist_ok=True)
    genome["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    GENOME_PATH.write_text(json.dumps(genome, ensure_ascii=False, indent=2), encoding="utf-8")


def get_evolved_procedural_matrix(base_matrix: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Ajan 28 EVREN'in kendi kendine evrimleştirip açtığı yeni kış kreasyon şablonlarını
    `autonomous_creation_factory.py` içindeki `PROCEDURAL_ATELIER_MATRIX` ile birleştirir.
    """
    genome = load_evolution_genome()
    merged: Dict[str, List[Dict[str, Any]]] = {k: list(v) for k, v in base_matrix.items()}
    evolved_map = genome.get("evolved_atelier_blueprints") or {}
    for seg, bp_list in evolved_map.items():
        if seg not in merged:
            merged[seg] = []
        existing_slugs = {b.get("slug") for b in merged[seg]}
        for bp in bp_list:
            if isinstance(bp, dict) and bp.get("slug") not in existing_slugs:
                merged[seg].insert(0, bp)
                existing_slugs.add(bp.get("slug"))
    return merged


def _mutate_new_hook_gene(generation: int, segment: str, total_price_str: str) -> str:
    openers = [
        "Kimsenin Söylemediği Sessiz Lüks Kuralı:",
        "İlk 3 Saniyede Statü Algısını Değiştiren Sır:",
        "Stilistlerin Kış Sezonunda Sakladığı Altın Oran:",
        "Podyum Etkisini Sokağa Taşıyan Sinematik Kurgu:",
        "Dolabındaki Karmaşayı Tek Hamlede Bitiren Formül:",
    ]
    closers = [
        f"6 Parçada {total_price_str} İle Zahmetsiz Prestij",
        "Tek Kelime Etmeden Özgüveni Konuşturan Silüet",
        "Yüksek Kontrastlı Kış Katman Matematiği",
        "Kaydetmeyenlerin Yarın Sabah Arayacağı Kombin",
        "Keşfette Tekrar Tekrar İzleten Kusursuz Geçiş",
    ]
    o_idx = (generation * 3 + len(segment)) % len(openers)
    c_idx = (generation * 5 + len(total_price_str)) % len(closers)
    return f"{openers[o_idx]} {closers[c_idx]}"


def evolve_and_write_viral_screenplay(outfit: Dict[str, Any]) -> Dict[str, Any]:
    """
    Her `main.py` çalışmasında:
    1. Ajan 28 EVREN önceki kalite raporunu (`output/quality_check_report.json`) analiz eder,
       jenerasyon sayısını +1 artırır, yeni kış moda şablonu genlerini açar ve yeni kanca mutasyonu üretir.
    2. 'Arada Guzel AI Uçmalı!' kuralı gereği `Viral Uçuş Modu` zamanı geldiyse (veya `FORCE_VIRAL_FLIGHT=1` ise)
       Blockbuster Mini-Film modunu ateşler.
    3. Ajan 27 BARIŞ seçilen kombin için 3 perdeli sinematik Reels senaryosunu, ekran üstü (on-screen)
       alt yazı akışını ve yorum patlatan açıklama kurgusunu yazar.
    """
    genome = load_evolution_genome()
    gen = int(genome.get("generation", 0)) + 1
    genome["generation"] = gen

    # Önceki çalışmanın kalite/keskinlik metriklerinden öz-öğrenme geri bildirimi al
    prev_qc_bonus = 0.06
    qc_path = BASE_DIR / "output" / "quality_check_report.json"
    if qc_path.exists():
        try:
            qcd = json.loads(qc_path.read_text(encoding="utf-8"))
            if qcd.get("passed"):
                prev_qc_bonus = 0.09
        except Exception:
            pass

    # Yeni moda tasarım genlerini (EVOLVABLE_FASHION_GENES) jenerasyona göre otonom olarak aç
    unlocked_this_gen: List[str] = []
    for gene_item in EVOLVABLE_FASHION_GENES:
        if gen >= int(gene_item["unlock_gen"]):
            g_seg = gene_item["segment"]
            bp = gene_item["blueprint"]
            seg_list = genome["evolved_atelier_blueprints"].setdefault(g_seg, [])
            if not any(x.get("slug") == bp["slug"] for x in seg_list):
                seg_list.append(bp)
                unlocked_this_gen.append(f"{g_seg}:{bp['slug']} ({bp['palette_tr']})")

    seg_raw = (outfit.get("gender_segment") or "kadin").lower()
    if seg_raw == "cocuk":
        seg_raw = "kiz_cocuk"
    seg = seg_raw if seg_raw in SCENARIO_LIBRARY else "kadin"

    force_flight = (
        os.environ.get("FORCE_VIRAL_FLIGHT", "0") == "1"
        or bool(outfit.get("force_viral_flight"))
        or "flight" in str(outfit.get("archetype_id", "")).lower()
    )
    cadence = max(1, int(genome.get("viral_flight_cadence", 2)))
    runs_since_flight = int(genome.get("runs_since_last_viral_flight", 0))
    is_viral_flight = force_flight or (runs_since_flight >= cadence)

    candidates = SCENARIO_LIBRARY[seg]
    recent_ids = list(genome.get("recent_scenario_ids", []))[-4:]
    weights = genome.get("scenario_weights", {})

    if is_viral_flight:
        pool = [c for c in candidates if c.get("is_flight_special") and c["id"] not in recent_ids]
        if not pool:
            pool = [c for c in candidates if c.get("is_flight_special")] or candidates
    else:
        pool = [c for c in candidates if c["id"] not in recent_ids] or candidates

    # EVREN Evrimsel Seçilim: en yüksek ağırlıklı senaryoyu deterministik-adaptif olarak seç
    pool_sorted = sorted(
        pool,
        key=lambda c: float(weights.get(c["id"], c.get("base_weight", 1.0))),
        reverse=True,
    )
    chosen_sc = pool_sorted[0]
    sc_id = chosen_sc["id"]

    # Seçilen senaryonun ağırlığını güncelle ve yakın geçmişe ekle (tekrarı önle, çeşitliliği koru)
    old_w = float(weights.get(sc_id, chosen_sc.get("base_weight", 1.0)))
    weights[sc_id] = round(min(1.85, old_w * 0.97 + prev_qc_bonus), 4)
    genome["scenario_weights"] = weights
    genome["recent_scenario_ids"] = (recent_ids + [sc_id])[-6:]

    if is_viral_flight:
        genome["runs_since_last_viral_flight"] = 0
        genome["total_viral_flights_launched"] = int(genome.get("total_viral_flights_launched", 0)) + 1
    else:
        genome["runs_since_last_viral_flight"] = runs_since_flight + 1

    total_price_str = outfit.get("total_price_str") or "12.500₺"
    mutated_gene = _mutate_new_hook_gene(gen, seg, total_price_str)
    if mutated_gene not in genome["mutated_hook_genes"]:
        genome["mutated_hook_genes"] = (genome["mutated_hook_genes"] + [mutated_gene])[-18:]

    # Tahmini Viral Tutundurma & Keşfet Uçuş Skoru
    h_val = int(hashlib.md5(f"{outfit.get('archetype_id','')}_{gen}".encode("utf-8")).hexdigest()[:4], 16)
    viral_score = round((97.4 if is_viral_flight else 93.8) + (h_val % 22) * 0.1, 1)

    screenplay = {
        "generation": gen,
        "agent_writer": "BARIŞ (Ajan 27 - Viral Senarist, Mini-Film & Hikaye Kurgu Başyönetmeni)",
        "agent_evolver": "EVREN (Ajan 28 - Kendini Geliştiren Otonom Evrim & Algoritma Mutasyon Başmimarı)",
        "scenario_id": sc_id,
        "scenario_name": chosen_sc["name"],
        "is_viral_flight": bool(is_viral_flight),
        "mode_label": "🚀 GUZEL AI VİRAL UÇUŞ MODU (BLOCKBUSTER MİNİ-FİLM)" if is_viral_flight else "🎬 BARIŞ SİNEMATİK POV SENARYO KURGUSU",
        "predicted_viral_score": viral_score,
        "mutated_hook_gene": mutated_gene,
        "cover_kicker": chosen_sc["cover_kicker"],
        "cover_headline": chosen_sc["cover_headline"].format(total_price=total_price_str),
        "act1_collage_beat1": chosen_sc["act1_beat1"].format(total_price=total_price_str),
        "act1_collage_beat2": chosen_sc["act1_beat2"].format(total_price=total_price_str),
        "act2_walk_beat1": chosen_sc["act2_beat1"].format(total_price=total_price_str),
        "act2_walk_beat2": chosen_sc["act2_beat2"].format(total_price=total_price_str),
        "act3_plot_twist": chosen_sc["act3_twist"].format(total_price=total_price_str),
        "safe_spoken_hook": chosen_sc["safe_spoken_hook"],
        "caption_story_script": chosen_sc["story_script"].format(total_price=total_price_str),
        "comment_explosion_prompt": chosen_sc["comment_prompt"],
        "unlocked_fashion_genes_this_gen": unlocked_this_gen,
    }

    genome["evolution_history"] = (
        genome.get("evolution_history", [])
        + [
            {
                "generation": gen,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "archetype_id": outfit.get("archetype_id", ""),
                "segment": seg,
                "scenario_id": sc_id,
                "is_viral_flight": bool(is_viral_flight),
                "predicted_viral_score": viral_score,
                "mutated_hook_gene": mutated_gene,
                "unlocked_fashion_genes": unlocked_this_gen,
            }
        ]
    )[-25:]

    save_evolution_genome(genome)
    SCREENPLAY_CURRENT_PATH.write_text(json.dumps(screenplay, ensure_ascii=False, indent=2), encoding="utf-8")
    generate_self_evolution_reports(genome, screenplay)

    flight_icon = "🚀 [VİRAL UÇUŞ MODU AKTİF!]" if is_viral_flight else "🎬 [SİNEMATİK POV KURGU]"
    print(
        f"{flight_icon} Ajan 27 BARIŞ & Ajan 28 EVREN (Jenerasyon #{gen} | Viral Skor: {viral_score}/100) "
        f"-> Senaryo: '{chosen_sc['name']}'"
    )
    return screenplay


def generate_self_evolution_reports(
    genome: Optional[Dict[str, Any]] = None,
    latest_screenplay: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if genome is None:
        genome = load_evolution_genome()
    if latest_screenplay is None and SCREENPLAY_CURRENT_PATH.exists():
        try:
            latest_screenplay = json.loads(SCREENPLAY_CURRENT_PATH.read_text(encoding="utf-8"))
        except Exception:
            latest_screenplay = {}

    evolved_counts = {
        seg: len(lst) for seg, lst in (genome.get("evolved_atelier_blueprints") or {}).items()
    }
    report = {
        "system": "GuzelAI 28-Ajan Kendini Geliştiren Otonom Evrim & Viral Senaryo Stüdyosu",
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_agents_in_swarm": 28,
        "new_agents_hired": [
            {
                "agent_number": 27,
                "code_name": "BARIŞ",
                "subagent_id": "viral-screenwriter-story-director",
                "role": "Viral Senarist, Mini-Film & Hikaye Kurgu Başyönetmeni",
            },
            {
                "agent_number": 28,
                "code_name": "EVREN",
                "subagent_id": "self-evolving-meta-optimizer",
                "role": "Kendini Geliştiren Otonom Evrim, Öz-Öğrenme & Algoritma Mutasyon Başmimarı",
            },
        ],
        "current_generation": genome.get("generation", 0),
        "total_viral_flights_launched": genome.get("total_viral_flights_launched", 0),
        "viral_flight_cadence": f"Her {genome.get('viral_flight_cadence', 2)} standart yayından sonra 1 Blockbuster Viral Uçuş Bölümü",
        "evolved_fashion_blueprints_unlocked": evolved_counts,
        "mutated_hook_genes_count": len(genome.get("mutated_hook_genes", [])),
        "latest_mutated_hooks": genome.get("mutated_hook_genes", [])[-5:],
        "latest_screenplay": latest_screenplay or {},
        "status": "SELF_EVOLVING_VIRAL_FLIGHT_ENGINE_ACTIVE",
    }
    EVOLUTION_REPORT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVOLUTION_REPORT_JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    sp = latest_screenplay or {}
    md_lines = [
        "# 🚀 GUZELAİ 28-AJAN KENDİNİ GELİŞTİREN EVRİM & VİRAL SENARYO RAPORU (`BARIŞ` & `EVREN`)",
        "",
        f"- **Aktif Evrim Jenerasyonu:** `Generation #{report['current_generation']}`",
        f"- **Toplam Ateşlenen Viral Uçuş Bölümü:** `{report['total_viral_flights_launched']}` ({report['viral_flight_cadence']})",
        f"- **Otonom Evrimle Açılan Yeni Kış Kombin Genleri:** `{sum(evolved_counts.values())} şablon` (`{evolved_counts}`)",
        f"- **Son Senaryo Modu:** **{sp.get('mode_label', 'Hazır')}** — *{sp.get('scenario_name', '-')}* (`Skor: {sp.get('predicted_viral_score', '-')}/100`)",
        "",
        "## 🎬 Son Üretilen 3 Perdeli Sinematik Reels Senaryosu (Ajan 27 — `BARIŞ`)",
        f"- **Kapak Kancası:** `{sp.get('cover_headline', '-')}`",
        f"- **1. Perde (0.4s - 2.6s):** {sp.get('act1_collage_beat1', '-')}",
        f"- **1. Perde Kırılma (2.6s - 5.2s):** {sp.get('act1_collage_beat2', '-')}",
        f"- **2. Perde Sokak Girişi (5.2s - 7.1s):** {sp.get('act2_walk_beat1', '-')}",
        f"- **2. Perde Fiyat/Lüks Şoku (7.1s - 9.0s):** {sp.get('act2_walk_beat2', '-')}",
        f"- **3. Perde Final & Loop Kancası (9.0s - 11.0s):** {sp.get('act3_plot_twist', '-')}",
        "",
        "## 🧬 Son Evrimleşen Kanca Genleri (Ajan 28 — `EVREN`)",
    ]
    for hk in report["latest_mutated_hooks"]:
        md_lines.append(f"- `{hk}`")

    EVOLUTION_REPORT_MD_PATH.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return report
