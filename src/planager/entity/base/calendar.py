from pathlib import Path
from typing import Any, Dict

from ...util import Norg, PDate
from ..container.entries import Entries


class Day:
    def __init__(
        self,
        date: PDate,
        entries: Entries = Entries(),
        max_load: int = 240,
        routines: list = ["morning", "midday" "evening"],
    ) -> None:
        self.date = date
        self.entries = entries
        self.max_load = max_load
        self.routines = routines


class Calendar:
    def __init__(self) -> None:
        self.days: Dict[PDate, Day] = {}

    def copy(self) -> "Calendar":
        cal = Calendar()
        cal.days = {k.copy(): v.copy() for k, v in self.days.items()}
        return cal
    
    def add(self, day: Day) -> None:
        self.days.update({day.date: day})

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Calendar":
        cal = Calendar()
        file = workspace_dir / "calendar.norg"
        norg = Norg.from_path(file)
        for item in norg.items:
            date_str = item.name
            pdate = PDate.from_string(str(date_str))
            if pdate:
                date = pdate
            else:
                raise ValueError("Date not parsable: {date_str}")
            # attributes = section.get_attributes(section.text)
            cal.add(
                Day(
                    date,
                    # **attributes
                )
            )

        return cal

    @property
    def start_date(self) -> PDate:
        return min(self.days)

    @property
    def end_date(self) -> PDate:
        return max(self.days)

    def __getitem__(self, __name: str) -> Any:
        item = ...
        return item

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    def __str__(self) -> str:
        return "need to implement this"
    
    def __repr__(self) -> str:
        return self.__str__()
