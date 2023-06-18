import re
from typing import Union


def tabularize(s, width, pad: int = 0):
    padding = pad * " "
    return f"┃ {padding}{str(s): <{width - 4 - pad}} ┃"


def round5(number: Union[int, float]) -> int:
    return int(5 * round(number / 5))


def expand_task_segments(task_abbr: str) -> list:
    def expand_block(block):
        if not task_abbr:
            return []
        error = ValueError(
            f"Tasks string (item '{block}') not of a suitable form."
            + r"Acceptable: \d{1, 3}(-\d{1, 3})?([A-Z]\d{0, 2}(-[A-Z]\d{0, 2})?)?"
        )
        if block.isnumeric():
            return list(map(str, range(1, int(block) + 1)))

        elif re.match(r"\w?\d\d?-", block):
            try:
                start, end = block.split("-")
            except:
                print(block)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if start.isnumeric() and end.isnumeric():
                return list(map(str, range(int(start), int(end) + 1)))
            elif start.isalpha() and end.isalpha():
                return list(map(chr, range(ord(start), ord(end) + 1)))
            elif start.isalnum() and end.isalnum():
                try:
                    start_letter = start[0]
                    start_number = int(start[1:])
                    end_isalpha = (end_letter := end[0]).isalpha()
                    if end_isalpha and (start_letter != end_letter):
                        raise error
                    end_number = int(end[1:]) if end_isalpha else int(end)
                    print(start_letter, end_letter, start_number, end_number)

                    return list(
                        map(
                            lambda num: start_letter + str(num),
                            range(start_number, end_number + 1),
                        )
                    )
                except:
                    raise error
            else:
                raise error
        else:
            return [block]

    tasks = []
    blocks = task_abbr.split(",")
    for block in blocks:
        tasks.extend(expand_block(block))
    return tasks
