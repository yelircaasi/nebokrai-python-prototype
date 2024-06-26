def wrap_as_list(
    line: str,
    width: int,
    trailing_spaces: int,
) -> list[str]:
    """
    Ensures that lines are below a specified length, sending the excess to the next line.
      Returns a list.
    """

    if len(line) < width:
        return [line]

    prefix = trailing_spaces * " "
    lines = []

    def splitline(s: str, width: int) -> tuple[str, str]:
        splitind = s[:width].rfind(" ")
        splitind = width if splitind == -1 else splitind
        line1 = s[:splitind].strip(" ")
        line2 = s[splitind:].strip(" ")
        return line1, line2

    line1, rest = splitline(line, width)
    lines.append(line1)
    width -= trailing_spaces

    while len(rest) > width:
        next_line, rest = splitline(rest, width)
        lines.append(prefix + next_line)

    if rest:
        lines.append(prefix + rest)

    return lines


def wrap_string(
    line: str,
    width: int,
    trailing_spaces: int = 2,
    borders: bool = False,
    border_char: str = "│",
    pad_char: str = " ",
    padding: int = 1,
) -> str:
    """
    Ensures that lines are below a specified length, sending the excess to the next line.
      Returns a string.
    """

    if borders:
        pad_chars = pad_char * padding
        bookend1, bookend2 = border_char + pad_chars, pad_chars + border_char
        width -= len(bookend1) + len(bookend2)
        lines_ = wrap_as_list(line, width, trailing_spaces)
        lines = list(map(lambda s: f"{bookend1}{s: <{width}}{bookend2}", lines_))
    else:
        lines = wrap_as_list(line, width, trailing_spaces)
    return "\n".join(lines)


def tabularize(
    s,
    width,
    padding: int = 1,
    pad_char: str = " ",
    trailing_spaces: int = 2,
    thick: bool = False,
):
    "Adds table borders to a string, wrapping it as needed."
    border_char = "┃" if thick else "│"
    return wrap_string(
        s,
        width,
        trailing_spaces=trailing_spaces,
        borders=True,
        border_char=border_char,
        pad_char=pad_char,
        padding=padding,
    )
