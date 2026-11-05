# GüzelAI Holding A.Ş. — Zorunlu Proje Kuralları (AGENTS.md)

## 1. %100 Fotogerçekçi İnsan AI Modeller (Sıfır Animasyon / Sıfır 3D Karakter)
- Kadın (`kadin`), Erkek (`erkek`), Kız Çocuk (`kiz_cocuk`) ve Erkek Çocuk (`erkek_cocuk`) dahil **tüm segmentlerde** `is_3d_avatar = False` zorunludur.
- Animasyon, 3D CGI, Pixar, karikatür veya oyuncak bebek görünümlü karakter üretimi kesinlikle yasaktır.
- Tüm mankenler **Hasselblad H6D-100c 85mm f/1.4** editöryal lens estetiğinde, doğal cilt ve kumaş dokusuna sahip **%100 fotogerçekçi gerçek insan AI manken** olarak üretilmelidir.

## 2. Sıfır-Tekrar Çift Kilit (Zero-Repeat Double-Lock)
- Daha önce paylaşılan hiçbir kombin (`archetype_id`) veya manken yürüyüş serisi (`model_frames[0]`) tekrar paylaşılamaz (`PERMANENTLY_RETIRED_ARCHETYPES`).
- `output/zero_repeat_ledger.json` hem yerel diske hem de `GH_TOKEN` üzerinden GitHub Contents API (`PUT /repos/thezencirs/instagram-kombin-bot/contents/output/zero_repeat_ledger.json`) ile anında buluta yazılmalıdır.
- `.github/workflows/daily_reels.yml` içinde `git add` komutu asla tek satırda çoklu opsiyonel dosyayla çağrılmamalı; her dosya `if [ -e "$f" ]; then git add -f "$f"; fi` döngüsüyle ayrı ayrı eklenmelidir.

## 3. Telegram (@guzelaibot) Saf Kopyala-Yapıştır Metin Kuralı
- `src/telegram_publisher.py` (`send_outfit_to_chat`) içindeki metin mesajında **yalnızca doğrudan kopyalanıp yapıştırılacak net paylaşım metni (`raw_cap`)** gönderilmelidir.
- Mesaj başında veya sonunda `"📋 [KOPYALA-YAPIŞTIR AÇIKLAMA & LİNKLER 3/3]"`, `"Kopyalanacak metin:"`, `"👇 Instagram Reels / TikTok için..."`, `"💬 Sabit Yorum..."` gibi sarmalayıcı ifadeler kesinlikle yer almamalıdır.

## 4. 2026–2027 Moda Gündemi, Stil Önerileri & 2K QHD+ Remotion Sinema Kalitesi
- Her kombin `src/fashion_agenda_engine.py` üzerinden aktif küresel moda gündemi (Milano, Paris, Londra, NYC, İstanbul 2026–2027 FW), **1/3–2/3 silüet altın oranı** ve **60-30-10 renk/doku uyumu** önerileriyle zenginleştirilmelidir.
- `src/render_reels.py` çıktıları **1440×2560 (2K QHD+) @ 30fps**, Remotion yay fiziği (`_remotion_spring`), `_sample_gimbal_step` optik kare geçişi, `unsharp=5:5:0.75:3:3:0.0` mikro-keskinlik ve **CRF 12 / 22 Mbps (30 Mbps maxrate)** H.264 High@L5.1 standardında üretilmelidir.

## 5. Çoklu Kullanıcı Telegram Kombin İşleme Önceliği
- `src/main.py` çalışmaya başladığında soğuma (cooldown) kontrolünden **önce** `poll_and_enqueue_telegram_outfits()` çalıştırılmalıdır.
- Yönetici (`995164733`) veya `@guzelaibot`'u kullanan **herhangi bir Telegram kullanıcısı (`requester_chat_id`)** ürün linki, düz çekim (flat-lay) fotoğraf veya kombin metni gönderdiğinde:
  1. İstek `output/telegram_pending_outfits_queue.json` kuyruğuna kaydedilir ve soğuma süresi (cooldown) otomatik bypass edilir.
  2. Kombinin **Kadın (`kadin`), Erkek (`erkek`), Kız Çocuk (`kiz_cocuk`) veya Erkek Çocuk (`erkek_cocuk`)** olduğu otomatik algılanır.
  3. Parçalar %100 fotogerçekçi gerçek insan AI manken üzerinde 2K Reels olarak hazırlanır ve hem kombini gönderen kullanıcıya (`requester_chat_id`) hem de yöneticiye (`995164733`) teslim edilir.
