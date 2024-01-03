import sys
from .cli import commands_dict, error_help_wrapped


def main() -> None:
    # parser = build_arg_parser()
    # args = parser.parse_args()
    # if "action" not in args:
    #     args.action = "interactive"

    action = " ".join(sys.argv[1:])
    # print(action)
    commands_dict.get(action, error_help_wrapped(action))()


if __name__ == "__main__":
    main()
