from typing import List, Tuple

import pytest

from planager.util.type import ClusterType


class TypeTest:
    def test_ClusterType(self) -> None:
        assert ClusterType == List[List[Tuple[str, str, str]]]
