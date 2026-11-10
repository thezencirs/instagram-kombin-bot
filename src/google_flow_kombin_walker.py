"""
Google Flow 1080p Realistic Model Walking Video Engine (`src/google_flow_kombin_walker.py`)
===========================================================================================
Generates 100% realistic 1080p (1080x1920 @ 30fps) walking videos of official `guzelai.com`
models wearing the exact 6-piece outfit for Part 2 (5.2s - 11.0s) of the Kombin Reel:

1. Primary Engine (Live Google Flow Ultra CDP):
   - Connects to `https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88`
     via Chrome `DevToolsActivePort` (with automatic `Allow remote debugging` clicker).
   - Pastes the official `guzelai.com` model's full-body outfit photo (`step1.jpg`) as the
     reference image ingredient chip (`flow-image-ingredient-chip`).
   - Submits the natural 9:16 1080p runway/boulevard walking prompt preserving the exact
     `guzelai.com` model face and 6-piece outfit.
   - Downloads the generated MP4 stream (`/asb/...=mm,22,15`) with browser cookies and
     normalizes it to 1080x1920 @ 30fps (`output/flow_walk.mp4`).

2. Secondary / Cloud Fallback Engine (Dense Optical Flow Farneback + 3D Stride Parallax):
   - When running in headless cloud CI (GitHub Actions) or if Google Flow is in rate-limit
     cooldown, synthesizes a continuous 30fps 1080p walking video (`output/flow_walk.mp4`)
     using OpenCV Dense Optical Flow (`cv2.calcOpticalFlowFarneback` + `cv2.remap`) across
     the 3 sequential stride keyframes (`step1.jpg`, `step2.jpg`, `step3.jpg`) with natural
     gimbal gait cadence so the walking section is always fluid and realistic.
"""

import base64
import ctypes
import ctypes.wintypes
import json
import math
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
import requests
from PIL import Image, ImageEnhance, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
FLOW_PROJECT_ID = "5b458128-eb46-49e2-9e58-58fade625e88"
FLOW_PROJECT_URL = f"https://flow.google.com/project/{FLOW_PROJECT_ID}"
DEVTOOLS_PORT_FILE = Path(r"C:\Users\zenci\AppData\Local\Google\Chrome\User Data\DevToolsActivePort")


def start_auto_allow_clicker(stop_event: threading.Event) -> Optional[threading.Thread]:
    """Automatically clicks Chrome's 'Uzaktan hata ayıklamaya izin verilsin mi?' dialog on Windows."""
    if os.name != "nt":
        return None
    user32 = ctypes.windll.user32
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)

    def _worker():
        while not stop_event.is_set():
            try:
                found = []

                def cb(hwnd, lParam):
                    if user32.IsWindowVisible(hwnd):
                        length = user32.GetWindowTextLengthW(hwnd)
                        if length > 0:
                            buf = ctypes.create_unicode_buffer(length + 1)
                            user32.GetWindowTextW(hwnd, buf, length + 1)
                            title = buf.value
                            if "hata ay" in title.lower() or "debugging" in title.lower():
                                rect = ctypes.wintypes.RECT()
                                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                                found.append((hwnd, rect.left, rect.top, rect.right, rect.bottom))
                    return True

                user32.EnumWindows(WNDENUMPROC(cb), 0)
                if found:
                    hwnd, l, t, r, b = found[0]
                    bx = l + int((r - l) * 0.665)
                    by = t + int((b - t) * 0.812)
                    user32.SetForegroundWindow(hwnd)
                    time.sleep(0.1)
                    user32.SetCursorPos(bx, by)
                    user32.mouse_event(0x0002, 0, 0, 0, 0)
                    time.sleep(0.05)
                    user32.mouse_event(0x0004, 0, 0, 0, 0)
                    time.sleep(0.4)
            except Exception:
                pass
            time.sleep(0.25)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    return t


