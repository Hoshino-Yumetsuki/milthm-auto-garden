"""Core image recognition and window interaction functionality.

This module provides the low-level functions for template matching,
window capture, and mouse click simulation.
"""

from __future__ import annotations

import time
import ctypes
from typing import Optional, Tuple

import cv2
import numpy as np
import psutil
import mss
import win32con
import win32gui
import win32process
import win32api


# Configuration constants
PROCESS_NAME = "milthm.exe"
MATCH_THRESHOLD = 0.9  # Increase if false positives appear.
DEBUG_SAVE_SCREENSHOTS = False  # Set to True to save screenshots for debugging
# Scales to try for template matching (supports arbitrary template sizes).
SCALES = [
    1.0,
    0.95,
    0.9,
    0.85,
    0.8,
    0.75,
    0.7,
    0.65,
    0.6,
    0.55,
    0.5,
    1.05,
    1.1,
]


def set_dpi_awareness() -> None:
    """Make the process DPI aware so capture and click coordinates align."""
    user32 = ctypes.windll.user32
    try:
        # Per-monitor v2 on Windows 10+.
        user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except Exception:
        try:
            user32.SetProcessDPIAware()
        except Exception:
            pass


def find_window_for_process(process_name: str) -> Optional[int]:
    """Return the top-level window handle for the given process name."""

    def _callback(hwnd, results):
        if not win32gui.IsWindowVisible(hwnd):
            return
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            return
        if proc.name().lower() == process_name.lower():
            results.append(hwnd)

    matches: list[int] = []
    win32gui.EnumWindows(_callback, matches)
    return matches[0] if matches else None


def bring_to_foreground(hwnd: int) -> bool:
    """Bring the window to the foreground.

    Returns:
        True if successful, False otherwise.
    """
    try:
        # First, restore the window if minimized
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.1)

        # Try to set foreground
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.05)

        # Verify it worked
        return win32gui.GetForegroundWindow() == hwnd
    except Exception as exc:
        # Silently handle common SetForegroundWindow failures
        # This often happens but doesn't prevent image detection
        return False


