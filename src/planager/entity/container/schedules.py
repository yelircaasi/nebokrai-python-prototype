from typing import Any, Dict, Optional

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

    def __getitem__(self, __key: Any) -> Schedule:
        __key = PDate.ensure_is_pdate(__key)
        if not __key:
            raise ValueError(f"Date not in schedules: {str(__key)}")
        return self._schedules[__key]

    def __setitem__(self, __key: Any, __value: Any) -> None:
        assert isinstance(__value, Schedule)
        __key = PDate.ensure_is_pdate(__key)
        if not __key:
            raise ValueError(f"Date not in schedules: {str(__key)}")
        self._schedules.update({__key: __value})

    def __str__(self) -> str:
        return "\n".join(map(str, self._schedules.values()))

    def __repr__(self) -> str:
        return self.__str__()
