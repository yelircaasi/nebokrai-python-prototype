from .entity_ids import TaskID
from .pdatetime import PDate

ClusterType = list[list[TaskID]]
# SubplanType = dict[PDate, list[int]]
SubplanType = dict[PDate, list[TaskID]]
