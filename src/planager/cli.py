from pathlib import Path

from planager import Planager


def interactive(json_root: Path) -> None:
    """
    Run planager in interactive mode as a CLI.
    """
    print("Welcome to interactive planager.")
    planager = Planager.from_json(json_root)
    print(planager)


def derive() -> None:
    print("Deriving...")


def plan() -> None:
    print("Planning...")


def schedule() -> None:
    print("Scheduling...")


def track() -> None:
    print("Welcome to planager tracking.")


def dashboard() -> None:
    print("Welcome to planager dashboard.")


def shift(ndays: int) -> None:
    print(f"Shifting by {ndays}...")
