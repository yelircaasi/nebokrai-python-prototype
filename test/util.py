import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import pytest
from pytest import monkeypatch

from planager.util.elementary_types import TrackingActivityType

this_file = Path(__file__)


@dataclass
class TDataPaths:
    """
    Helper class for working with test data, found in …/planager-py/test/data
    """

    tdatamanager_path: Path = this_file
    data_dir: Path = this_file.parent / "data"
    input1 = data_dir / "json_directory1"
    input2 = data_dir / "json_directory2"
    input3 = data_dir / "json_directory3"
    json_dirs = [input1, input2, input3]
    expected1 = data_dir / "json_expected1"
    expected2 = data_dir / "json_expected2"
    expected3 = data_dir / "json_expected3"


# def prompt_helper_simple(
#     input_str: str, expected: Any, prompt_function: Callable[[str, str, str], Any], *args
# ) -> None:
#     monkeypatch.setattr("builtins.input", lambda _: input_str)
#     received = prompt_function(*args)
#     return received == expected


# def make_new_input(output: TrackingActivityType) -> Callable[[str], TrackingActivityType]:
#     def inner(prmpt: str) -> str:
#         sys.stdout.write(prmpt)
#         return output

#     return inner
