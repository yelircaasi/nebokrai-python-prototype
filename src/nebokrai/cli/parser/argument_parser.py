# # https://docs.python.org/3/library/argparse.html#sub-commands
# # https://realpython.com/command-line-interfaces-python-argparse/#setting-up-your-cli-apps-layout-and-build-system

# import argparse


# def build_arg_parser() -> argparse.ArgumentParser:
#     arg_parser = argparse.ArgumentParser(prog="nebokrai", allow_abbrev=True)
#     # arg_parser.add_argument(
#     #     "action",
#     #     type=str,
#     #     choices=[
#     #         "derive",
#     #         "plan",
#     #         "schedule",
#     #         "track",
#     #         "dashboard",
#     #         "shift",
#     #         "interactive",
#     #     ],
#     #     default="derive",
#     #     help="help for action",
#     # )

#     # arg_parser.add_argument(
#     #     "--json_root", "-j", required=False, default="", help="help for json_root"
#     # )
#     # arg_parser.add_argument(
#     #     "--num_days", "-n", type=int, required=False, default=1, help="help for num_days_to_shift"
#     # )
#     # arg_parser.add_argument(
#     #     "--algorithm",
#     #     "-a",
#     #     choices=["rigid"],
#     #     required=False,
#     #     default="rigid",
#     #     help="help for num_days_to_shift",
#     # )
#     subparsers = arg_parser.add_subparsers(help="Help for sub-commands:")

#     # parser_a = subparsers.add_parser("a", help="a help")
#     # parser_a.add_argument("bar", type=int, help="bar help")
#     # parser_b = subparsers.add_parser("b", help="b help")
#     # parser_b.add_argument("--baz", choices="XYZ", help="baz help")

#     parser_interactive: argparse.ArgumentParser = subparsers.add_parser(
#         "interactive",
#         aliases=["int"],
#         help="run nebokrai as an interactive command-line program",
#         allow_abbrev=True,
#     )
#     parser_validate: argparse.ArgumentParser = subparsers.add_parser(
#         "validate", aliases=["val"], help="validate declaration data"
#     )
#     parser_derive: argparse.ArgumentParser = subparsers.add_parser(
#         "derive", aliases=["der"], help="perform a derivation (default: both plan and schedules)"
#     )
#     parser_track: argparse.ArgumentParser = subparsers.add_parser(
#         "track", aliases=["tr"], help="perform activity tracking"
#     )
#     parser_x: argparse.ArgumentParser = subparsers.add_parser(
#         "x", aliases=["check", "mark"], help="check off an item (default: task)"
#     )
#     parser_declaration: argparse.ArgumentParser = subparsers.add_parser(
#         "declaration", aliases=["dec"], help="manage declaration files and their contents"
#     )
#     parser_derivation: argparse.ArgumentParser = subparsers.add_parser(
#         "derivation", aliases=["drn", "drvn"], help="manage derivation files and their contents"
#     )
#     parser_tracking: argparse.ArgumentParser = subparsers.add_parser(
#         "tracking",
#         aliases=["tg", "trng"],
#         help="view and browse tracking activities and their associated information",
#     )
#     parser_sync: argparse.ArgumentParser = subparsers.add_parser(
#         "sync", help="sync data with a sync server (default: both declaration and derivation)"
#     )
#     parser_generations: argparse.ArgumentParser = subparsers.add_parser(
#         "generations",
#         aliases=["gen", "gens"],
#         help="view and manage past generations (iterations of declaration-derivation pairs)",
#     )
#     parser_revert: argparse.ArgumentParser = subparsers.add_parser(
#         "revert", aliases=["rev"], help="go back to a previous generation (default: penultimate)"
#     )
#     parser_dashboard: argparse.ArgumentParser = subparsers.add_parser(
#         "dashboard", aliases=["dash", "-"], help="view or export dashboard"
#     )

#     # parser_interactive.add_argument(
#     #     "--action",
#     #     type=str,
#     #     choices=[],
#     #     default="interactive",
#     #     required=False,
#     #     help="help for action",
#     # )

#     subparsers_validate = parser_validate.add_subparsers()
#     subparsers_derive = parser_derive.add_subparsers()
#     # subparsers_track = parser_track.add_subparsers()
#     # subparsers_x = parser_x.add_subparsers()
#     subparsers_declaration = parser_declaration.add_subparsers()
#     subparsers_derivation = parser_derivation.add_subparsers()
#     subparsers_tracking = parser_tracking.add_subparsers()
#     # subparsers_sync = parser_sync.add_subparsers()
#     # subparsers_generations = parser_generations.add_subparsers()
#     # subparsers_revert = parser_revert.add_subparsers()
#     subparsers_dashboard = parser_dashboard.add_subparsers()

