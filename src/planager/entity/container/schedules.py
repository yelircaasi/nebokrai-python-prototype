from typing import Dict, Optional

from ...config import Config
from ...util import PDate
from ..base.schedule import Schedule


class Schedules:
    """
    Container class for multiple instances of the Schedule class.
    """

    def __init__(self, config: Config, schedules: Optional[Dict[PDate, Schedule]]) -> None:
        self.config = config
        self._schedules: Dict[PDate, Schedule] = schedules or {}

    def __len__(self) -> int:
        return len(self._schedules)

    def __getitem__(self, __key: PDate) -> Schedule:
        return self._schedules[__key]

    def __setitem__(self, __key: PDate, __value: Schedule) -> None:
        assert isinstance(__value, Schedule)
        self._schedules.update({__key: __value})
        raise ValueError(f"Invalid indexed assignment: {{{str(__key)}: {str(__value)}}}")

    def __str__(self) -> str:
        return "\n".join(map(str, self._schedules.values()))

    def __repr__(self) -> str:
        return self.__str__()
