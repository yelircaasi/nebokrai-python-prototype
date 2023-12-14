import sys
from .cli import commands_dict


def main() -> None:
    # parser = build_arg_parser()
    # args = parser.parse_args()
    # if "action" not in args:
    #     args.action = "interactive"

    action = ' '.join(sys.argv[1:])
    print(action)
    commands_dict[action]()


if __name__ == "__main__":
    main()
