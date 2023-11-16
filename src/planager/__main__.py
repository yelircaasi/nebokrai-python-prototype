# https://docs.python.org/3/library/argparse.html#sub-commands
import argparse

from .cli import commands_dict


def get_arg_parser() -> argparse.ArgumentParser:
    arg_parser = argparse.ArgumentParser(prog="planager")
    arg_parser.add_argument(
        "action",
        type=str,
        choices=[
            "derive",
            "plan",
            "schedule",
            "track",
            "dashboard",
            "shift",
            "interactive",
        ],
        default="derive",
        help="help for action",
    )
    arg_parser.add_argument(
        "--json_root", "-j", required=False, default="", help="help for json_root"
    )
    arg_parser.add_argument(
        "--num_days", "-n", type=int, required=False, default=1, help="help for num_days_to_shift"
    )
    arg_parser.add_argument(
        "--algorithm",
        "-a",
        choices=["rigid"],
        required=False,
        default="rigid",
        help="help for num_days_to_shift",
    )

    return arg_parser


def main() -> None:
    parser = get_arg_parser()
    args = parser.parse_args()

    commands_dict[args.action]()


if __name__ == "__main__":
    main()
