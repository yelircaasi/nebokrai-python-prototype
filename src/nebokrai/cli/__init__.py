from typing import Callable

from ..configuration import path_manager
from ..nebokrai import NebokraiEntryPoint
from ..util.prompt import prompt_any
from ..util.prompt.prompt_config import PromptConfig
from ..validation import validate_declaration
from .commands import (
    check_off_interactive,
    dashboard_debug,
    dashboard_export,
    dashboard_interactive,
    dashboard_view,
    declaration_add,
    declaration_edit,
    declaration_export,
    declaration_interactive,
    declaration_remove,
    declaration_search,
    derivation_blame,
    derivation_debug,
    derivation_export,
    derivation_interactive,
    derivation_search,
    derivation_summarize,
    derive_dryrun,
    derive_dryrun_accept,
    derive_interactive,
    derive_plan,
    derive_schedules,
    generations_interactive,
    interactive,
    revert_interactive,
    summary,
    sync_noninteractive,
    track_interactive,
    tracking_interactive,
    tracking_search,
    validate_all,
    validate_calendar,
    validate_config,
    validate_interactive,
    validate_roadmaps,
    validate_routines,
    validate_tracking,
)
# from .parser import build_arg_parser

# def interactive() -> None:
#     """
#     Run nebokrai in interactive mode as a CLI.
#     """
#     print("Welcome to interactive nebokrai.")
#     nebokrai = NebokraiEntryPoint()
#     print(nebokrai.summary)


# def validate() -> None:
#     """
#     CLI to validate the data found in the nebokrai root folder. Non-destructive.
#     """
#     validate_declaration(path_manager.declaration_dir)


# def declare() -> None:
#     """
#     CLI to create or edit the declaration.json file interactively.
#     """
#     nebokrai = NebokraiEntryPoint()
#     nebokrai.declare_interactive()


# def derive() -> None:
#     """
#     CLI to derive and write the plan and schedules from the declaration file.
#     """
#     nebokrai = NebokraiEntryPoint()
#     nebokrai.derive()
#     nebokrai.save_derivation()


# def plan() -> None:
#     """
#     Derive and save only plan.
#     """
#     nebokrai = NebokraiEntryPoint()
#     nebokrai.derive_plan()
#     nebokrai.save_plan()


# def schedule() -> None:
#     """
#     Derive and save only schedule.
#     """
#     nebokrai = NebokraiEntryPoint()
#     nebokrai.derive_schedules()
#     nebokrai.save_schedules()


# def track() -> None:
#     """
#     Enters interactive CLI prompt, allowing the user to track activities.
#     """
#     nebokrai = NebokraiEntryPoint()
#     print("Welcome to nebokrai tracking.")
#     nebokrai.track()


# def dashboard() -> None:
#     """
#     Show the dashboard, a visualization of the progress one has made.
#     """
#     nebokrai = NebokraiEntryPoint()
#     nebokrai.show_dashboard()


# def shift() -> None:  # WORKS!
#     """
#     Adjusts the declaration by shifting activities back a certain number of days.
#     """
#     nebokrai = NebokraiEntryPoint()
#     print(nebokrai.summary)
#     ndays = prompt_any(
#         PromptConfig(
#             "integer",
#             prompt_message="How many days would you like to shift the declaration back by? ",
#         )
#     )
#     assert isinstance(ndays, int)
#     print(f"Shifting declaration back by {ndays} days...")
#     nebokrai.shift_declaration(ndays)


# def lint() -> None:
#     """
#     Checks the declaration.json file specified for validity.
#     """
#     # with open(path_manager.declaration, encoding="utf-8") as f:
#     #     declaration = json.load(f)
#     # print(declaration)
#     print("Not yet implemented!")


commands_dict: dict[str, Callable] = {
    "": interactive,
    "interactive": interactive,
    "summary": summary,
    "validate": validate_interactive,
    "validate all": validate_all,
    "validate calendar": validate_calendar,
    "validate config": validate_config,
    "validate roadmaps": validate_roadmaps,
    "validate routines": validate_routines,
    "validate tracking": validate_tracking,
    "derive": derive_interactive,
    "derive dryrun": derive_dryrun,
    "derive dryrun-accept": derive_dryrun_accept,
    "derive plan": derive_plan,
    "derive schedules": derive_schedules,
    "track": track_interactive,
    "x": check_off_interactive,
    "declaration": declaration_interactive,
    "declaration add": declaration_add,
    "declaration remove": declaration_remove,
    "declaration edit": declaration_edit,
    "declaration search": declaration_search,
    "derivation": derivation_interactive,
    "declaration export": declaration_export,
    "derivation": derivation_interactive,
    "derivation blame": derivation_blame,
    "derivation summarize": derivation_summarize,
    "derivation search": derivation_search,
    "derivation debug": derivation_debug,
    "derivation export": derivation_export,
    "tracking": tracking_interactive,
    "tracking search": tracking_search,
    "sync": sync_noninteractive,
    "generations": generations_interactive,
    "revert": revert_interactive,
    "dashboard": dashboard_interactive,
    "dashboard view": dashboard_view,
    "dashboard debug": dashboard_debug,
    "dashboard export": dashboard_export,
    # "declare": declare,
    # "derive": derive,
    # "lint": lint,
    # "plan": plan,
    # "schedule": schedule,
    # "track": track,
    # "dashboard": dashboard,
    # "shift": shift,
}


__all__ = ["build_arg_parser", "commands_dict"]
