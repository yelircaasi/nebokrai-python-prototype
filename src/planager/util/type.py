from typing import Dict, List, Optional, Tuple, Union

from ..config import ConfigType
from .pdatetime import PDate

ClusterType = List[List[Tuple[str, str, str]]]
# SubplanType = Dict[PDate, List[int]]
SubplanType = Dict[PDate, List[Tuple[str, str, str]]]
PDateInputType = Optional[
    Union["PDate", str, Tuple[str, str, str], Tuple[int, int], int]
]