def capture_window(hwnd: int) -> Tuple[np.ndarray, Tuple[int, int]]:
    """Capture the client area of the window as a BGR numpy array.

    Returns (image, (offset_x, offset_y)) where offset is the screen-space
    coordinate of the top-left corner of the captured client area.
    """

    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    if right - left == 0 or bottom - top == 0:
        raise RuntimeError("Window client area is empty")

    # Convert client coords to screen coords.
    offset = win32gui.ClientToScreen(hwnd, (left, top))
    width, height = right - left, bottom - top

    bbox = {"left": offset[0], "top": offset[1], "width": width, "height": height}
    with mss.mss() as sct:
        shot = sct.grab(bbox)
    img = np.array(shot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    return img, (offset[0], offset[1])


def find_template_on_screen(
    screen: np.ndarray,
    template: np.ndarray,
    threshold: float,
    scales: Tuple[float, ...],
) -> Optional[Tuple[int, int, int, int, float, float]]:
    """Return (x, y, w, h, score, scale) of the best match if above threshold."""

    best = None
    for scale in scales:
        scaled = cv2.resize(
            template,
            dsize=None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA if scale < 1.0 else cv2.INTER_CUBIC,
        )
        h, w = scaled.shape[:2]
        if h > screen.shape[0] or w > screen.shape[1]:
            continue
        result = cv2.matchTemplate(screen, scaled, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if best is None or max_val > best[0]:
            best = (max_val, max_loc, w, h, scale)

    if best is None or best[0] < threshold:
        return None

    max_val, max_loc, w, h, scale = best
    return max_loc[0], max_loc[1], w, h, max_val, scale


def click_screen(x: int, y: int) -> None:
    """Simulate a left mouse click at screen coordinates."""

    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def locate_and_click(
    template_path: str,
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate the template in the process window and click it.

    Args:
        template_path: Path to the template image file
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """

    hwnd = find_window_for_process(process_name)
    if hwnd is None:
        print(f"[error] No window found for process '{process_name}'.")
        return False

    # Try to bring to foreground (may fail, but continue anyway)
    bring_to_foreground(hwnd)
    time.sleep(0.2)  # Allow focus to settle.

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"[error] Could not read template image: {template_path}")
        return False

    screen, offset = capture_window(hwnd)

    # Debug: Save screenshot if enabled
    if DEBUG_SAVE_SCREENSHOTS:
        from pathlib import Path

        debug_dir = Path("debug_screenshots")
        debug_dir.mkdir(exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        template_name = Path(template_path).stem
        screenshot_path = debug_dir / f"{timestamp}_{template_name}_screen.png"
        cv2.imwrite(str(screenshot_path), screen)
        print(f"[debug] Saved screenshot to {screenshot_path}")

    match = find_template_on_screen(screen, template, threshold, tuple(SCALES))
    if match is None:
        # print(f"[error] Template not found (threshold={threshold}).")  # Commented out for cleaner output
        return False

    x, y, w, h, score, scale = match
    client_center = (x + w // 2, y + h // 2)
    screen_center = win32gui.ClientToScreen(hwnd, client_center)
    click_screen(screen_center[0], screen_center[1])
    print(
        f"[info] Clicked at client={client_center} screen={screen_center} score={score:.3f} scale={scale:.2f}."
    )
    return True


def check_exists(
    template_path: str,
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if the template exists in the process window without clicking.

    Args:
        template_path: Path to the template image file
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if found, False otherwise.
    """

    hwnd = find_window_for_process(process_name)
    if hwnd is None:
        return False

    # Try to bring to foreground (may fail, but continue anyway)
    bring_to_foreground(hwnd)
    time.sleep(0.1)  # Brief pause for focus.

    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        return False

    screen, offset = capture_window(hwnd)
    match = find_template_on_screen(screen, template, threshold, tuple(SCALES))

    if match is not None:
        x, y, w, h, score, scale = match
        print(f"[info] Template found: score={score:.3f} scale={scale:.2f}")
        return True

    return False


def locate_and_click_multi(
    template_paths: list[str],
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate one of multiple template variants and click it.

    Tries each template in order and clicks the first one found.

    Args:
        template_paths: List of paths to template image files (variants)
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """

    hwnd = find_window_for_process(process_name)
    if hwnd is None:
        print(f"[error] No window found for process '{process_name}'.")
        return False

    bring_to_foreground(hwnd)
    time.sleep(0.2)  # Allow focus to settle.

    screen, offset = capture_window(hwnd)

    # Try each template variant
    best_match = None
    best_template_path = None

    for template_path in template_paths:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"[warn] Could not read template image: {template_path}")
            continue

        match = find_template_on_screen(screen, template, threshold, tuple(SCALES))
        if match is not None:
            # Found a match
            if best_match is None or match[4] > best_match[4]:  # Compare scores
                best_match = match
                best_template_path = template_path

    if best_match is None:
        print(f"[error] None of the template variants found (threshold={threshold}).")
        return False

    x, y, w, h, score, scale = best_match
    client_center = (x + w // 2, y + h // 2)
    screen_center = win32gui.ClientToScreen(hwnd, client_center)
    click_screen(screen_center[0], screen_center[1])
    print(
        f"[info] Clicked variant '{best_template_path}' at client={client_center} screen={screen_center} score={score:.3f} scale={scale:.2f}."
    )
    return True


def check_exists_multi(
    template_paths: list[str],
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if one of multiple template variants exists without clicking.

    Args:
        template_paths: List of paths to template image files (variants)
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if any variant found, False otherwise.
    """

    hwnd = find_window_for_process(process_name)
    if hwnd is None:
        return False

    bring_to_foreground(hwnd)
    time.sleep(0.1)  # Brief pause for focus.

    screen, offset = capture_window(hwnd)

    # Try each template variant
    for template_path in template_paths:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            continue

        match = find_template_on_screen(screen, template, threshold, tuple(SCALES))
        if match is not None:
            x, y, w, h, score, scale = match
            print(
                f"[info] Template variant found: '{template_path}' score={score:.3f} scale={scale:.2f}"
            )
            return True

    return False


# Initialize DPI awareness when module is imported
set_dpi_awareness()
