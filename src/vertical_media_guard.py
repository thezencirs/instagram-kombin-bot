"""
GüzelAI Holding A.Ş. — %100 Dikey (9:16 Portrait) Fotoğraf & Video Zorunlu Kalite Kilidi
(`src/vertical_media_guard.py`)
========================================================================================
Telegram (@guzelaibot) ve Instagram (@guzelaicom) paylaşımlarında yatay (16:9 / 4:3) veya
kare (1:1) medya gönderimini %100 engeller; tüm fotoğraf ve videoların tam dikey 9:16
(1440x2560 2K QHD+ veya 1080x1920 Full HD, SAR 1:1, DAR 9:16) formatında olmasını garanti eder.
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def _get_ffmpeg_bin() -> str:
    ff = shutil.which("ffmpeg")
    if ff:
        return ff
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def fit_pil_to_vertical_9x16(
    img: Image.Image,
    target_w: int = 1440,
    target_h: int = 2560,
) -> Image.Image:
    """
    Herhangi bir PIL görselini deformasyon (sündürme) olmadan tam 9:16 dikey (1440x2560) boyuta getirir.
    - Zaten dikey portre ise (h > w ve oran ~9:16'ya yakınsa) akıllı merkez kırpma (ImageOps.fit) uygular.
    - Kare veya yatay ise bulanıklaştırılmış lüks dikey stüdyo arka planı üzerine tam ortalayarak yerleştirir.
    """
    im = ImageOps.exif_transpose(img).convert("RGB")
    w, h = im.size
    if w <= 0 or h <= 0:
        return Image.new("RGB", (target_w, target_h), (18, 16, 20))

    ratio = w / float(h)
    target_ratio = target_w / float(target_h)  # 0.5625 (9:16)

    if (w, h) == (target_w, target_h):
        return im

    # Dikey portre görseller (ör. 768x1344, 768x1376, 1080x1920): Baş ve ayakkabıyı koruyarak 9:16'ya oturt
    if h > w and abs(ratio - target_ratio) <= 0.10:
        return ImageOps.fit(
            im,
            (target_w, target_h),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.38),
        )

    # Kare (1:1), 4:5 veya Yatay (16:9) görseller: Kesilme olmaması için 9:16 ambiyans tuvaline yerleştir
    bg = ImageOps.fit(
        im,
        (target_w, target_h),
        method=Image.Resampling.BICUBIC,
        centering=(0.5, 0.5),
    )
    bg = bg.filter(ImageFilter.GaussianBlur(radius=36))
    bg = ImageEnhance.Brightness(bg).enhance(0.42)

    fg = im.copy()
    fg.thumbnail((target_w - 48, target_h - 120), Image.Resampling.LANCZOS)
    px = (target_w - fg.width) // 2
    py = (target_h - fg.height) // 2
    bg.paste(fg, (px, py))
    return bg


def ensure_vertical_photo(
    photo_path: str | Path,
    target_w: int = 1440,
    target_h: int = 2560,
) -> Path:
    """
    Telegram ve Instagram'a gönderilecek fotoğrafın %100 dikey 9:16 (h > w) olduğunu doğrular.
    Dikey 9:16 değilse otomatik olarak kayıpsız 9:16 dikey versiyonunu üretip onun yolunu döndürür.
    """
    src = Path(photo_path)
    if not src.exists():
        return src

    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    w, h = im.size
    ratio = w / float(max(1, h))
    if h > w and abs(ratio - (9.0 / 16.0)) <= 0.02 and w >= 1080:
        return src

    vertical_im = fit_pil_to_vertical_9x16(im, target_w=target_w, target_h=target_h)
    out_path = src.with_name(f"{src.stem}_vertical_9x16.jpg")
    vertical_im.save(out_path, format="JPEG", quality=97, subsampling=0)
    return out_path


def get_video_dimensions(video_path: str | Path) -> Tuple[int, int]:
    """Videonun gerçek piksel (width, height) değerlerini okur."""
    try:
        import cv2
        cap = cv2.VideoCapture(str(video_path))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        if w > 0 and h > 0:
            return w, h
    except Exception:
        pass
    return 1440, 2560


def ensure_vertical_video(
    video_path: str | Path,
    target_w: int = 1440,
    target_h: int = 2560,
) -> Tuple[Path, int, int]:
    """
    Telegram ve Instagram'a yüklenecek videonun %100 dikey 9:16 (height > width, DAR 9:16, SAR 1:1)
    olduğunu denetler. Eğer yatay veya kare bir video gelirse otomatik olarak 9:16 dikey formata çevirir.
    """
    src = Path(video_path)
    if not src.exists():
        return src, target_w, target_h

    w, h = get_video_dimensions(src)
    ratio = w / float(max(1, h))
    if h > w and abs(ratio - (9.0 / 16.0)) <= 0.025:
        return src, w, h

    out_mp4 = src.with_name(f"{src.stem}_vertical_9x16.mp4")
    ffmpeg_bin = _get_ffmpeg_bin()
    vf_complex = (
        f"[0:v]split=2[bg][fg];"
        f"[bg]scale={target_w}:{target_h}:force_original_aspect_ratio=increase,"
        f"crop={target_w}:{target_h},boxblur=28:4,eq=brightness=-0.14[bg2];"
        f"[fg]scale={target_w}:{target_h}:force_original_aspect_ratio=decrease[fg2];"
        f"[bg2][fg2]overlay=(W-w)/2:(H-h)/2,setsar=1:1[v]"
    )
    cmd = [
        ffmpeg_bin, "-y",
        "-i", str(src),
        "-filter_complex", vf_complex,
        "-map", "[v]",
        "-map", "0:a?",
        "-aspect", "9:16",
        "-c:v", "libx264",
        "-preset", "fast",
        "-profile:v", "high",
        "-crf", "14",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-metadata", "encoder=Apple QuickTime",
        "-c:a", "aac", "-b:a", "256k",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_mp4, target_w, target_h


def build_telegram_vertical_thumbnail(
    cover_photo_path: Optional[Path],
    video_path: Optional[Path],
    out_dir: str | Path,
) -> Optional[Path]:
    """
    Telegram mobil/masaüstü oynatıcısının videoyu tam ekran 9:16 dikey kart olarak göstermesi için
    Telegram API standardına uygun (180x320, <200KB, 9:16 dikey JPEG) kapak küçük resmi üretir.
    """
    out_p = Path(out_dir) / "_tg_vertical_thumb_180x320.jpg"
    src_im: Optional[Image.Image] = None

    if cover_photo_path and Path(cover_photo_path).exists():
        try:
            src_im = Image.open(cover_photo_path).convert("RGB")
        except Exception:
            src_im = None

    if src_im is None and video_path and Path(video_path).exists():
        try:
            import cv2
            cap = cv2.VideoCapture(str(video_path))
            ret, bgr = cap.read()
            cap.release()
            if ret and bgr is not None:
                src_im = Image.fromarray(bgr[:, :, ::-1], mode="RGB")
        except Exception:
            src_im = None

    if src_im is None:
        return None

    thumb_9x16 = fit_pil_to_vertical_9x16(src_im, target_w=180, target_h=320)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    thumb_9x16.save(out_p, format="JPEG", quality=88, optimize=True)
    return out_p