#     subparser_validate_all: argparse.ArgumentParser = subparsers_validate.add_parser("all")
#     subparser_validate_calendar: argparse.ArgumentParser = subparsers_validate.add_parser(
#         "calendar"
#     )
#     subparser_validate_config: argparse.ArgumentParser = subparsers_validate.add_parser("config")
#     subparser_validate_roadmaps: argparse.ArgumentParser = subparsers_validate.add_parser(
#         "roadmaps"
#     )
#     subparser_validate_routines: argparse.ArgumentParser = subparsers_validate.add_parser(
#         "routines"
#     )
#     subparser_validate_tracking: argparse.ArgumentParser = subparsers_validate.add_parser(
#         "tracking"
#     )

#     subparser_derive_dryrun: argparse.ArgumentParser = subparsers_derive.add_parser("dryrun")
#     subparser_derive_dryrun_accept: argparse.ArgumentParser = subparsers_derive.add_parser(
#         "dryrun-accept"
#     )
#     subparser_derive_plan: argparse.ArgumentParser = subparsers_derive.add_parser("plan")
#     subparser_derive_schedules: argparse.ArgumentParser = subparsers_derive.add_parser("schedules")

#     # subparser_track: argparse.ArgumentParser = subparsers_track.add_parser("")

#     # subparser_x: argparse.ArgumentParser = subparsers_x.add_parser("")

#     subparser_declaration_add: argparse.ArgumentParser = subparsers_declaration.add_parser("add")
#     subparser_declaration_remove: argparse.ArgumentParser = subparsers_declaration.add_parser(
#         "remove"
#     )
#     subparser_declaration_edit: argparse.ArgumentParser = subparsers_declaration.add_parser("edit")
#     subparser_declaration_search: argparse.ArgumentParser = subparsers_declaration.add_parser(
#         "search"
#     )
#     subparser_declaration_export: argparse.ArgumentParser = subparsers_declaration.add_parser(
#         "export"
#     )

#     subparser_derivation_blame: argparse.ArgumentParser = subparsers_derivation.add_parser("blame")
#     subparser_derivation_summarize: argparse.ArgumentParser = subparsers_derivation.add_parser(
#         "summarize"
#     )
#     subparser_derivation_search: argparse.ArgumentParser = subparsers_derivation.add_parser(
#         "search"
#     )
#     subparser_derivation_debug: argparse.ArgumentParser = subparsers_derivation.add_parser("debug")
#     subparser_derivation_export: argparse.ArgumentParser = subparsers_derivation.add_parser(
#         "export"
#     )

#     subparser_tracking_search: argparse.ArgumentParser = subparsers_tracking.add_parser("search")

#     # subparser_sync: argparse.ArgumentParser = subparsers_sync.add_parser("")

#     # subparser_generations_: argparse.ArgumentParser = subparsers_generations.add_parser("")

#     # subparser_revert_: argparse.ArgumentParser = subparsers_revert.add_parser("")

#     subparser_dashboard_view: argparse.ArgumentParser = subparsers_dashboard.add_parser("view")
#     subparser_dashboard_debug: argparse.ArgumentParser = subparsers_dashboard.add_parser("debug")
#     subparser_dashboard_export: argparse.ArgumentParser = subparsers_dashboard.add_parser("export")

#     subparser_validate_all.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_validate_calendar.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_validate_config.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_validate_config.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_validate_roadmaps.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )

#     subparser_validate_routines.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_validate_tracking.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derive_dryrun.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derive_dryrun_accept.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derive_plan.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derive_schedules.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_declaration_add.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_declaration_add.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_declaration_remove.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_declaration_edit.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_declaration_search.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_declaration_export.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derivation_blame.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derivation_summarize.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derivation_search.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derivation_debug.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_derivation_export.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_tracking_search.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_dashboard_view.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_dashboard_debug.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )
#     subparser_dashboard_export.add_argument(
#         "--action",
#         type=str,
#         choices=[],
#         default="dashboard_view_interactive",
#         required=False,
#         help="help for action",
#     )


#     # subparsers_derive: argparse.ArgumentParser = parser_derive.add_subparsers(
#     #     "", aliases=[""], help=""
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_track.add_parser(
#     #     "", aliases=[""], help=""
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_x.add_parser(
#     #     "", aliases=["", ""], help=""
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_declaration.add_parser(
#     #     "", aliases=[""], help=""
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_derivation.add_parser(
#     #     "", aliases=["", ""], help=""
#     # )
#     # subparser_parser: argparse.ArgumentParser = parser_tracking.add_parser(
#     #     "",
#     #     aliases=["", ""],
#     #     help="",
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_sync.add_parser(
#     #     "", help=""
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_generations.add_parser(
#     #     "",
#     #     aliases=["", ""],
#     #     help="",
#     # )
#     # subparser_
#     # : argparse.ArgumentParser = parser_revert.add_parser(
#     #     "", aliases=[""], help=""
#     # )
#     # subparser_dashboard

#     return arg_parser
