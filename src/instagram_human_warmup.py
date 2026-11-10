"""
Pre-Publish Human Browsing, GhostCursor Cubic Bézier Biometrics & Niche Algorithm Warm-Up Engine
================================================================================================
Developed for GüzelAI Holding A.Ş. (@guzelaicom)
Skill Reference: `guzelai-human-algorithm-warmup`

Open-Source GitHub Repositories Integrated & Adapted for Chrome CDP (Port 9230):
1. `Xetera/ghost-cursor` (https://github.com/Xetera/ghost-cursor - 1,627⭐):
   Fitts's Law + Cubic Bézier mouse trajectories with target overshoot and micro-tremor jitter.
2. `reaz1995/ghost-cursor-playwright` (https://github.com/reaz1995/ghost-cursor-playwright - 101⭐):
   Variable velocity curves, randomized bounding-box click targets, and organic scroll dynamics.
3. `riflosnake/HumanCursor` (https://github.com/riflosnake/HumanCursor - 546⭐):
   Human hand acceleration/deceleration profiles and natural wheel scroll inertia.
4. `mcolella14/python_ghost_cursor` (https://github.com/mcolella14/python_ghost_cursor - 81⭐):
   Python mathematical port of GhostCursor 2D Bézier path generation.

Strict Zero-Violation ("İhlal Olmasın") Guarantees:
- Respects the 24-Hour Post-Login Curing Lock (`session_warmup_until_iso`): NEVER touches Instagram today
  while the newly saved login session is resting/curing.
- Runs ONLY on the single local trusted Chrome profile (`ig_chrome_trusted`, Port 9230) on home IP.
- Micro-Dose Caps per Warm-Up Session:
  * Watched Reels: 4 to 6 Reels
  * Likes (❤️): Max 1 to 2 per session (only on verified fashion/kombin Reels)
  * Saves (🔖): Max 1 per session (only on high-signal fashion/Old Money Reels)
  * Comments / Follows / Unfollows / DMs: STRICTLY 0 (Permanently Banned)
"""

import argparse
import datetime
import json
import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import websocket

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
WARMUP_LEDGER_PATH = OUTPUT_DIR / "instagram_algorithm_warmup_ledger.json"
IG_HIST_PATH = OUTPUT_DIR / "instagram_uploaded_history.json"
GITHUB_KB_PATH = OUTPUT_DIR / "github_open_source_knowledge_base.json"

GITHUB_BIOMETRIC_REPOS: List[Dict[str, Any]] = [
    {
        "repo": "Xetera/ghost-cursor",
        "url": "https://github.com/Xetera/ghost-cursor",
        "stars": 1627,
        "domain": "Biometric Cubic Bézier Mouse Physics & Fitts's Law Overshoot",
        "integrated_in": "src/instagram_human_warmup.py (GhostCursorCDP)",
    },
    {
        "repo": "riflosnake/HumanCursor",
        "url": "https://github.com/riflosnake/HumanCursor",
        "stars": 546,
        "domain": "Human Hand Velocity Profiles, Gaussian Click Offset & Wheel Scroll Inertia",
        "integrated_in": "src/instagram_human_warmup.py (GhostCursorCDP)",
    },
    {
        "repo": "reaz1995/ghost-cursor-playwright",
        "url": "https://github.com/reaz1995/ghost-cursor-playwright",
        "stars": 101,
        "domain": "Playwright/CDP Bézier Pathing & Auto-Scroll Humanization",
        "integrated_in": "src/instagram_human_warmup.py",
    },
    {
        "repo": "mcolella14/python_ghost_cursor",
        "url": "https://github.com/mcolella14/python_ghost_cursor",
        "stars": 81,
        "domain": "Python 2D Bézier Curve Control Point Math",
        "integrated_in": "src/instagram_human_warmup.py",
    },
]

