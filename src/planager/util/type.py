from typing import Dict, List, Optional, Tuple, Union

from ..config import ConfigType
from .pdatetime import PDate

ClusterType = List[List[Tuple[int, int, int]]]
# SubplanType = Dict[PDate, List[int]]
SubplanType = Dict[PDate, List[Tuple[int, int, int]]]
PDateInputType = Optional[Union["PDate", str, Tuple[int, int, int], int]]
