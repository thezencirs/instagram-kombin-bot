"""
Official GuzelAI.com Model Roster Lock (`src/guzelai_official_models.py`)
=========================================================================
Enforces the strict rule:
- ONLY official models registered on `https://guzelai.com` (`src/data/models.ts`) may be used
  in outfit generations across ALL 4 segments (`kadin`, `erkek`, `kiz_cocuk`, `erkek_cocuk`).
- Zero random/outside model faces are permitted.
- Every outfit carries `guzelai_model_id`, `guzelai_model_name`, `guzelai_model_badge`, and
  `guzelai_face_prompt_en` locked to the official `guzelai.com` roster.
"""

from typing import Any, Dict, List

GUZELAI_COM_OFFICIAL_MODELS: Dict[str, List[Dict[str, Any]]] = {
    "kadin": [
        {
            "id": "guzelai-leyla-001",
            "name": "Leyla",
            "badge": "guzelai.com • Leyla",
            "title_tr": "İstanbul Zarafeti & Old Money Marka Yüzü (guzelai.com)",
            "avatar_url": "https://guzelai.com/influencers/leyla/reference.png",
            "face_prompt_en": (
                "official guzelai.com female model Leyla (25-year-old Turkish-Mediterranean woman with shoulder-length "
                "wavy dark chestnut-brown hair, warm expressive hazel-brown eyes, natural warm olive-ivory skin tone, "
                "soft symmetrical facial geometry matching guzelai.com Leyla reference)"
            ),
            "hair_tr": "Omuz hizasında dalgalı koyu kestane saçlar",
        },
        {
            "id": "valentina-cruz",
            "name": "Valentina Cruz",
            "badge": "guzelai.com • Valentina Cruz",
            "title_tr": "Lüks Yaşam & Haute Glamour Marka Yüzü (guzelai.com)",
            "avatar_url": "https://guzelai.com/assets/valentina_avatar.jpg",
            "face_prompt_en": (
                "official guzelai.com female supermodel Valentina Cruz (176cm Mediterranean-Italian brunette with "
                "long silky chestnut-brown wavy hair, hazel-green eyes, subtle natural freckles on cheeks, "
                "sun-kissed glowing skin matching guzelai.com Valentina Cruz reference)"
            ),
            "hair_tr": "Uzun ipeksi kestane dalgalı saçlar",
        },
        {
            "id": "aura-kaya",
            "name": "Aura Kaya",
            "badge": "guzelai.com • Aura Kaya",
            "title_tr": "İstanbul / Paris Haute Couture Podyum Yüzü (guzelai.com)",
            "avatar_url": "https://guzelai.com/influencers/aurakaya/avatar.jpg",
            "face_prompt_en": (
                "official guzelai.com female runway model Aura Kaya (178cm Turkish-Parisian supermodel with "
                "glossy dark chestnut wavy hair, sculpted cheekbones, luminous bronze glass-skin complexion "
                "matching guzelai.com Aura Kaya reference)"
            ),
            "hair_tr": "Parlak kestane dalgalı podyum saçı",
        },
        {
            "id": "elena-rostova",
            "name": "Elena Rostova",
            "badge": "guzelai.com • Elena Rostova",
            "title_tr": "Nordic Siren & Minimalist Haute Couture Modeli (guzelai.com)",
            "avatar_url": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=800&auto=format&fit=crop&q=85",
            "face_prompt_en": (
                "official guzelai.com female model Elena Rostova (180cm Nordic-European supermodel with sleek ash-platinum "
                "blonde blowout hair, piercing emerald-green eyes, sculpted symmetrical cheekbones)"
            ),
            "hair_tr": "Küllü platin ipeksi fön",
        },
        {
            "id": "selene-noir",
            "name": "Selene Noir",
            "badge": "guzelai.com • Selene Noir",
            "title_tr": "Milano / Paris Gece Zarafeti & İpek Musesi (guzelai.com)",
            "avatar_url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&auto=format&fit=crop&q=85",
            "face_prompt_en": (
                "official guzelai.com female model Selene Noir (180cm Italian-French editorial model with straight "
                "jet-black raven silk hair, satin porcelain skin, magnetic dark eyes)"
            ),
            "hair_tr": "Kuzguni siyah ipek düz saçlar",
        },
        {
            "id": "chloe-bennett",
            "name": "Chloe Bennett",
            "badge": "guzelai.com • Chloe Bennett",
            "title_tr": "Kaliforniya & Saint-Tropez Resort Marka Yüzü (guzelai.com)",
            "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800&auto=format&fit=crop&q=85",
            "face_prompt_en": (
                "official guzelai.com female model Chloe Bennett (176cm sun-kissed golden-blonde supermodel with "
                "voluminous honey-blonde waves, warm radiant smile, golden peach skin)"
            ),
            "hair_tr": "Güneşte açılmış dalgalı altın sarı saçlar",
        },
    ],
    "erkek": [
        {
            "id": "kenzo-takahashi",
            "name": "Kenzo Takahashi",
            "badge": "guzelai.com • Kenzo Takahashi",
            "title_tr": "Erkek Moda, Lüks Saat & Sartorial Kaban Yüzü (guzelai.com)",
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&auto=format&fit=crop&q=80",
            "face_prompt_en": (
                "official guzelai.com male supermodel Kenzo Takahashi (186cm charismatic Eurasian-Sartorial gentleman "
                "with classic side-parted jet-black hair, chiseled jawline, smooth skin, timeless Milan-Tokyo Old Money aura)"
            ),
            "hair_tr": "Klasik yandan ayrılmış siyah saç & keskin çene hattı",
        },
        {
            "id": "mateo-silva",
            "name": "Mateo Silva",
            "badge": "guzelai.com • Mateo Silva",
            "title_tr": "Akdeniz Sartorial & Dinamik Sokak Modası Yüzü (guzelai.com)",
            "avatar_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=500&auto=format&fit=crop&q=80",
            "face_prompt_en": (
                "official guzelai.com male supermodel Mateo Silva (185cm Mediterranean charismatic male model with "
                "textured short dark-brown wavy hair, sharp cheekbones, light groomed stubble, warm Mediterranean bronze skin)"
            ),
            "hair_tr": "Dokulu kısa kahve dalgalar & Akdeniz bronzu",
        },
    ],
    "kiz_cocuk": [
        {
            "id": "guzelai-ada-junior",
            "name": "Ada Güzel",
            "badge": "guzelai.com • Ada Güzel (Kids)",
            "title_tr": "Kız Çocuk Kolej & Kış Kapsül Marka Yüzü (guzelai.com)",
            "avatar_url": "https://guzelai.com/influencers/leyla/reference.png",
            "face_prompt_en": (
                "official guzelai.com junior girl fashion model Ada Güzel (8-year-old photorealistic real human child model "
                "with long wavy chestnut-brown hair, warm hazel eyes, cheerful natural smile, zero 3D/cartoon look)"
            ),
            "hair_tr": "Uzun dalgalı kestane saçlar",
        },
    ],
    "erkek_cocuk": [
        {
            "id": "guzelai-atlas-junior",
            "name": "Atlas Güzel",
            "badge": "guzelai.com • Atlas Güzel (Kids)",
            "title_tr": "Erkek Çocuk Urban Kolej & Kış Marka Yüzü (guzelai.com)",
            "avatar_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&auto=format&fit=crop&q=80",
            "face_prompt_en": (
                "official guzelai.com junior boy fashion model Atlas Güzel (8-year-old photorealistic real human boy model "
                "with neat side-parted sandy-brown hair, bright hazel-green eyes, warm confident smile, zero 3D/cartoon look)"
            ),
            "hair_tr": "Yandan ayrılmış kumral dokulu saçlar",
        },
    ],
}


