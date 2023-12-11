import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional, Tuple, Union

import pytest

from nebokrai.util.elementary_types import TrackingActivityResponseType
from nebokrai.util.prompt import prompt_any
from nebokrai.util.prompt.prompt_config import PromptConfig

this_file = Path(__file__)


@dataclass
class TDataPaths:
    """
    Helper class for working with test data, found in …/nebokrai-py/test/data
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


def prompt_helper(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    pconf: PromptConfig,
    input_strings: Tuple[str, ...],
    expected_response: Optional[TrackingActivityResponseType],
    expected_error_message: Optional[str] = None,
) -> None:
    """
    Abstracts away the boilerplate code for testing input prompts.
    """
    string_iter = iter(input_strings)
    monkeypatch.setattr("builtins.input", lambda _: next(string_iter))  # type: ignore
    received = prompt_any(pconf)

    if expected_error_message is None:
        assert received == expected_response
    else:
        cap = capsys.readouterr()
        assert cap.out == expected_error_message
