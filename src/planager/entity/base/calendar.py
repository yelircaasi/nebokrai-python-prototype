from pathlib import Path
from typing import Any, Dict

from ...util import Norg, PDate


class Day:
    def __init__(
        self,
        date: PDate,
        max_load: int = 240,
        routines: list = ["morning", "midday" "evening"],
        # **kwargs,
    ) -> None:
        self.date = date
        self.max_load = max_load
        self.routines = routines
        # self.__dict__.update(**kwargs)


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