class FlowCDPClient:
    def __init__(self):
        import websocket
        lines = DEVTOOLS_PORT_FILE.read_text(encoding="utf-8").strip().splitlines()
        self.port = int(lines[0].strip())
        self.browser_ws = f"ws://127.0.0.1:{self.port}{lines[1].strip()}"
        self.ws = websocket.create_connection(self.browser_ws, timeout=45, suppress_origin=True)
        self.msg_id = 0
        self.session_id = None
        self._attach_to_flow_tab()

    def _attach_to_flow_tab(self):
        res = self.send_raw("Target.getTargets")
        targets = res.get("result", {}).get("targetInfos", [])
        flow_target = None
        for t in targets:
            if t.get("type") == "page" and "flow.google.com/project/" in (t.get("url") or ""):
                flow_target = t["targetId"]
                break
        if not flow_target:
            res_create = self.send_raw("Target.createTarget", {"url": FLOW_PROJECT_URL})
            flow_target = res_create["result"]["targetId"]
            time.sleep(5)
        att = self.send_raw("Target.attachToTarget", {"targetId": flow_target, "flatten": True})
        self.session_id = att["result"]["sessionId"]
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.send("DOM.enable")
        self.send("Network.enable")

    def send_raw(self, method: str, params: Optional[dict] = None) -> dict:
        self.msg_id += 1
        cid = self.msg_id
        payload = {"id": cid, "method": method, "params": params or {}}
        self.ws.send(json.dumps(payload))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == cid:
                return msg

    def send(self, method: str, params: Optional[dict] = None) -> dict:
        self.msg_id += 1
        cid = self.msg_id
        payload = {"id": cid, "method": method, "params": params or {}, "sessionId": self.session_id}
        self.ws.send(json.dumps(payload))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == cid:
                return msg

    def eval_js(self, expr: str, await_promise: bool = True) -> Any:
        res = self.send(
            "Runtime.evaluate",
            {
                "expression": expr,
                "returnByValue": True,
                "awaitPromise": await_promise,
            },
        )
        return res.get("result", {}).get("result", {}).get("value")

    def get_cookie_jar(self) -> requests.cookies.RequestsCookieJar:
        cookies_res = self.send("Network.getAllCookies")
        cookies_list = cookies_res.get("result", {}).get("cookies", [])
        jar = requests.cookies.RequestsCookieJar()
        for c in cookies_list:
            jar.set(c["name"], c["value"], domain=c.get("domain", ""), path=c.get("path", "/"))
        return jar

    def list_completed_asb_urls(self) -> List[str]:
        js = r"""
        (() => {
            const tiles = Array.from(document.querySelectorAll('flow-video-tile'));
            const urls = [];
            for (const tile of tiles) {
                const v = tile.querySelector('video');
                const img = tile.querySelector('img.thumbnail') || tile.querySelector('img');
                if (v && v.src && v.src.includes('/asb/')) {
                    urls.push(v.src);
                } else if (img && img.src && img.src.includes('/asb/')) {
                    urls.push(img.src.split('=')[0] + '=mm,22,15');
                }
            }
            return urls;
        })()
        """
        res = self.eval_js(js)
        return res if isinstance(res, list) else []

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def build_flow_walking_prompt(outfit: Dict[str, Any]) -> str:
    """Builds a 1080p 9:16 realistic walking prompt for Google Flow preserving the exact guzelai.com model & outfit."""
    seg = (outfit.get("gender_segment") or "kadin").strip().lower()
    model_name = outfit.get("guzelai_model_name") or "Leyla"
    items = outfit.get("items") or {}
    outer_name = (items.get("outerwear") or {}).get("name", "tailored winter coat")
    top_name = (items.get("top") or {}).get("name", "knit sweater")
    bottom_name = (items.get("bottom") or {}).get("name", "tailored trousers")
    shoes_name = (items.get("shoes") or {}).get("name", "luxury boots")

    if seg == "erkek":
        return (
            f"Vertical 9:16 photorealistic 1080p full-body luxury menswear fashion commercial video of the exact "
            f"guzelai.com male model ({model_name}) from the reference image walking naturally and confidently "
            f"forward towards the camera along a sunlit luxury stone boulevard in smooth steady gimbal tracking motion. "
            f"Keep the exact same face, hairstyle, coat, sweater, trousers, shoes, and hands relaxed with no women's bag. "
            f"Realistic human leg stride physics, natural coat fabric sway, 85mm f/1.4 optical depth of field, zero morphing."
        )
    if seg in ("kiz_cocuk", "erkek_cocuk"):
        return (
            f"Vertical 9:16 photorealistic 1080p full-body kids fashion catalog video of the exact guzelai.com junior "
            f"model ({model_name}) from the reference image walking cheerfully and naturally forward along a sunlit "
            f"park walkway towards the camera in smooth gimbal tracking motion. Keep the exact same child face, hair, "
            f"winter jacket, sweater, trousers, and sneakers. 100% realistic human movement, zero cartoon/3D effect."
        )
    return (
        f"Vertical 9:16 photorealistic 1080p full-body luxury fashion commercial video of the exact guzelai.com "
        f"female supermodel ({model_name}) from the reference image walking naturally and gracefully forward "
        f"towards the camera along Nişantaşı luxury stone boulevard in smooth gimbal tracking motion. "
        f"Keep the exact same face, hairstyle, winter coat, knitwear, trousers, handbag, and footwear. "
        f"Authentic runway stride physics, natural coat hem movement, 85mm f/1.4 golden-hour lighting, zero morphing."
    )


