from typing import Dict, Optional

from nebokrai.util import color

from ...util import NKDate
from ...util.serde.custom_dict_types import ScheduleDictParsed, ScheduleDictRaw
from ..base.schedule import Schedule


class Schedules:
    """
    Container class for multiple instances of the Schedule class.
    """

    def __init__(self, schedules: Optional[Dict[NKDate, Schedule]] = None) -> None:
        self._schedules: Dict[NKDate, Schedule] = schedules or {}

    @classmethod
    def from_derivation(cls, schedules_derivation_dict: ScheduleDictParsed) -> "Schedules":
        """
        Create an instance from the dictionary read from from derivation/schedules.json.
        """
        print(schedules_derivation_dict)  # TODO
        schedules_dict: dict[NKDate, Schedule] = {}
        scheds = Schedules(schedules_dict)
        return scheds

    def serializes(self) -> list[ScheduleDictRaw]:
        return list(map(Schedule.serialize, self._schedules.values()))

    def __len__(self) -> int:
        return len(self._schedules)

    def __getitem__(self, __key: NKDate) -> Schedule:
        return self._schedules[__key]

    def __setitem__(self, __key: NKDate, __value: Schedule) -> None:
        assert isinstance(__value, Schedule)
        self._schedules.update({__key: __value})

    @property
    def summary(self) -> str:
        return "Schedules.summary property is not yet implemented."

    def __str__(self) -> str:
        return "\n".join(map(str, self._schedules.values()))

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def repr1(self) -> str:
        return color.red(" | ").join(map(lambda e: e.repr1, self))
