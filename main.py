"""Credit Scoring Tool - entry point.

Run from the project root with:  python main.py
"""

from ingestion.menu import run_main_menu


def main() -> None:
    """Start the text-based main menu."""
    try:
        run_main_menu()
    except NotImplementedError:
        print("The main menu is not implemented yet (US-M1-09).")


if __name__ == "__main__":
    main()
