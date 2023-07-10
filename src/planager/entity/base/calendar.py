from pathlib import Path
from typing import Any, Dict

from planager.util.data.norg.norg_util import Norg
from planager.util.datetime_extensions import PDate


class Day:
    def __init__(
        self,
        date: PDate,
        max_load: int = 240,
        routines: list = ["morning", "midday" "evening"],
        **kwargs,
    ) -> None:
        self.date = date
        self.max_load = max_load
        self.routines = routines
        self.__dict__.update(**kwargs)


class Calendar:
    def __init__(self) -> None:
        self.days: Dict[PDate, Day] = {}

    def __getitem__(self, __name: str) -> Any:
        item = ...
        return item

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    def start(self) -> PDate:
        return min(self.days)

    def end(self) -> PDate:
        return max(self.days)

    def add(self, day: Day) -> None:
        self.days.update({day.date: day})

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Calendar":
        cal = Calendar()
        file = workspace_dir / "calendar.norg"
        parsed = Norg.from_path(file)
        for section in parsed.sections:
            date = section["title"]
            attributes = Norg.get_attributes(section["text"])
            date = PDate.from_string(date)
            cal.add(Day(date, **attributes))

        return cal
