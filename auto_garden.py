"""Automated garden management workflow for the game.

This script implements the complete automation workflow using YAML-based workflows:
1. Navigate to garden interface
2. Plant crops
3. Monitor and harvest automatically

Usage:
    python auto_garden.py [crop_name]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from workflow import WorkflowEngine
from functions import get_all_functions


def get_crop_choice() -> str:
    """Ask user which crop to plant.

    Returns:
        Crop name (e.g., 'shuangbaomogu')
    """
    print("\n" + "=" * 60)
    print("请选择要种植的作物 (Please select crop to plant)")
    print("=" * 60)

    # List available crops from plant folder
    assets_dir = Path(__file__).parent / "assets" / "plant"
    crop_files = sorted([f.stem for f in assets_dir.glob("*.png")])

    print("\n可用作物列表 (Available crops):")
    for i, crop in enumerate(crop_files, 1):
        print(f"  {i}. {crop}")

    print("\n请输入作物名称 (Enter crop name):")
    crop_name = input("> ").strip()

    return crop_name


def main(crop_name: Optional[str] = None) -> int:
    """Main entry point for the automated garden workflow.

    Args:
        crop_name: Name of the crop to plant (optional, will prompt if not provided)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("\n" + "=" * 60)
    print("🌱 Milthm Auto Garden - YAML-based Workflow Engine")
    print("=" * 60)

    # Initialize workflow engine and register all functions
    engine = WorkflowEngine()
    all_functions = get_all_functions()
    engine.register_functions(all_functions)

    # Get crop choice from user or parameter
    if not crop_name:
        print("\n[Main] Getting crop selection...")
        crop_name = get_crop_choice()

    if not crop_name:
        print("\n[Main] ✗ No crop selected")
        return 1

    print(f"\n[Main] ✓ Selected crop: {crop_name}")

    # Execute auto_garden workflow with crop parameter
    print("\n[Main] Starting auto garden workflow...")
    try:
        engine.execute_workflow("auto_garden", params={"crop_name": crop_name})
        print("\n[Main] ✓ Auto garden workflow completed")
        return 0
    except KeyboardInterrupt:
        print("\n\n[Main] Interrupted by user. Exiting...")
        return 0
    except Exception as e:
        print(f"\n[Main] ✗ Workflow execution failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[Main] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Main] ✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