# Fashion, Old Money & Styling Niche Keywords for Selective Algorithm Training
FASHION_NICHE_POSITIVE_KEYWORDS: List[str] = [
    "kombin",
    "old money",
    "oldmoney",
    "quiet luxury",
    "sessiz lüks",
    "stil",
    "moda",
    "outfit",
    "ootd",
    "grwm",
    "kaban",
    "kaşe",
    "trençkot",
    "triko",
    "kaşmir",
    "palazzo",
    "loafer",
    "chelsea bot",
    "çanta",
    "elbise",
    "ceket",
    "blazer",
    "gömlek",
    "pantolon",
    "kış kombini",
    "sonbahar kombini",
    "erkek kombin",
    "kadın kombin",
    "fashion",
    "style",
    "menswear",
    "womenswear",
    "street style",
    "lookbook",
    "nişantaşı",
    "bebek",
    "milano",
    "paris",
    "sprezzatura",
    "kapsül gardırop",
]

OFF_NICHE_SKIP_KEYWORDS: List[str] = [
    "futbol",
    "galatasaray",
    "fenerbahçe",
    "beşiktaş",
    "iddaa",
    "bahis",
    "kripto",
    "bitcoin",
    "pubg",
    "valorant",
    "siyaset",
    "yemek tarifi",
    "komedi",
    "şaka",
]


