from typing import Callable

from .planager import Planager


def interactive() -> None:
    """
    Run planager in interactive mode as a CLI.
    """
    print("Welcome to interactive planager.")
    planager = Planager.from_json()
    print(planager.summary)


def derive() -> None:
    planager = Planager.from_json()
    planager.derive()


def plan() -> None:
    planager = Planager.from_json()
    planager.derive_plan()


def schedule() -> None:
    planager = Planager.from_json()
    planager.derive_schedules()


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


def shift() -> None:
    """
    Adjusts the declaration by shifting activities back a certain number of days.
    """
    planager = Planager.from_json()
    print(planager.summary)
    ndays = 999
    while ndays == 999:
        try:
            ndays = int(input("How many days would you like to shift the declaration back by?"))
        except ValueError:
            print("Invalid input. Please enter an integer.")
            ndays = 999
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
