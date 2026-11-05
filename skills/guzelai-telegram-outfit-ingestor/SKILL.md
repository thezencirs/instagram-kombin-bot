---
name: guzelai-telegram-outfit-ingestor
description: Ingests outfits, product links, flat-lay photos, or text descriptions sent by ANY user to @guzelaibot on Telegram, automatically detects the gender/age segment (kadin, erkek, kiz_cocuk, erkek_cocuk), synthesizes 100% photorealistic real-looking human AI models wearing those exact items plus 6 studio 1:1 cutouts, and delivers the 2K Reel back to the requesting user and admin.
---

# GüzelAI Holding — Telegram Outfit Ingestor & Photorealistic AI Model Synthesis Skill (`guzelai-telegram-outfit-ingestor`)

## Core Mandate
1. **Priority #1: Always Process Outfits Sent via Telegram (`@guzelaibot`) by Admin OR Any External User:**
   - At the very start of `src/main.py` (before cooldown check and before `select_daily_outfit`), call `poll_and_enqueue_telegram_outfits()` to poll `@guzelaibot` (`getUpdates`) and check `output/telegram_pending_outfits_queue.json` + `output/telegram_trigger_override.json` (plus remote GitHub queue via `GH_TOKEN`).
   - Whenever the admin (`995164733`) OR **any other Telegram user (`requester_chat_id`)** sends product links (Trendyol, Zara, Mango, Bagmori, İpekyol, etc.), a flat-lay/collage photo, or an outfit description to `@guzelaibot`:
     - Never lose or discard the update in a short-lived daemon thread!
     - Never block non-admin users (`cid != "995164733"` restriction is forbidden).
     - Bypass the 4-hour cooldown whenever a Telegram outfit request is pending.
     - Persist the incoming Telegram outfit request into `output/telegram_pending_outfits_queue.json` (with `requester_chat_id` and `requester_name`, synced to GitHub via Contents API) and process it immediately in `generate_daily_outfit()`.
     - Once rendered, deliver the finished 2K Reel package + pure net copy-paste caption directly to `requester_chat_id` as well as `995164733`.

2. **Automatic Gender & Age Segment Detection (`kadın`, `erkek`, `kız çocuk`, `erkek çocuk`):**
   - Analyze all product URLs, scraped product titles/breadcrumbs, and Telegram message/caption text:
     - **Kız Çocuk (`kiz_cocuk`):** Keywords `kız çocuk`, `kiz-cocuk`, `kız bebek`, `girl`, `kids girl`, `-g3-` with girl items.
     - **Erkek Çocuk (`erkek_cocuk`):** Keywords `erkek çocuk`, `erkek-cocuk`, `erkek bebek`, `boy`, `kids boy`, `çocuk`, `kids`.
     - **Erkek (`erkek`):** Keywords `erkek`, `men`, `man`, `-g2-`, `/erkek-`.
     - **Kadın (`kadin`):** Keywords `kadın`, `kadin`, `women`, `woman`, `elbise`, `palazzo`, `topuklu`, `-g1-`, `/kadin-`.

3. **100% Photorealistic Real-Looking AI Models (`gerçek ai modellere yap` — Even for Kids!):**
   - **Strictly ZERO animated / 3D CGI / cartoon characters (`is_3d_avatar = False` for ALL segments including `kiz_cocuk` and `erkek_cocuk`)!**
   - For **`kadin`**: Photorealistic adult female supermodel shot on Hasselblad H6D-100c 85mm f/1.4 prime lens, natural skin texture, walking on luxury Istanbul boulevard wearing the exact 6 items.
   - For **`erkek`**: Photorealistic adult male supermodel shot on Hasselblad H6D-100c 85mm f/1.4 prime lens, natural skin texture, walking on luxury Istanbul boulevard wearing the exact 6 items.
   - For **`kiz_cocuk` & `erkek_cocuk`**: Photorealistic real-looking AI child fashion model (Zara Kids / Massimo Dutti Kids editorial lookbook photography, shot on 85mm f/1.4 lens, real skin and hair texture, zero 3D/cartoon/Pixar look) wearing the exact 6 items.
