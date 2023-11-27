from typing import Any, Dict, Optional

from ...util import PDate
from ..base.schedule import Schedule


class Schedules:
    """
    Container class for multiple instances of the Schedule class.
    """

    def __init__(self, schedules: Optional[Dict[PDate, Schedule]] = None) -> None:
        self._schedules: Dict[PDate, Schedule] = schedules or {}

    @classmethod
    def from_derivation(cls, schedules_derivation_dict: dict[str, Any]) -> "Schedules":
        ...  # TODO
        schedules_dict: dict[PDate, Schedule] = {}
        scheds = Schedules(schedules_dict)
        return scheds

    def as_dicts(self) -> list[dict[str, dict]]:
        return list(map(Schedule.as_dict, self._schedules.values()))

    def __len__(self) -> int:
        return len(self._schedules)

    def __getitem__(self, __key: PDate) -> Schedule:
        return self._schedules[__key]

    def __setitem__(self, __key: PDate, __value: Schedule) -> None:
        assert isinstance(__value, Schedule)
        self._schedules.update({__key: __value})
        # raise ValueError(f"Invalid indexed assignment: {{{str(__key)}: {str(__value)}}}")

    @property
    def summary(self) -> str:
        return "Schedules.summary property is not yet implemented."

    def __str__(self) -> str:
        return "\n".join(map(str, self._schedules.values()))

    def __repr__(self) -> str:
        return self.__str__()
