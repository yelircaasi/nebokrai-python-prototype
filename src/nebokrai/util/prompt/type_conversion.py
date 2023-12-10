import re
from typing import Callable, Optional

from ..elementary_types import (
    Natural,
    Nonnegative,
    PromptTypeName,
    TrackingActivityResponseType,
    prompt_type_mapping,
)
from ..nkdatetime import NKTime
from ..nkdatetime.nktime import NKTime

ConversionFuncType = Callable[[str], TrackingActivityResponseType]


def split_input_sequence(input_sequence_string: str) -> list[str]:
    return list(filter(bool, map(str.strip, re.split(r",?\s+|,", input_sequence_string.strip()))))


def convert_nonnegative(nonneg: str) -> Nonnegative:
    nnf = float(nonneg)
    if not nnf >= 0:
        raise ValueError
    return nnf


def convert_natural(nonneg_int: str) -> Natural:
    nni = int(nonneg_int)
    if not nni >= 0:
        raise ValueError
    return nni


def convert_integer_sequence(seq_string: str) -> list[Natural]:
    return list(map(int, split_input_sequence(seq_string)))


def convert_natural_sequence(seq_string: str) -> list[Natural]:
    return list(map(convert_natural, split_input_sequence(seq_string)))


def convert_nonnegative_sequence(seq_string: str) -> list[Nonnegative]:
    return list(map(convert_nonnegative, split_input_sequence(seq_string)))


def convert_time_amount(s: str) -> float:
    r"""
    Designed to accept string inputs of the form \d+ and \d\d?:\d\d and return a float in either
      case.
    """
    s = s.strip()
    if s.replace(".", "", 1).isdigit():
        return float(s)
    if ":" in s:
        nktime = NKTime.from_string(s)
        return float(60 * nktime.hour + nktime.minute)
    raise ValueError(f"Input string {s} cannot be converted to float.")


conversion_func_dict: dict[PromptTypeName, ConversionFuncType] = {
    "float": float,
    "integer": int,
    "integer_sequence": convert_integer_sequence,
    "natural": convert_natural,
    "natural_sequence": convert_natural_sequence,
    "nonnegative_sequence": convert_nonnegative_sequence,
    "nonnegative": convert_nonnegative,
    "boolean": lambda s: s.strip().lower() in {"y", "yes", "true", "done", "check"},
    "text": lambda x: x,
    "time_amount": convert_time_amount,
    "time": NKTime.from_string,
}
