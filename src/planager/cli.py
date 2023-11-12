import argparse
from pathlib import Path
from typing import Callable, Protocol

from .planager import Planager


def interactive(json_root: Path) -> None:
    """
    Run planager in interactive mode as a CLI.
    """
    print("Welcome to interactive planager.")
    planager = Planager.from_json(json_root)
    print(planager.summary)


def derive(json_root: Path) -> None:
    planager = Planager.from_json(json_root)
    planager.derive()


def plan(json_root: Path) -> None:
    planager = Planager.from_json(json_root)
    planager.derive_plan()


def schedule(json_root: Path) -> None:
    planager = Planager.from_json(json_root)
    planager.derive_schedules()


def track(json_root: Path) -> None:
    planager = Planager.from_json(json_root)
    print("Welcome to planager tracking.")
    planager.track()


def dashboard(json_root: Path) -> None:
    planager = Planager.from_json(json_root)
    planager.show_dashboard()


def shift(json_root: Path) -> None:
    planager = Planager.from_json(json_root)
    _ndays = input("How many days would you like to shift the declaration back by?")
    ndays = int(_ndays)
    print(f"Shifting by {ndays}...")


commands_dict: dict[str, Callable] = {
    "interactive": interactive,
    "derive": derive,
    "plan": plan,
    "schedule": schedule,
    "track": track,
    "dashboard": dashboard,
    "shift": shift,
}
