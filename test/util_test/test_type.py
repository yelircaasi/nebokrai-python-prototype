from typing import Tuple

import pytest

from planager.util.type import ClusterType


class TypeTest:
    def test_ClusterType(self) -> None:
        assert ClusterType == list[list[tuple[str, str, str]]]
