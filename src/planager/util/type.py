from .pdatetime import PDate

ClusterType = list[list[tuple[str, str, str]]]
# SubplanType = dict[PDate, list[int]]
SubplanType = dict[PDate, list[tuple[str, str, str]]]
