"""CLI entry point for Milthm Auto Garden automation workflows.

This is the main command-line interface for controlling various automation workflows.

Dependencies (install inside your venv):
    uv pip install opencv-python numpy psutil pywin32 mss pyyaml

Usage:
    python main.py                    # Show help and available commands
    python main.py auto [crop]        # Run full auto garden workflow
    python main.py plant <crop>       # Plant a specific crop
    python main.py harvest            # Run harvest workflow once
    python main.py monitor [interval] # Start harvest monitoring loop
    python main.py test <template>    # Test click on a template image
    python main.py list               # List all available functions
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# Import workflow engine
from workflow import WorkflowEngine
from functions import get_all_functions
from core import locate_and_click


def show_help():
    """Display help information and available commands."""
    print("\n" + "=" * 70)
    print("🌱 Milthm Auto Garden - CLI Control Panel")
    print("=" * 70)
    print("\nAvailable Commands:")
    print("\n  python main.py auto [crop_name]")
    print("    Run the complete auto garden workflow:")
    print("    - Navigate to garden (handles all possible starting locations)")
    print("    - Plant crops (will prompt for selection if crop not specified)")
    print("    - Start automatic harvest monitoring")
    print("    Example: python main.py auto shuangbaomuogu")
    print()
    print("  python main.py plant <crop_name>")
    print("    Plant a specific crop without full workflow")
    print("    Example: python main.py plant shuangbaomuogu")
    print()
    print("  python main.py harvest")
    print("    Run harvest workflow once (manual trigger)")
    print()
    print("  python main.py monitor [interval]")
    print("    Start harvest monitoring event loop")
    print("    Optional interval in seconds (default: 10)")
    print("    Example: python main.py monitor 15")
    print()
    print("  python main.py test <template_path>")
    print("    Test clicking a specific template image")
    print("    Example: python main.py test assets/button/shouhuo.png")
    print()
    print("  python main.py list")
    print("    List all available click functions")
    print()
    print("  python main.py help")
    print("    Show this help message")
    print("\n" + "=" * 70)


def list_functions():
    """List all available click functions."""
    print("\n" + "=" * 70)
    print("Available Click Functions")
    print("=" * 70)

    functions = get_all_functions()

    print("\n📌 Buttons:")
    for name in sorted([n for n in functions.keys() if n.startswith("button_")]):
        print(f"  • {name}()")

    print("\n🔍 Icons:")
    for name in sorted([n for n in functions.keys() if n.startswith("icon_")]):
        print(f"  • {name}()")

    print("\n📦 Items:")
    for name in sorted([n for n in functions.keys() if n.startswith("item_")]):
        print(f"  • {name}()")

    print("\n✓ Check Functions:")
    for name in sorted([n for n in functions.keys() if n.startswith("check_")]):
        print(f"  • {name}()")

    print("\n" + "=" * 70)


def run_auto_workflow(crop_name: Optional[str] = None) -> int:
    """Run the complete auto garden workflow.

    Args:
        crop_name: Optional crop name to plant
    """
    if crop_name:
        print(f"\n🚀 Starting complete auto garden workflow with crop: {crop_name}")
    else:
        print("\n🚀 Starting complete auto garden workflow...")

    from auto_garden import main as auto_main

    return auto_main(crop_name)


def run_plant_workflow(crop_name: str) -> int:
    """Run planting workflow for a specific crop using YAML workflow."""
    print(f"\n🌱 Planting crop: {crop_name}")

    # Initialize engine and register functions
    engine = WorkflowEngine()
    engine.register_functions(get_all_functions())

    try:
        # Execute navigate + plant workflow
        engine.execute_workflow("navigate_to_garden")
        engine.execute_workflow("plant_crop", params={"crop_name": crop_name})
        print(f"\n✓ Successfully planted {crop_name}")
        return 0
    except Exception as e:
        print(f"\n✗ Failed to plant {crop_name}: {e}")
        return 1


def run_harvest_workflow() -> int:
    """Run harvest workflow once using YAML workflow."""
    print("\n🌾 Running harvest workflow...")

    # Initialize engine and register functions
    engine = WorkflowEngine()
    engine.register_functions(get_all_functions())

    try:
        engine.execute_workflow("harvest")
        print("\n✓ Harvest completed successfully")
        return 0
    except Exception as e:
        print(f"\n✗ Harvest failed: {e}")
        return 1


def run_monitor_loop(interval: float = 10.0) -> int:
    """Start harvest monitoring event loop using YAML workflow."""
    print(f"\n👁 Starting harvest monitor (interval: {interval}s)")
    print("Press Ctrl+C to stop\n")

    # Initialize engine and register functions
    engine = WorkflowEngine()
    engine.register_functions(get_all_functions())

    try:
        # Note: monitor_harvest workflow has event_loop built-in
        engine.execute_workflow("monitor_harvest")
        return 0
    except KeyboardInterrupt:
        print("\n\n✓ Monitor stopped by user")
        return 0
    except Exception as e:
        print(f"\n✗ Monitor failed: {e}")
        return 1


def test_template(template_path: str) -> int:
    """Test clicking a template image."""
    path = Path(template_path)

    if not path.exists():
        print(f"\n✗ Template not found: {template_path}")
        return 1

    print(f"\n🧪 Testing template: {template_path}")

    if locate_and_click(str(path)):
        print("\n✓ Template click successful")
        return 0
    else:
        print("\n✗ Template click failed")
        return 1


def main() -> int:
    """Main CLI entry point."""

    # No arguments - show help
    if len(sys.argv) == 1:
        show_help()
        return 0

    command = sys.argv[1].lower()

    # Route commands
    if command in ["help", "-h", "--help"]:
        show_help()
        return 0

    elif command == "auto":
        crop_name = None
        if len(sys.argv) >= 3:
            crop_name = sys.argv[2]
        return run_auto_workflow(crop_name)

    elif command == "plant":
        if len(sys.argv) < 3:
            print("\n✗ Error: Crop name required")
            print("Usage: python main.py plant <crop_name>")
            return 1
        crop_name = sys.argv[2]
        return run_plant_workflow(crop_name)

    elif command == "harvest":
        return run_harvest_workflow()

    elif command == "monitor":
        interval = 10.0
        if len(sys.argv) >= 3:
            try:
                interval = float(sys.argv[2])
            except ValueError:
                print(f"\n⚠ Invalid interval: {sys.argv[2]}, using default 10s")
        return run_monitor_loop(interval)

    elif command == "test":
        if len(sys.argv) < 3:
            print("\n✗ Error: Template path required")
            print("Usage: python main.py test <template_path>")
            return 1
        template_path = sys.argv[2]
        return test_template(template_path)

    elif command == "list":
        list_functions()
        return 0

    else:
        print(f"\n✗ Unknown command: {command}")
        print("Run 'python main.py help' for available commands")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n✓ Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
