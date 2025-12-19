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


# ============================================================================
# Item Functions
# ============================================================================


def item_konghuapen(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """Locate and click the 'konghuapen' item.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "item" / "konghuapen.png")
    return locate_and_click(template_path, process_name, threshold)


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
        crop_name: Name of the crop (e.g., 'shuangbaomuogu')
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True on success, False otherwise.
    """
    template_path = str(ASSETS_DIR / "plant" / f"{crop_name}.png")
    return locate_and_click(template_path, process_name, threshold)


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
    """Check if 'konghuapen' exists without clicking.

    Args:
        process_name: Name of the process to find (default: PROCESS_NAME)
        threshold: Match threshold (default: MATCH_THRESHOLD)

    Returns:
        True if found, False otherwise.
    """
    template_path = str(ASSETS_DIR / "item" / "konghuapen.png")
    return check_exists(template_path, process_name, threshold)


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
        # Items
        "item_konghuapen": item_konghuapen,
        "item_is_in_select_music": item_is_in_select_music,
        # Plants
        "plant_crop": plant_crop,
        "item_crop": item_crop,  # Backward compatibility
        # Check functions
        "check_luxiaohuiting": check_luxiaohuiting,
        "check_konghuapen": check_konghuapen,
        "check_icon_shouhuo": check_icon_shouhuo,
        "check_is_in_garden": check_is_in_garden,
        "check_garden_zhongzhi": check_garden_zhongzhi,
    }
