from typing import Union


def round5(number: Union[int, float]) -> int:
    return int(5 * round(number / 5 + 0.01))