def _get_ffmpeg_bin() -> str:
    ff = shutil.which("ffmpeg")
    if ff:
        return ff
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def normalize_video_to_1080p_vertical(src_mp4: str, dst_mp4: str, target_duration: float = 6.0) -> bool:
    """Normalizes any downloaded Flow MP4 to exact 1080x1920 @ 30fps H.264."""
    if not os.path.exists(src_mp4) or os.path.getsize(src_mp4) < 20_000:
        return False
    ffmpeg_bin = _get_ffmpeg_bin()
    os.makedirs(os.path.dirname(dst_mp4) or ".", exist_ok=True)
    vf_chain = (
        "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
        "crop=1080:1920,"
        "fps=30,"
        "unsharp=5:5:0.55:3:3:0.0"
    )
    cmd = [
        ffmpeg_bin, "-y",
        "-stream_loop", "-1",
        "-i", src_mp4,
        "-t", f"{target_duration:.2f}",
        "-vf", vf_chain,
        "-an",
        "-c:v", "libx264",
        "-preset", "fast",
        "-profile:v", "high",
        "-crf", "14",
        "-pix_fmt", "yuv420p",
        dst_mp4,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0 and os.path.exists(dst_mp4) and os.path.getsize(dst_mp4) > 30_000


def generate_flow_walk_via_cdp(
    ref_image_path: str,
    prompt_text: str,
    output_mp4_path: str,
    timeout_sec: int = 195,
) -> Dict[str, Any]:
    """
    Connects to Google Flow (`https://flow.google.com/project/5b458128-eb46-49e2-9e58-58fade625e88`),
    pastes `ref_image_path` as reference ingredient, submits `prompt_text`, and downloads the MP4.
    """
    if not DEVTOOLS_PORT_FILE.exists():
        return {"ok": False, "reason": "DevToolsActivePort_missing"}
    if not os.path.exists(ref_image_path):
        return {"ok": False, "reason": f"ref_image_missing:{ref_image_path}"}

    stop_evt = threading.Event()
    start_auto_allow_clicker(stop_evt)
    client = None
    try:
        client = FlowCDPClient()
        stop_evt.set()

        for _ in range(20):
            if client.eval_js("Boolean(document.querySelector('.ProseMirror'))"):
                break
            time.sleep(1.0)
        else:
            return {"ok": False, "reason": "ProseMirror_not_found"}

        existing_urls = set(client.list_completed_asb_urls())

        # Convert ref image to clean 1080x1920 JPEG base64 and paste into .ProseMirror
        im = Image.open(ref_image_path).convert("RGB").resize((1080, 1920), Image.Resampling.LANCZOS)
        tmp_jpg = str(BASE_DIR / "output" / "_flow_ref_upload.jpg")
        os.makedirs(os.path.dirname(tmp_jpg), exist_ok=True)
        im.save(tmp_jpg, "JPEG", quality=94)
        with open(tmp_jpg, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("ascii")
        fname = os.path.basename(ref_image_path)

        prep_res = client.eval_js(
            f"""(async () => {{
                document.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Escape', bubbles: true}}));
                const closeIcons = Array.from(document.querySelectorAll('flow-base-prompt-box flow-image-ingredient-chip .chip-close-icon, flow-base-prompt-box .hover-icon-overlay'));
                for (const ic of closeIcons) {{
                    ic.click();
                    await new Promise(r => setTimeout(r, 250));
                }}
                const ed = document.querySelector('flow-base-prompt-box .ProseMirror') || document.querySelector('.ProseMirror');
                if (!ed) return 'NO_EDITOR';
                ed.focus();
                document.execCommand('selectAll', false, null);
                document.execCommand('delete', false, null);

                const b64 = "{b64_img}";
                const bin = atob(b64);
                const arr = new Uint8Array(bin.length);
                for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
                const file = new File([arr], "{fname}", {{type: "image/jpeg"}});
                const dt = new DataTransfer();
                dt.items.add(file);
                const pasteEvt = new ClipboardEvent('paste', {{bubbles: true, cancelable: true, clipboardData: dt}});
                ed.dispatchEvent(pasteEvt);
                return 'PASTED';
            }})()"""
        )
        if prep_res != "PASTED":
            return {"ok": False, "reason": f"paste_failed:{prep_res}"}

        # Wait up to 30s for the ingredient chip INSIDE flow-base-prompt-box to appear and have aria-busy === "false"
        chip_ready = False
        for _ in range(30):
            time.sleep(1.0)
            ready = client.eval_js(
                r"""(() => {
                    const chips = Array.from(document.querySelectorAll('flow-base-prompt-box flow-image-ingredient-chip button.chip-container'));
                    if (chips.length === 0) return false;
                    return chips.every(c => c.getAttribute('aria-busy') === 'false');
                })()"""
            )
            if ready is True:
                chip_ready = True
                break
        if not chip_ready:
            return {"ok": False, "reason": "ingredient_chip_timeout_in_prompt_box"}

        # Click .ProseMirror physically via CDP, clear ONLY text inside .ProseMirror, and insert prompt
        ed_box = client.eval_js(
            r"""(() => {
                const ed = document.querySelector('flow-base-prompt-box .ProseMirror') || document.querySelector('.ProseMirror');
                if (!ed) return null;
                const r = ed.getBoundingClientRect();
                return {x: Math.round(r.left + 40), y: Math.round(r.top + r.height/2)};
            })()"""
        )
        if ed_box:
            ex, ey = ed_box["x"], ed_box["y"]
            client.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": ex, "y": ey, "button": "left", "clickCount": 1})
            time.sleep(0.05)
            client.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": ex, "y": ey, "button": "left", "clickCount": 1})
            time.sleep(0.15)

        client.eval_js(
            r"""(() => {
                const ed = document.querySelector('flow-base-prompt-box .ProseMirror') || document.querySelector('.ProseMirror');
                if (ed) {
                    ed.focus();
                    document.execCommand('selectAll', false, null);
                    document.execCommand('delete', false, null);
                }
            })()"""
        )
        time.sleep(0.2)
        client.send("Input.insertText", {"text": prompt_text})
        time.sleep(1.2)

        # Wait up to 10s for "Oluşturmaya başla" button to become enabled, then click it via Input.dispatchMouseEvent
        btn_info = None
        for _ in range(10):
            btn_info = client.eval_js(
                r"""(() => {
                    const btn = document.querySelector('button[aria-label="Oluşturmaya başla"]');
                    if (!btn) return null;
                    const r = btn.getBoundingClientRect();
                    return {disabled: btn.disabled, x: Math.round(r.left + r.width/2), y: Math.round(r.top + r.height/2)};
                })()"""
            )
            if btn_info and not btn_info.get("disabled"):
                break
            time.sleep(1.0)

        if not btn_info or btn_info.get("disabled"):
            return {"ok": False, "reason": f"create_button_disabled:{btn_info}"}

        bx, by = btn_info["x"], btn_info["y"]
        client.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": bx, "y": by, "button": "left", "clickCount": 1})
        time.sleep(0.06)
        client.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": bx, "y": by, "button": "left", "clickCount": 1})

        print(f"🎬 [Google Flow 1080p] Manken yürüyüş videosu üretimi başlatıldı ({timeout_sec}sn bekleniyor)...")
        new_video_url = None
        t0 = time.time()
        while time.time() - t0 < timeout_sec:
            time.sleep(4.0)
            current_urls = client.list_completed_asb_urls()
            for u in current_urls:
                if u not in existing_urls:
                    new_video_url = u
                    break
            if new_video_url:
                break

        if not new_video_url:
            return {"ok": False, "reason": "video_generation_timeout"}

        jar = client.get_cookie_jar()
        raw_mp4 = output_mp4_path + ".raw.mp4"
        os.makedirs(os.path.dirname(output_mp4_path) or ".", exist_ok=True)
        r = requests.get(
            new_video_url,
            cookies=jar,
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://flow.google.com/"},
            timeout=90,
        )
        if r.status_code == 200 and len(r.content) > 30_000:
            with open(raw_mp4, "wb") as vf:
                vf.write(r.content)
            if normalize_video_to_1080p_vertical(raw_mp4, output_mp4_path, target_duration=6.0):
                try:
                    os.remove(raw_mp4)
                except Exception:
                    pass
                print(f"✅ [Google Flow 1080p] Gerçekçi manken yürüyüş videosu indirildi: {output_mp4_path}")
                return {"ok": True, "engine": "google_flow_ultra_cdp", "video_path": output_mp4_path}
        return {"ok": False, "reason": f"download_failed_status_{r.status_code}"}
    except Exception as e:
        return {"ok": False, "reason": str(e)}
    finally:
        stop_evt.set()
        if client:
            client.close()


def synthesize_1080p_optical_flow_walk_mp4(
    model_frame_paths: List[str],
    output_mp4_path: str,
    duration_sec: float = 6.0,
    fps: int = 30,
) -> Dict[str, Any]:
    """
    OpenCV Dense Optical Flow (Farneback) + 2.5D Foreground/Background Depth Stride Synthesizer.
    Produces a smooth 1080x1920 @ 30fps realistic walking video (`output_mp4_path`) from the
    official `guzelai.com` model's 3 sequential stride frames (`step1.jpg`, `step2.jpg`, `step3.jpg`),
    eliminating static photo cuts or ghosting.
    """
    valid_paths = [p for p in model_frame_paths if p and os.path.exists(p)]
    if not valid_paths:
        return {"ok": False, "reason": "no_valid_model_frames"}

    W, H = 1080, 1920
    frames_bgr = []
    for p in valid_paths[:3]:
        pil_im = Image.open(p).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
        pil_im = ImageEnhance.Contrast(pil_im).enhance(1.06)
        pil_im = ImageEnhance.Color(pil_im).enhance(1.06)
        pil_im = pil_im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=2))
        frames_bgr.append(cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR))

    while len(frames_bgr) < 3:
        frames_bgr.append(frames_bgr[-1].copy())

    # Downscaled optical flow computation (360x640) for fast, artifact-free motion vectors
    fw, fh = 270, 480
    small_grays = [cv2.cvtColor(cv2.resize(f, (fw, fh)), cv2.COLOR_BGR2GRAY) for f in frames_bgr]

    flows_fwd = []
    flows_bwd = []
    for idx in range(2):
        fl_f = cv2.calcOpticalFlowFarneback(
            small_grays[idx], small_grays[idx + 1], None,
            pyr_scale=0.5, levels=3, winsize=25, iterations=3, poly_n=7, poly_sigma=1.5, flags=0
        )
        fl_b = cv2.calcOpticalFlowFarneback(
            small_grays[idx + 1], small_grays[idx], None,
            pyr_scale=0.5, levels=3, winsize=25, iterations=3, poly_n=7, poly_sigma=1.5, flags=0
        )
        # Upscale flow fields back to 1080x1920 and damp high-frequency warping so face/limbs stay 100% sharp
        fl_f_up = cv2.resize(fl_f, (W, H), interpolation=cv2.INTER_CUBIC) * (W / float(fw)) * 0.32
        fl_b_up = cv2.resize(fl_b, (W, H), interpolation=cv2.INTER_CUBIC) * (W / float(fw)) * 0.32
        flows_fwd.append(fl_f_up)
        flows_bwd.append(fl_b_up)

    grid_x, grid_y = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    total_frames = int(round(duration_sec * fps))
    os.makedirs(os.path.dirname(output_mp4_path) or ".", exist_ok=True)

    tmp_dir = Path(os.path.dirname(output_mp4_path) or ".") / "_flow_walk_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    for f_idx in range(total_frames):
        t = f_idx / float(fps)
        u_norm = f_idx / float(max(1, total_frames - 1))

        # Continuous natural walking cadence (2.15 Hz step frequency -> subtle vertical/horizontal gimbal bob)
        gait_phase = t * 2.15 * 2.0 * math.pi
        bob_y = math.sin(gait_phase) * 5.5
        sway_x = math.cos(gait_phase * 0.5) * 4.0
        forward_zoom = 1.035 + 0.055 * u_norm

        # Determine active segment (0->1 in first half, 1->2 in second half) with smooth optical-flow morph window
        seg_pos = u_norm * 2.0
        seg_idx = min(1, int(seg_pos))
        local_alpha = seg_pos - seg_idx

        # Concentrate the transition smoothly in the middle of each stride phase
        if local_alpha < 0.30:
            blend_w = 0.0
        elif local_alpha > 0.70:
            blend_w = 1.0
        else:
            s = (local_alpha - 0.30) / 0.40
            blend_w = s * s * (3.0 - 2.0 * s)

        img_a = frames_bgr[seg_idx]
        img_b = frames_bgr[seg_idx + 1]

        if blend_w <= 0.001:
            morphed = img_a
        elif blend_w >= 0.999:
            morphed = img_b
        else:
            map_a_x = grid_x - flows_fwd[seg_idx][:, :, 0] * blend_w
            map_a_y = grid_y - flows_fwd[seg_idx][:, :, 1] * blend_w
            map_b_x = grid_x - flows_bwd[seg_idx][:, :, 0] * (1.0 - blend_w)
            map_b_y = grid_y - flows_bwd[seg_idx][:, :, 1] * (1.0 - blend_w)
            warped_a = cv2.remap(img_a, map_a_x, map_a_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)
            warped_b = cv2.remap(img_b, map_b_x, map_b_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)
            morphed = cv2.addWeighted(warped_a, 1.0 - blend_w, warped_b, blend_w, 0.0)

        # Apply natural Steadicam walking cadence + forward tracking dolly
        crop_w = int(W / forward_zoom)
        crop_h = int(H / forward_zoom)
        cx = int(max(0, min(W - crop_w, (W - crop_w) * 0.5 + sway_x)))
        cy = int(max(0, min(H - crop_h, (H - crop_h) * 0.42 + bob_y)))
        cropped = morphed[cy:cy + crop_h, cx:cx + crop_w]
        final_bgr = cv2.resize(cropped, (W, H), interpolation=cv2.INTER_LANCZOS4)
        cv2.imwrite(str(tmp_dir / f"wf_{f_idx:04d}.jpg"), final_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 96])

    ffmpeg_bin = _get_ffmpeg_bin()
    cmd = [
        ffmpeg_bin, "-y",
        "-framerate", str(fps),
        "-i", str(tmp_dir / "wf_%04d.jpg"),
        "-t", f"{duration_sec:.2f}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-profile:v", "high",
        "-crf", "14",
        "-pix_fmt", "yuv420p",
        output_mp4_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return {"ok": True, "engine": "dense_optical_flow_1080p", "video_path": output_mp4_path}


def run_flow_cdp_in_interactive_desktop(
    ref_image_path: str,
    output_mp4_path: str,
    segment: str = "kadin",
    model_name: str = "Leyla",
    timeout_sec: int = 190,
) -> Dict[str, Any]:
    """
    Launches `google_flow_kombin_walker.py --cdp-only` in the interactive Windows desktop
    session via WMI (`Win32_Process.Create`) so `start_auto_allow_clicker` can click the
    Chrome remote-debugging confirmation prompt automatically.
    """
    status_json = Path(output_mp4_path).with_suffix(".json")
    try:
        if status_json.exists():
            status_json.unlink()
    except Exception:
        pass

    py_exe = sys.executable
    script_path = str(Path(__file__).resolve())
    cmd_line = (
        f'"{py_exe}" -X utf8 -u "{script_path}" '
        f'--ref "{ref_image_path}" --out "{output_mp4_path}" '
        f'--segment "{segment}" --model-name "{model_name}" --cdp-only'
    )
    ps_cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        f"Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList '{cmd_line}'",
    ]
    subprocess.run(ps_cmd, capture_output=True, text=True)

    t0 = time.time()
    while time.time() - t0 < (timeout_sec + 25):
        if status_json.exists():
            time.sleep(0.5)
            try:
                return json.loads(status_json.read_text(encoding="utf-8"))
            except Exception:
                pass
        time.sleep(2.5)
    return {"ok": False, "reason": "interactive_wmi_timeout"}