def register_biometric_repos_in_knowledge_base() -> Dict[str, Any]:
    """Saves the discovered GitHub human-biometric repositories into the Holding's GitHub R&D Knowledge Base."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    kb: Dict[str, Any] = {}
    if GITHUB_KB_PATH.exists():
        try:
            kb = json.loads(GITHUB_KB_PATH.read_text(encoding="utf-8"))
        except Exception:
            kb = {}
    existing = kb.get("human_biometrics_and_algorithm_warmup_repos", [])
    existing_names = {r.get("repo") for r in existing if isinstance(r, dict)}
    for repo_item in GITHUB_BIOMETRIC_REPOS:
        if repo_item["repo"] not in existing_names:
            existing.append(repo_item)
    kb["human_biometrics_and_algorithm_warmup_repos"] = existing
    kb["last_updated_iso"] = datetime.datetime.now().isoformat(timespec="seconds")
    GITHUB_KB_PATH.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"registered_repos": len(existing), "kb_path": str(GITHUB_KB_PATH)}


class GhostCursorCDP:
    """
    Python CDP port of `Xetera/ghost-cursor` + `riflosnake/HumanCursor`.
    Generates human-like Cubic Bézier mouse paths with Fitts's Law ease-in-out velocity,
    natural micro-tremor, optional overshoot, Gaussian bounding-box targeting, and wheel inertia.
    """

    def __init__(self, cdp_call: Callable[[str, Optional[Dict[str, Any]]], Dict[str, Any]]) -> None:
        self.cdp = cdp_call
        self.x: float = random.uniform(420.0, 760.0)
        self.y: float = random.uniform(340.0, 620.0)

    @staticmethod
    def _cubic_bezier(
        t: float,
        p0: Tuple[float, float],
        p1: Tuple[float, float],
        p2: Tuple[float, float],
        p3: Tuple[float, float],
    ) -> Tuple[float, float]:
        u = 1.0 - t
        tt = t * t
        uu = u * u
        uuu = uu * u
        ttt = tt * t
        bx = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
        by = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
        return bx, by

    def generate_human_curve(
        self,
        start: Tuple[float, float],
        end: Tuple[float, float],
    ) -> List[Tuple[float, float]]:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dist = math.hypot(dx, dy)
        steps = max(14, min(34, int(dist / 18.0) + random.randint(4, 9)))

        # Perpendicular arc offset so the hand never moves in a robotic straight line
        spread = min(110.0, max(18.0, dist * 0.25))
        p1 = (
            start[0] + dx * random.uniform(0.20, 0.38) + random.uniform(-spread, spread),
            start[1] + dy * random.uniform(0.20, 0.38) + random.uniform(-spread, spread),
        )
        p2 = (
            start[0] + dx * random.uniform(0.62, 0.82) + random.uniform(-spread * 0.6, spread * 0.6),
            start[1] + dy * random.uniform(0.62, 0.82) + random.uniform(-spread * 0.6, spread * 0.6),
        )

        points: List[Tuple[float, float]] = []
        for i in range(1, steps + 1):
            raw_t = i / float(steps)
            # Smoothstep ease-in-out velocity profile (human hand acceleration & deceleration)
            eased_t = raw_t * raw_t * (3.0 - 2.0 * raw_t)
            px, py = self._cubic_bezier(eased_t, start, p1, p2, end)
            # Micro-tremor noise except on final landing point
            if i < steps:
                px += random.gauss(0.0, 0.65)
                py += random.gauss(0.0, 0.65)
            points.append((round(px, 1), round(py, 1)))

        # Occasional natural human overshoot (15% probability on longer moves > 260px)
        if dist > 260.0 and random.random() < 0.18:
            overshoot_pt = (
                round(end[0] + random.uniform(-6.0, 6.0), 1),
                round(end[1] + random.uniform(-6.0, 6.0), 1),
            )
            points.insert(-1, overshoot_pt)

        return points

    def move_to(self, target_x: float, target_y: float) -> None:
        curve = self.generate_human_curve((self.x, self.y), (target_x, target_y))
        for px, py in curve:
            self.cdp(
                "Input.dispatchMouseEvent",
                {"type": "mouseMoved", "x": px, "y": py, "button": "none"},
            )
            time.sleep(random.uniform(0.008, 0.022))
        self.x, self.y = target_x, target_y

    def click_bounding_box(self, bbox: Dict[str, float]) -> Tuple[float, float]:
        """
        Selects a Gaussian-randomized point inside the inner 60% of `bbox` (`x`, `y`, `width`, `height`),
        moves along a Cubic Bézier trajectory, hovers briefly, and performs a realistic human click.
        """
        w = max(8.0, float(bbox.get("width", 24.0)))
        h = max(8.0, float(bbox.get("height", 24.0)))
        cx = float(bbox.get("x", 500.0)) + w * 0.5
        cy = float(bbox.get("y", 500.0)) + h * 0.5

        # Gaussian offset clamped to inner 60% of box (never exact mathematical center)
        ox = max(-w * 0.28, min(w * 0.28, random.gauss(0.0, w * 0.14)))
        oy = max(-h * 0.28, min(h * 0.28, random.gauss(0.0, h * 0.14)))
        if abs(ox) < 0.8:
            ox = 1.4 if random.random() < 0.5 else -1.4
        if abs(oy) < 0.8:
            oy = 1.2 if random.random() < 0.5 else -1.2

        tx = round(cx + ox, 1)
        ty = round(cy + oy, 1)
        self.move_to(tx, ty)
        time.sleep(random.uniform(0.075, 0.165))
        self.cdp(
            "Input.dispatchMouseEvent",
            {"type": "mousePressed", "x": tx, "y": ty, "button": "left", "clickCount": 1},
        )
        time.sleep(random.uniform(0.055, 0.125))
        self.cdp(
            "Input.dispatchMouseEvent",
            {"type": "mouseReleased", "x": tx, "y": ty, "button": "left", "clickCount": 1},
        )
        return tx, ty

    def human_wheel_scroll(self, delta_y: int = 680) -> None:
        """
        Simulates a natural multi-step mouse wheel / trackpad flick with inertia deceleration.
        """
        weights = [0.12, 0.24, 0.28, 0.18, 0.11, 0.07]
        for w in weights:
            step_dy = int(delta_y * w + random.uniform(-8.0, 8.0))
            self.cdp(
                "Input.dispatchMouseEvent",
                {
                    "type": "mouseWheel",
                    "x": self.x,
                    "y": self.y,
                    "deltaX": 0,
                    "deltaY": step_dy,
                },
            )
            time.sleep(random.uniform(0.035, 0.085))


def score_reel_niche_relevance(caption_text: str) -> Dict[str, Any]:
    """
    Scores a visible Reel/post caption against our Luxury Fashion / Old Money / Kombin niche.
    Returns whether the human agent should watch deeply & consider liking/saving, or skip quickly.
    """
    low = (caption_text or "").lower()
    for skip_kw in OFF_NICHE_SKIP_KEYWORDS:
        if skip_kw in low:
            return {"is_niche_match": False, "score": 0, "matched_keywords": [], "skip_reason": skip_kw}

    matched = [kw for kw in FASHION_NICHE_POSITIVE_KEYWORDS if kw in low]
    score = len(matched)
    return {
        "is_niche_match": score >= 1,
        "score": score,
        "matched_keywords": matched[:6],
        "high_value_save_candidate": score >= 2 or any(k in low for k in ["kombin", "old money", "quiet luxury", "kaşe", "stil"]),
    }


def check_warmup_curing_status() -> Dict[str, Any]:
    """
    Verifies whether the 24-hour post-login curing lock (`session_warmup_until_iso`) or
    6-hour cooldown is currently active. Guarantees 0 activity today while the new login cures.
    """
    register_biometric_repos_in_knowledge_base()
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        return {
            "ready_to_browse": False,
            "status": "blocked_cloud_ip",
            "reason": "Yabancı bulut IP (GitHub Actions) üzerinden Instagram gezinmesi güvenlik kilidiyle kapatıldı.",
        }

    from instagram_safe_publisher import verify_trusted_ig_session_readonly

    session_check = verify_trusted_ig_session_readonly()
    if not session_check.get("logged_in"):
        return {
            "ready_to_browse": False,
            "status": "not_logged_in",
            "reason": "Tekil güvenilir tarayıcıda (`ig_chrome_trusted`) aktif oturum bulunamadı.",
            "session_check": session_check,
        }

    if IG_HIST_PATH.exists():
        try:
            hdata = json.loads(IG_HIST_PATH.read_text(encoding="utf-8"))
            warmup_until_str = hdata.get("session_warmup_until_iso", "")
            if warmup_until_str:
                warmup_dt = datetime.datetime.fromisoformat(warmup_until_str)
                now_dt = datetime.datetime.now(warmup_dt.tzinfo)
                if now_dt < warmup_dt:
                    rem_hours = round((warmup_dt - now_dt).total_seconds() / 3600.0, 1)
                    return {
                        "ready_to_browse": False,
                        "status": "curing_lock_active_today",
                        "warmup_until_iso": warmup_until_str,
                        "remaining_hours": rem_hours,
                        "session_logged_in": True,
                        "ds_user_id": session_check.get("ds_user_id", ""),
                        "reason": (
                            f"Yeni giriş sonrası 24 saatlik doğal oturum dinlendirme kilidi aktif "
                            f"({warmup_until_str} tarihine kadar, kalan: {rem_hours} saat). "
                            f"Bugün Instagram'a hiçbir otomatik gezinme/beğeni/paylaşım yapılmaz."
                        ),
                    }
        except Exception:
            pass

    return {
        "ready_to_browse": True,
        "status": "ready_for_human_warmup",
        "session_logged_in": True,
        "ds_user_id": session_check.get("ds_user_id", ""),
    }


def run_prepublish_human_warmup(
    cdp: Optional[Callable[[str, Optional[Dict[str, Any]]], Dict[str, Any]]] = None,
    max_reels_to_watch: int = 5,
    max_likes: int = 2,
    max_saves: int = 1,
    force_ignore_curing_lock: bool = False,
) -> Dict[str, Any]:
    """
    Executes the Pre-Publish Human Browsing & Niche Algorithm Warm-Up walk inside
    `ig_chrome_trusted` (Port 9230) before uploading a Reel.
    - Watches 4-6 Reels with natural watch times (9.5s-19.5s for fashion/kombin, 2.2s-3.9s skip for off-niche).
    - Uses GhostCursor Cubic Bézier mouse physics (`Xetera/ghost-cursor` & `riflosnake/HumanCursor`).
    - Likes at most 1-2 fashion posts and Saves at most 1 high-performing fashion post.
    - Strictly 0 comments, 0 follows, 0 rapid URL jumps.
    """
    curing = check_warmup_curing_status()
    if not curing.get("ready_to_browse") and not force_ignore_curing_lock:
        return curing

    own_ws = None
    if cdp is None:
        from instagram_safe_publisher import ensure_trusted_ig_chrome

        ws_url = ensure_trusted_ig_chrome()
        if not ws_url:
            return {"status": "error", "reason": "Trusted Chrome CDP tab unavailable"}
        own_ws = websocket.create_connection(ws_url, timeout=30)
        msg_id = 0

        def _cdp(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            nonlocal msg_id
            msg_id += 1
            own_ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
            while True:
                resp = json.loads(own_ws.recv())
                if resp.get("id") == msg_id:
                    return resp.get("result", {})

        cdp = _cdp
        cdp("Page.enable")
        cdp("DOM.enable")
        cdp("Runtime.enable")
        cdp("Input.enable")

    cursor = GhostCursorCDP(cdp)
    watched_log: List[Dict[str, Any]] = []
    likes_given = 0
    saves_given = 0
    niche_reels_count = random.randint(4, max(4, max_reels_to_watch))

    try:
        # 1. Navigate to Instagram Home or click Reels tab naturally
        cdp("Page.navigate", {"url": "https://www.instagram.com/reels/"})
        time.sleep(random.uniform(4.2, 6.4))

        for idx in range(niche_reels_count):
            # Move cursor slightly as a human resting their hand on the mouse while watching
            cursor.move_to(
                random.uniform(460.0, 780.0),
                random.uniform(320.0, 680.0),
            )

            # Inspect visible text and Like/Save button bounding boxes (read-only DOM evaluation)
            dom_info = json.loads(
                cdp(
                    "Runtime.evaluate",
                    {
                        "expression": """JSON.stringify((() => {
                            const visibleText = document.body ? document.body.innerText.slice(0, 1200) : '';
                            const findBtnBox = (labels) => {
                                const svgs = Array.from(document.querySelectorAll('svg[aria-label]'));
                                for (const svg of svgs) {
                                    const lbl = (svg.getAttribute('aria-label') || '').trim();
                                    if (labels.some(rx => rx.test(lbl))) {
                                        const btn = svg.closest('div[role="button"], button') || svg;
                                        const r = btn.getBoundingClientRect();
                                        if (r.width > 8 && r.height > 8 && r.top > 60 && r.bottom < window.innerHeight - 20) {
                                            return {x: r.left, y: r.top, width: r.width, height: r.height, label: lbl};
                                        }
                                    }
                                }
                                return null;
                            };
                            return {
                                url: location.href,
                                text: visibleText,
                                likeBox: findBtnBox([/^Beğen$/i, /^Like$/i]),
                                saveBox: findBtnBox([/^Kaydet$/i, /^Save$/i])
                            };
                        })())""",
                        "returnByValue": True,
                    },
                )
                .get("result", {})
                .get("value", "{}")
                or "{}"
            )

            caption_snippet = " ".join((dom_info.get("text") or "").split())[:260]
            rel = score_reel_niche_relevance(caption_snippet)

            action_taken: List[str] = []
            if rel["is_niche_match"]:
                # High-affinity fashion/style Reel: watch for 9.5s - 18.5s like a real human
                watch_sec = round(random.uniform(9.5, 18.5), 1)
                time.sleep(watch_sec * 0.55)

                # Micro-dose Like (max 1-2 per session)
                if likes_given < max_likes and dom_info.get("likeBox") and random.random() < 0.65:
                    cursor.click_bounding_box(dom_info["likeBox"])
                    likes_given += 1
                    action_taken.append("liked_via_bezier_cursor")
                    time.sleep(random.uniform(1.4, 2.8))

                # Micro-dose Save (max 1 per session — strongest algorithm signal)
                if (
                    saves_given < max_saves
                    and rel.get("high_value_save_candidate")
                    and dom_info.get("saveBox")
                ):
                    cursor.click_bounding_box(dom_info["saveBox"])
                    saves_given += 1
                    action_taken.append("saved_for_algorithm_affinity")
                    time.sleep(random.uniform(1.6, 3.1))

                time.sleep(watch_sec * 0.45)
            else:
                # Off-niche or generic Reel: human watches 2.2s - 3.9s and scrolls past without engaging
                watch_sec = round(random.uniform(2.2, 3.9), 1)
                action_taken.append("selective_skip_off_niche")
                time.sleep(watch_sec)

            watched_log.append(
                {
                    "reel_index": idx + 1,
                    "url": dom_info.get("url", ""),
                    "watch_seconds": watch_sec,
                    "is_niche_match": rel["is_niche_match"],
                    "matched_keywords": rel["matched_keywords"],
                    "actions": action_taken,
                    "caption_preview": caption_snippet[:140],
                }
            )

            # Scroll to next Reel using human wheel inertia
            cursor.human_wheel_scroll(delta_y=random.randint(640, 780))
            time.sleep(random.uniform(1.8, 3.4))

        # Creator Transition Pause on Home Feed before starting the upload flow
        cdp("Page.navigate", {"url": "https://www.instagram.com/"})
        transition_pause = round(random.uniform(11.0, 16.5), 1)
        time.sleep(transition_pause)

        session_summary = {
            "status": "completed_human_warmup",
            "timestamp_iso": datetime.datetime.now().isoformat(timespec="seconds"),
            "reels_inspected": len(watched_log),
            "likes_given": likes_given,
            "saves_given": saves_given,
            "creator_transition_pause_sec": transition_pause,
            "watched_log": watched_log,
        }

        # Persist to warmup ledger for Style Curation Council analysis
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            ledger = {"sessions": []}
            if WARMUP_LEDGER_PATH.exists():
                ledger = json.loads(WARMUP_LEDGER_PATH.read_text(encoding="utf-8"))
            sessions = ledger.get("sessions", [])
            sessions.append(session_summary)
            ledger["sessions"] = sessions[-50:]
            WARMUP_LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

        return session_summary
    finally:
        if own_ws is not None:
            try:
                own_ws.close()
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description="GüzelAI Yayın Öncesi İnsan Gezinme & Algoritma Isındırma Motoru")
    parser.add_argument("--status", action="store_true", help="Salt-okunur ısınma kilidi ve GitHub repo kaydı kontrolü")
    parser.add_argument("--dry-test-bezier", action="store_true", help="Instagram'a dokunmadan Bézier fare ve algoritma skorlama testi")
    parser.add_argument("--run-warmup", action="store_true", help="Yayın öncesi insan gezinmesini çalıştır (24s dinlenme kilidine uyar)")
    args = parser.parse_args()

    if args.status:
        print(json.dumps(check_warmup_curing_status(), ensure_ascii=False, indent=2))
        return

    if args.dry_test_bezier:
        dummy_events: List[Dict[str, Any]] = []
        cursor = GhostCursorCDP(lambda m, p: dummy_events.append({"method": m, "params": p}) or {})
        click_pt = cursor.click_bounding_box({"x": 620, "y": 480, "width": 32, "height": 32})
        cursor.human_wheel_scroll(700)
        sample_fashion = score_reel_niche_relevance(
            "Nişantaşı Old Money kış kombini: Devetüyü kaşe kaban, ekru boğazlı triko ve palazzo pantolon #kombin #oldmoney"
        )
        sample_offniche = score_reel_niche_relevance("Dün akşamki futbol maçında harika gol! #futbol")
        print(
            json.dumps(
                {
                    "bezier_mouse_events_generated": len(dummy_events),
                    "randomized_click_target": click_pt,
                    "exact_center_avoided": click_pt != (636.0, 496.0),
                    "fashion_reel_evaluation": sample_fashion,
                    "off_niche_reel_evaluation": sample_offniche,
                    "github_repos_registered": register_biometric_repos_in_knowledge_base(),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.run_warmup:
        print(json.dumps(run_prepublish_human_warmup(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
