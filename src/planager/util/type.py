from .pdatetime import PDate
from .entity_ids import TaskID

ClusterType = list[list[TaskID]]
# SubplanType = dict[PDate, list[int]]
SubplanType = dict[PDate, list[TaskID]]
