"""Auto-generated click functions for each template image.

Each function corresponds to a specific template image and provides
a convenient way to locate and click that template in the target window.

Usage:
    from functions import button_shouhuo, icon_shouhuo

    # Click the shouhuo button
    button_shouhuo()

    # Click with custom threshold
    icon_shouhuo(threshold=0.7)
"""

from pathlib import Path
from core import (
    locate_and_click,
    check_exists,
    locate_and_click_multi,
    check_exists_multi,
    get_template_location,
    PROCESS_NAME,
    MATCH_THRESHOLD,
)


# Get the assets directory path
ASSETS_DIR = Path(__file__).parent / "assets"


# ============================================================================
# Button Functions
# ============================================================================


def button_luxiaohuiting(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'luxiaohuiting' button (supports two variants).

    This function supports two variants of the button:
    - luxiaohuiting.png (normal state)
    - luxiaohuiting_gantanhao.png (with exclamation mark)

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_paths = [
        str(ASSETS_DIR / "button" / "luxiaohuiting.png"),
        str(ASSETS_DIR / "button" / "luxiaohuiting_gantanhao.png"),
    ]
    return locate_and_click_multi(template_paths, process_name, threshold)


def button_shouhuo(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'shouhuo' button.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "button" / "shouhuo.png")
    return locate_and_click(template_path, process_name, threshold)


def button_zhongzhi(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'zhongzhi' button.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "button" / "zhongzhi.png")
    return locate_and_click(template_path, process_name, threshold)


def button_return(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'return' button.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "button" / "return.png")
    return locate_and_click(template_path, process_name, threshold)


# ============================================================================
# Icon Functions
# ============================================================================


def icon_shouhuo(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'shouhuo' icon.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "shouhuo.png")
    return locate_and_click(template_path, process_name, threshold)


def icon_garden_zhongzhi(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'garden_zhongzhi' icon.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "garden_zhongzhi.png")
    return locate_and_click(template_path, process_name, threshold)


def icon_garden_return(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'garden_return' icon.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "garden_return.png")
    return locate_and_click(template_path, process_name, threshold)


def icon_huode(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'huode' (obtained/reward) icon to close the reward screen.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "huode.png")
    return locate_and_click(template_path, process_name, threshold)


# ============================================================================
# Item Functions
# ============================================================================


def item_konghuapen(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'konghuapen' item.

    This function finds all empty pots, excludes those with seedlings nearby,
    and clicks the first truly empty pot. Uses a single screenshot for consistency.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    from core import (
        find_window_for_process,
        bring_to_foreground,
        capture_window,
        click_screen,
    )
    import cv2
    import numpy as np
    import time

    # Capture window once for all detections
    hwnd = find_window_for_process(process_name)
    if hwnd is None:
        print("[debug] item_konghuapen: Window not found")
        return False

    bring_to_foreground(hwnd)
    time.sleep(0.2)

    screen, offset = capture_window(hwnd)

    # Helper function to find all matches in the captured screen
    def find_all_in_screen(template_path, thresh):
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            return []

        from core import SCALES

        locations = []

        for scale in SCALES:
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
            loc = np.where(result >= thresh)

            for pt in zip(*loc[::-1]):
                x, y = pt
                is_new = True
                for ex_x, ex_y, ex_w, ex_h in locations:
                    dist = ((x - ex_x) ** 2 + (y - ex_y) ** 2) ** 0.5
                    if dist < 30:
                        is_new = False
                        break
                if is_new:
                    locations.append((x, y, w, h))

        return locations

    # Find all empty pot locations
    template_path = str(ASSETS_DIR / "item" / "konghuapen.png")
    pot_locations = find_all_in_screen(template_path, threshold)

    if not pot_locations:
        print("[debug] item_konghuapen: No pots detected")
        return False

    print(f"[debug] item_konghuapen: Found {len(pot_locations)} pot(s) to check")

    # Find all seedling pot locations using the SAME screenshot
    seedling_locations = []
    seedling_dir = ASSETS_DIR / "is_not_empty_huapen"
    if seedling_dir.exists():
        template_count = 0
        for seedling_template in seedling_dir.glob("*.png"):
            template_count += 1
            print(
                f"[debug] item_konghuapen: Checking template: {seedling_template.name}"
            )
            locs = find_all_in_screen(str(seedling_template), 0.75)
            if locs:
                print(
                    f"[debug] item_konghuapen: Found {len(locs)} seedling(s) with {seedling_template.name}"
                )
            else:
                print(
                    f"[debug] item_konghuapen: No matches for {seedling_template.name}"
                )
            seedling_locations.extend(locs)
        print(f"[debug] item_konghuapen: Checked {template_count} template(s)")

    print(
        f"[debug] item_konghuapen: Total seedlings to avoid: {len(seedling_locations)}"
    )

    # Find first pot that is far from all seedlings and click it
    for pot_x, pot_y, pot_w, pot_h in pot_locations:
        pot_center_x = pot_x + pot_w // 2
        pot_center_y = pot_y + pot_h // 2

        is_empty = True
        for s_x, s_y, s_w, s_h in seedling_locations:
            s_center_x = s_x + s_w // 2
            s_center_y = s_y + s_h // 2
            distance = (
                (pot_center_x - s_center_x) ** 2 + (pot_center_y - s_center_y) ** 2
            ) ** 0.5

            if distance < 80:
                print(
                    f"[info] Pot at ({pot_center_x}, {pot_center_y}) has seedling, skipping (distance: {distance:.1f}px)"
                )
                is_empty = False
                break

        if is_empty:
            # Convert window coordinates to screen coordinates
            screen_x = pot_center_x + offset[0]
            screen_y = pot_center_y + offset[1]
            print(
                f"[info] Clicking empty pot at window({pot_center_x}, {pot_center_y}) -> screen({screen_x}, {screen_y})"
            )
            click_screen(screen_x, screen_y)
            return True

    return False


def item_is_in_select_music(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if currently in music selection screen.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if found, False otherwise.
    """
    template_path = str(ASSETS_DIR / "item" / "is_in_select_music.png")
    return check_exists(template_path, process_name, threshold)


def plant_crop(
    crop_name: str,
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Click on a specific plant/crop by name.

    Args:
        crop_name: Name of the crop (e.g., 'shuangbaomuogu', 'wuwangcao')
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "plant" / f"{crop_name}.png")
    return locate_and_click(template_path, process_name, threshold)


def plant_wuwangcao(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Convenience function to plant wuwangcao (forget-me-not).

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    return plant_crop("wuwangcao", process_name, threshold)


def plant_shuangbaomogu(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Convenience function to plant shuangbaomogu (double spore mushroom).

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    return plant_crop("shuangbaomogu", process_name, threshold)


# Keep backward compatibility alias
item_crop = plant_crop


# ============================================================================
# Check Functions (detection without clicking)
# ============================================================================


def check_luxiaohuiting(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if 'luxiaohuiting' button exists without clicking (supports two variants).

    This function supports two variants of the button:
    - luxiaohuiting.png (normal state)
    - luxiaohuiting_gantanhao.png (with exclamation mark)

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if found, False otherwise.
    """
    template_paths = [
        str(ASSETS_DIR / "button" / "luxiaohuiting.png"),
        str(ASSETS_DIR / "button" / "luxiaohuiting_gantanhao.png"),
    ]
    return check_exists_multi(template_paths, process_name, threshold)


def check_konghuapen(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if 'konghuapen' item exists without clicking.

    This function finds all empty pots and excludes those that have seedlings nearby.
    Uses a single screenshot for consistency.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if empty pot found (without seedling nearby), False otherwise.
    """
    from core import find_window_for_process, bring_to_foreground, capture_window
    import cv2
    import numpy as np
    import time

    # Capture window once for all detections
    hwnd = find_window_for_process(process_name)
    if hwnd is None:
        print("[debug] Window not found")
        return False

    bring_to_foreground(hwnd)
    time.sleep(0.2)  # Longer wait to ensure window is ready

    screen, offset = capture_window(hwnd)

    # Helper function to find all matches in the captured screen
    def find_all_in_screen(template_path, thresh):
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            return []

        from core import SCALES

        locations = []

        for scale in SCALES:
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
            loc = np.where(result >= thresh)

            for pt in zip(*loc[::-1]):
                x, y = pt
                # Avoid duplicates
                is_new = True
                for ex_x, ex_y, ex_w, ex_h in locations:
                    dist = ((x - ex_x) ** 2 + (y - ex_y) ** 2) ** 0.5
                    if dist < 30:
                        is_new = False
                        break
                if is_new:
                    locations.append((x, y, w, h))

        return locations

    # Find all empty pot locations
    template_path = str(ASSETS_DIR / "item" / "konghuapen.png")
    pot_locations = find_all_in_screen(template_path, threshold)

    if not pot_locations:
        print("[debug] No pots detected")
        return False

    print(f"[debug] Found {len(pot_locations)} pot(s)")

    # Find all seedling pot locations using the SAME screenshot
    seedling_locations = []
    seedling_dir = ASSETS_DIR / "is_not_empty_huapen"
    if seedling_dir.exists():
        template_count = 0
        for seedling_template in seedling_dir.glob("*.png"):
            template_count += 1
            print(f"[debug] Checking seedling template: {seedling_template.name}")
            locs = find_all_in_screen(str(seedling_template), 0.75)
            if locs:
                print(
                    f"[debug] Found {len(locs)} seedling(s) with template {seedling_template.name}"
                )
            else:
                print(f"[debug] No matches for template {seedling_template.name}")
            seedling_locations.extend(locs)
        print(f"[debug] Checked {template_count} seedling template(s)")

    print(f"[debug] Total seedlings detected: {len(seedling_locations)}")

    # Check if any pot is far from all seedlings
    for pot_x, pot_y, pot_w, pot_h in pot_locations:
        pot_center_x = pot_x + pot_w // 2
        pot_center_y = pot_y + pot_h // 2

        is_empty = True
        for s_x, s_y, s_w, s_h in seedling_locations:
            s_center_x = s_x + s_w // 2
            s_center_y = s_y + s_h // 2
            distance = (
                (pot_center_x - s_center_x) ** 2 + (pot_center_y - s_center_y) ** 2
            ) ** 0.5

            if distance < 80:
                print(
                    f"[info] Pot at ({pot_center_x}, {pot_center_y}) has seedling nearby (distance: {distance:.1f}px)"
                )
                is_empty = False
                break

        if is_empty:
            print(f"[info] Found empty pot at ({pot_center_x}, {pot_center_y})")
            return True

    return False


def check_icon_shouhuo(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if 'shouhuo' icon exists without clicking.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if found, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "shouhuo.png")
    return check_exists(template_path, process_name, threshold)


def check_is_in_garden(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if currently in garden interface.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if in garden, False otherwise.
    """
    template_path = str(ASSETS_DIR / "item" / "is_in_garden.png")
    return check_exists(template_path, process_name, threshold)


def check_garden_zhongzhi(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if currently in plant selection interface.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if in plant selection, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "garden_zhongzhi.png")
    return check_exists(template_path, process_name, threshold)


def check_plant_wuwangcao(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if wuwangcao (forget-me-not) plant is visible/planted.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if wuwangcao is visible, False otherwise.
    """
    template_path = str(ASSETS_DIR / "plant" / "wuwangcao.png")
    return check_exists(template_path, process_name, threshold)


def check_plant_shuangbaomogu(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if shuangbaomogu (double spore mushroom) plant is visible/planted.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if shuangbaomogu is visible, False otherwise.
    """
    template_path = str(ASSETS_DIR / "plant" / "shuangbaomogu.png")
    return check_exists(template_path, process_name, threshold)


def check_icon_huode(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Check if 'huode' (obtained/reward) screen is visible.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if reward screen is visible, False otherwise.
    """
    template_path = str(ASSETS_DIR / "icon" / "huode.png")
    return check_exists(template_path, process_name, threshold)


# ============================================================================
# Utility: Get all available functions
# ============================================================================


def get_all_functions():
    """Return a dictionary of all available click functions."""
    return {
        # Buttons
        "button_luxiaohuiting": button_luxiaohuiting,
        "button_shouhuo": button_shouhuo,
        "button_zhongzhi": button_zhongzhi,
        "button_return": button_return,
        # Icons
        "icon_shouhuo": icon_shouhuo,
        "icon_garden_zhongzhi": icon_garden_zhongzhi,
        "icon_garden_return": icon_garden_return,
        "icon_huode": icon_huode,
        # Items
        "item_konghuapen": item_konghuapen,
        "item_is_in_select_music": item_is_in_select_music,
        # Plants
        "plant_crop": plant_crop,
        "plant_wuwangcao": plant_wuwangcao,
        "plant_shuangbaomogu": plant_shuangbaomogu,
        "item_crop": item_crop,  # Backward compatibility
        # Check functions
        "check_luxiaohuiting": check_luxiaohuiting,
        "check_konghuapen": check_konghuapen,
        "check_icon_shouhuo": check_icon_shouhuo,
        "check_is_in_garden": check_is_in_garden,
        "check_garden_zhongzhi": check_garden_zhongzhi,
        "check_plant_wuwangcao": check_plant_wuwangcao,
        "check_plant_shuangbaomogu": check_plant_shuangbaomogu,
        "check_icon_huode": check_icon_huode,
    }