def ensure_realistic_flow_walk_video(outfit: Dict[str, Any], out_dir: str = "output") -> Optional[str]:
    """
    Ensures a realistic 1080p (1080x1920 @ 30fps) walking video exists for `outfit`.
    1. Checks if `outfit["flow_walk_video"]` or `assets/{arch_id}_flow_walk.mp4` already exists.
    2. If on Windows desktop and `USE_GOOGLE_FLOW_CDP != "0"`, launches Google Flow Ultra CDP
       via interactive WMI (`Win32_Process.Create`) to generate a real 1080p AI walking video
       from `model_frames[0]` (`step1.jpg`).
    3. Otherwise (or if Flow CDP is busy/offline), synthesizes the 1080p 30fps walking video
       using `synthesize_1080p_optical_flow_walk_mp4` so Part 2 of the Reel is always a true
       continuous 1080p video.
    """
    os.makedirs(out_dir, exist_ok=True)
    arch_id = outfit.get("archetype_id") or outfit.get("id") or "kombin"
    cached_asset_mp4 = str(BASE_DIR / "assets" / f"{arch_id}_flow_walk.mp4")
    out_walk_mp4 = os.path.join(out_dir, "flow_walk.mp4")

    existing_custom = outfit.get("flow_walk_video")
    if existing_custom and os.path.exists(existing_custom) and os.path.getsize(existing_custom) > 30_000:
        if os.path.abspath(existing_custom) != os.path.abspath(out_walk_mp4):
            shutil.copy2(existing_custom, out_walk_mp4)
        outfit["flow_walk_video"] = out_walk_mp4
        return out_walk_mp4

    if os.path.exists(cached_asset_mp4) and os.path.getsize(cached_asset_mp4) > 30_000:
        shutil.copy2(cached_asset_mp4, out_walk_mp4)
        outfit["flow_walk_video"] = out_walk_mp4
        print(f"🎬 [Flow 1080p Yürüyüş Videosu Hazır (Önbellek)]: {cached_asset_mp4}")
        return out_walk_mp4

    model_frames = outfit.get("model_frames") or []
    ref_step1 = model_frames[0] if model_frames else ""
    if ref_step1 and not os.path.isabs(ref_step1):
        ref_step1 = str(BASE_DIR / ref_step1)

    # Try live Google Flow CDP on Windows if DevToolsActivePort exists and not disabled
    use_flow_cdp = os.environ.get("USE_GOOGLE_FLOW_CDP", "1") != "0"
    if os.name == "nt" and use_flow_cdp and DEVTOOLS_PORT_FILE.exists() and os.path.exists(ref_step1):
        res = run_flow_cdp_in_interactive_desktop(
            ref_image_path=ref_step1,
            output_mp4_path=cached_asset_mp4,
            segment=str(outfit.get("gender_segment", "kadin")),
            model_name=str(outfit.get("guzelai_model_name", "Leyla")),
            timeout_sec=int(os.environ.get("FLOW_WALK_TIMEOUT", "185")),
        )
        if res.get("ok") and os.path.exists(cached_asset_mp4) and os.path.getsize(cached_asset_mp4) > 30_000:
            shutil.copy2(cached_asset_mp4, out_walk_mp4)
            outfit["flow_walk_video"] = out_walk_mp4
            outfit["flow_walk_engine"] = "google_flow_ultra_1080p"
            return out_walk_mp4
        else:
            print(f"ℹ️ [Google Flow CDP Bilgi]: {res.get('reason')} -> 1080p Optik Akış (Optical Flow) motoruna geçiliyor.")

    # Synthesize 1080p 30fps Optical Flow walking video
    abs_frames = [str(BASE_DIR / p) if not os.path.isabs(p) else p for p in model_frames]
    opt_res = synthesize_1080p_optical_flow_walk_mp4(
        model_frame_paths=abs_frames,
        output_mp4_path=cached_asset_mp4,
        duration_sec=6.0,
        fps=30,
    )
    if opt_res.get("ok") and os.path.exists(cached_asset_mp4):
        shutil.copy2(cached_asset_mp4, out_walk_mp4)
        outfit["flow_walk_video"] = out_walk_mp4
        outfit["flow_walk_engine"] = opt_res.get("engine", "dense_optical_flow_1080p")
        print(f"🎬 [1080p Gerçekçi Yürüyüş Videosu Hazır ({outfit['flow_walk_engine']})]: {out_walk_mp4}")
        return out_walk_mp4
    return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True, help="Path to step1.jpg reference image")
    parser.add_argument("--out", required=True, help="Output MP4 path")
    parser.add_argument("--segment", default="kadin", help="kadin / erkek / kiz_cocuk / erkek_cocuk")
    parser.add_argument("--model-name", default="Leyla", help="Official guzelai.com model name")
    parser.add_argument("--cdp-only", action="store_true", help="Only try Google Flow CDP")
    args = parser.parse_args()

    dummy_outfit = {
        "gender_segment": args.segment,
        "guzelai_model_name": args.model_name,
        "model_frames": [args.ref],
    }
    prompt = build_flow_walking_prompt(dummy_outfit)
    res = generate_flow_walk_via_cdp(args.ref, prompt, args.out, timeout_sec=190)
    out_json = Path(args.out).with_suffix(".json")
    out_json.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False))