def get_official_guzelai_model_for_segment(segment: str, index_hint: int = 0) -> Dict[str, Any]:
    """Returns the official `guzelai.com` model for the given segment (`kadin`, `erkek`, `kiz_cocuk`, `erkek_cocuk`)."""
    seg = (segment or "kadin").strip().lower()
    roster = GUZELAI_COM_OFFICIAL_MODELS.get(seg) or GUZELAI_COM_OFFICIAL_MODELS["kadin"]
    return roster[index_hint % len(roster)]


def enforce_guzelai_official_model_lock(outfit: Dict[str, Any], index_hint: int = 0) -> Dict[str, Any]:
    """
    Ensures the outfit dictionary is strictly bound to an official `guzelai.com` model.
    Replaces any non-guzelai.com model name or face description.
    """
    seg = (outfit.get("gender_segment") or "kadin").strip().lower()
    roster = GUZELAI_COM_OFFICIAL_MODELS.get(seg) or GUZELAI_COM_OFFICIAL_MODELS["kadin"]
    valid_ids = {m["id"] for m in roster}

    cur_id = outfit.get("guzelai_model_id", "")
    if cur_id in valid_ids:
        selected = next(m for m in roster if m["id"] == cur_id)
    else:
        arch_id = (outfit.get("archetype_id") or outfit.get("id") or "").lower()
        name_matched = next(
            (m for m in roster if m["name"].split()[0].lower() in arch_id or m["id"].lower() in arch_id),
            None,
        )
        if name_matched:
            selected = name_matched
        else:
            h_val = sum(ord(c) for c in arch_id) if arch_id else index_hint
            selected = roster[h_val % len(roster)]

    outfit["guzelai_model_id"] = selected["id"]
    outfit["guzelai_model_name"] = selected["name"]
    outfit["guzelai_model_badge"] = selected["badge"]
    outfit["guzelai_model_title"] = selected["title_tr"]
    outfit["guzelai_face_prompt_en"] = selected["face_prompt_en"]
    outfit["is_3d_avatar"] = False
    outfit["ai_model_verified"] = True
    return outfit
