from pathlib import Path
from typing import Any, Dict

from ...util import Norg, PDate, round5, tabularize
from ..base.schedule import Schedule


class Schedules:
    def __init__(self, schedules: Dict[PDate, Schedule] = {}) -> None:
        self._schedules: Dict[PDate, Schedule] = schedules

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

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Schedules":
        file = workspace_dir / "roadmaps.norg"
        parsed: Norg = Norg.from_path(file)
        ...  # TODO
        return cls()

    def __str__(self) -> str:
        return "\n".join(map(str, self._schedules.values()))

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self._schedules)
