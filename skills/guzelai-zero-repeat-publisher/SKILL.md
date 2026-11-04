---
name: guzelai-zero-repeat-publisher
description: Atomic Zero-Repeat Ledger (Local + GitHub Contents API Double-Lock) and Pure Net Copy-Paste Telegram Publisher Skill for GüzelAI Holding (@guzelaibot). Prevents outfit repetition forever and outputs clean copy-paste post text with zero wrapper labels.
---

# GüzelAI Holding — Zero-Repeat Atomic Lock & Net Copy-Paste Publisher Skill (`guzelai-zero-repeat-publisher`)

## Core Mandate
1. **100% Zero-Repeat Guarantee (Local + GitHub API Double-Lock):**
   - Never repeat any previously shared outfit (`archetype_id`) or supermodel (`model_frames[0]`).
   - `load_zero_repeat_ledger()` merges local `output/zero_repeat_ledger.json` with remote `repos/thezencirs/instagram-kombin-bot/contents/output/zero_repeat_ledger.json` via GitHub API (`GH_TOKEN`).
   - `mark_creation_and_model_used()` immediately persists the updated ledger both locally and to GitHub via `PUT /repos/thezencirs/instagram-kombin-bot/contents/output/zero_repeat_ledger.json` (`[skip ci]`), ensuring that even if a workflow step is interrupted, no outfit can ever be repeated.
   - In `.github/workflows/daily_reels.yml`, stage files individually (`for f in ...; do [ -e "$f" ] && git add -f "$f"; done`) so a missing optional file never blocks `git add` for `zero_repeat_ledger.json`.

2. **Pure, Net Copy-Paste Text Only on Telegram (`@guzelaibot`):**
   - When sending the post caption to Telegram (`send_outfit_to_chat` in `src/telegram_publisher.py`), send **ONLY the ready-to-copy-and-paste caption text itself**.
   - **Forbidden wrapper text:** Never include `"📋 [KOPYALA-YAPIŞTIR AÇIKLAMA & LİNKLER 3/3]"`, `"👇 Instagram Reels / TikTok için aşağıdaki kutuya dokunarak..."`, `"Kopyalanacak metin:"`, or `"💬 Sabit Yorum..."`.
   - The Telegram text message must be 100% pure post text (Viral Hook + Moda Gündemi & Stil Önerisi + 1..6 Parça Marka/Fiyat/Link Listesi + Hashtagler) so the user can copy the entire message in one tap and paste it directly.
