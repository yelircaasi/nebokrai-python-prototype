def black(s: str) -> str:
    return f"\x1b[30m{s}\x1b[39m"


def red(s: str) -> str:
    return f"\x1b[31m{s}\x1b[39m"


def green(s: str) -> str:
    return f"\x1b[32m{s}\x1b[39m"


def yellow(s: str) -> str:
    return f"\x1b[33m{s}\x1b[39m"


def blue(s: str) -> str:
    return f"\x1b[34m{s}\x1b[39m"


def magenta(s: str) -> str:
    return f"\x1b[35m{s}\x1b[39m"


def cyan(s: str) -> str:
    return f"\x1b[36m{s}\x1b[39m"


def pblack(s: str) -> None:
    print(black(s))


def pred(s: str) -> None:
    print(red(s))


def pgreen(s: str) -> None:
    print(green(s))


def pyellow(s: str) -> None:
    print(yellow(s))


def pblue(s: str) -> None:
    print(blue(s))


def pmagenta(s: str) -> None:
    print(magenta(s))


def pcyan(s: str) -> None:
    print(cyan(s))
