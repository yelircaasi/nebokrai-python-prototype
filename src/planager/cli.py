import json
from pathlib import Path
from typing import Callable

from .planager import Planager, path_manager
from .util import prompt_integer
from .validation import validate_declaration


def interactive() -> None:
    """
    Run planager in interactive mode as a CLI.
    """
    print("Welcome to interactive planager.")
    planager = Planager.from_json()
    print(planager.summary)


def validate() -> None:
    validate_declaration(path_manager.declaration)


def declare() -> None:
    planager = Planager.from_json()
    planager.declare_interactive()


def derive() -> None:
    planager = Planager.from_json()
    planager.derive()
    planager.save_derivation()


def plan() -> None:
    planager = Planager.from_json()
    planager.derive_plan()
    planager.save_plan()


def schedule() -> None:
    planager = Planager.from_json()
    planager.derive_schedules()
    planager.save_schedules()


def track() -> None:
    """
    Enters interactive CLI prompt, allowing the user to track activities.
    """
    planager = Planager.from_json()
    print("Welcome to planager tracking.")
    planager.track()


def dashboard() -> None:
    planager = Planager.from_json()
    planager.show_dashboard()


def shift() -> None:  # WORKS!
    """
    Adjusts the declaration by shifting activities back a certain number of days.
    """
    planager = Planager.from_json()
    print(planager.summary)
    ndays = prompt_integer(
        "How many days would you like to shift the declaration back by? ",
        "Invalid input. Please enter an integer.",
    )
    print(f"Shifting declaration back by {ndays} days...")
    Planager.shift_declaration(ndays)


def lint() -> None:
    """
    Checks the declaration.json file specified for validity.
    """
    with open(path_manager.declaration, encoding="utf-8") as f:
        declaration = json.load(f)


commands_dict: dict[str, Callable] = {
    "interactive": interactive,
    "declare": declare,
    "derive": derive,
    "lint": lint,
    "plan": plan,
    "schedule": schedule,
    "track": track,
    "dashboard": dashboard,
    "shift": shift,
}
