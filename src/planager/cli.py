import json
from typing import Callable

from .configuration import path_manager
from .planager import Planager
from .util import prompt_integer
from .validation import validate_declaration


def interactive() -> None:
    """
    Run planager in interactive mode as a CLI.
    """
    print("Welcome to interactive planager.")
    planager = Planager()
    print(planager.summary)


def validate() -> None:
    """
    CLI to validate the data found in the planager root folder. Non-destructive.
    """
    validate_declaration(path_manager.declaration)


def declare() -> None:
    """
    CLI to create or edit the declaration.json file interactively.
    """
    planager = Planager()
    planager.declare_interactive()


def derive() -> None:
    """
    CLI to derive and write the plan and schedules from the declaration file.
    """
    planager = Planager()
    planager.derive()
    planager.save_derivation()


def plan() -> None:
    """
    Derive and save only plan.
    """
    planager = Planager()
    planager.derive_plan()
    planager.save_plan()


def schedule() -> None:
    """
    Derive and save only schedule.
    """
    planager = Planager()
    planager.derive_schedules()
    planager.save_schedules()


def track() -> None:
    """
    Enters interactive CLI prompt, allowing the user to track activities.
    """
    planager = Planager()
    print("Welcome to planager tracking.")
    planager.track()


def dashboard() -> None:
    """
    Show the dashboard, a visualization of the progress one has made.
    """
    planager = Planager()
    planager.show_dashboard()


def shift() -> None:  # WORKS!
    """
    Adjusts the declaration by shifting activities back a certain number of days.
    """
    planager = Planager()
    print(planager.summary)
    ndays = prompt_integer(
        "How many days would you like to shift the declaration back by? ",
        "Invalid input. Please enter an integer.",
    )
    print(f"Shifting declaration back by {ndays} days...")
    planager.shift_declaration(ndays)


def lint() -> None:
    """
    Checks the declaration.json file specified for validity.
    """
    with open(path_manager.declaration, encoding="utf-8") as f:
        declaration = json.load(f)
    print(declaration)
    print("Not yet implemented!")


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
