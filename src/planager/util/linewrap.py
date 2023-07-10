def wrap_string(
    line: str,
    width: int = 80,
    trailing_spaces: int = 2,
    borders: bool = False,
    border_char: str = "│",
) -> str:
    if len(line) < width:
        return line
    width -= trailing_spaces - 4 * borders
    lines = []
    while len(line) > width:
        splitind = line[:width].rfind(" ")
        lines.append(trailing_spaces * " " + line[:splitind])
        line = line[splitind + 1 :]
    lines.append(trailing_spaces * " " + line)
    lines[0] = lines[0][trailing_spaces:]
    if borders:
        lines_ = list(
            map(lambda s: f"{border_char} {s: <{width}} {border_char}", lines)
        )
    return "\n".join(lines)
