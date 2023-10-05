from pathlib import Path
from typing import Any, Iterable, Optional, Union

from ...util.pdatetime.ptime import PTime
from ..container.routines import Routines
from .entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from ...util import Norg, PDate, tabularize
from ..container.entries import Entries


class Day:
    """
    Designed as a component of `Calendar`. To be used as an input to scheduling,
      contining most importantly the max load, routines, and the 'big rock' entries planned in advance,
      around which other entries are to be automatically be scheduled.
    """

    DAY_START_DEFAULT: PTime = PTime(5)
    DAY_END_DEFAULT: PTime = PTime(22)
    WIDTH: int = 80

    def __init__(
        self,
        date: PDate,
        entries: Entries = Entries(),
        routine_names: list[str] = [
            "Morning Routine",
            "Midday Routine",
            "Evening Routine",
        ],
        start: PTime = PTime(5),
        end: PTime = PTime(21),
    ) -> None:
        self.date = date
        self.entries = entries
        self.routine_names = routine_names

        # self.entries.insert(0, FIRST_ENTRY)
        # self.entries.append(LAST_ENTRY)
        waketime = min(start, self.entries.start)
        bedtime = max(end, self.entries.end)
        morning_sleep = Entry(
            "Sleep", PTime(0), end=waketime, priority=70, ismovable=False
        )
        evening_sleep = Entry(
            "Sleep", bedtime, end=PTime(24), priority=70, ismovable=False
        )
        # print(entries)
        if self.entries:
            first_entry = self.entries[0]
            last_entry = self.entries[-1]

            if first_entry.name.lower() == "sleep":
                pass
            elif first_entry.overlaps(morning_sleep):
                raise ValueError("\n".join(("", str(first_entry), str(morning_sleep))))
            else:
                self.entries.insert(0, morning_sleep)

            if last_entry.name.lower() == "sleep":
                pass
            elif last_entry.overlaps(evening_sleep):
                raise ValueError("")
            else:
                self.entries.append(evening_sleep)

        else:
            self.entries.append(morning_sleep)
            self.entries.append(evening_sleep)

    def copy(self) -> "Day":
        return Day(self.date.copy(), self.entries.copy(), self.routine_names.copy())

    # @classmethod
    # def default_day(cls, date: PDate) -> "Day":
    #     return cls(
    #         date
    #         entries: Entries = Entries(),
    #         routine_names: list[str] = [
    #             "Morning Routine",
    #             "Midday Routine",
    #             "Evening Routine",
    #         ],
    #         start: PTime = PTime(5),
    #         end: PTime = PTime(21),
    #     )

    @classmethod
    def from_dict(cls, date: PDate, day_dict: dict[str, Any]) -> "Day":
        entries = Entries()
        for entry_dict in day_dict["entries"]:
            entries.append(Entry.from_dict(entry_dict))

        routine_names = []
        for routine_dict in day_dict["routines"]:
            routine_names.append(routine_dict["name"])

        start = PTime.from_string(day_dict.get("start", str(cls.DAY_START_DEFAULT)))
        end = PTime.from_string(day_dict.get("end", str(cls.DAY_END_DEFAULT)))

        # print(entries)

        return cls(date, entries, routine_names, start=start, end=end)

    @property
    def available(self) -> int:
        return sum(map(lambda e: e.normaltime * (e.priority > 0), self.entries))

    def __str__(self) -> str:
        width = self.WIDTH
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        header_thickbeam = "┣━━━━━━━━━━━━━┯" + (width - 16) * "━" + "┫\n"
        header_thinbeam = "\n┠─────────────┴" + (width - 16) * "─" + "┨\n"
        thinbeam = "\n┠" + +(width - 2) * "─" + "┨\n"
        bottombeam = "\n┣" + (width - 2) * "━" + "┫\n"
        header = (
            header_thickbeam
            + tabularize(str(self.date) + "  │", width, thick=True)
            + header_thinbeam
            + tabularize(", ".join(self.routine_names), width, thick=True)
            + "\n"
            # + thickbeam
        )

        return header + "\n".join(map(str, self.entries)) + bottombeam


class Calendar:
    def __init__(self, days: Union[dict[PDate, Day], Iterable[Day]] = {}) -> None:
        self.days: dict[PDate, Day] = (
            days if isinstance(days, dict) else {d.date: d for d in days}
        )

    @classmethod
    def from_dict(cls, calendar_dict: dict[str, Any]) -> "Calendar":
        days = {}
        for date_string, day_dict in calendar_dict["days"].items():
            day_date = PDate.from_string(date_string)
            day = Day.from_dict(day_date, day_dict)
            days.update({day_date: day})

        return cls(days)

    # @classmethod
    # def from_norg_workspace(cls, workspace_dir: Path) -> "Calendar":
    #     cal = Calendar()
    #     file = workspace_dir / "calendar.norg"
    #     norg = Norg.from_path(file)
    #     for item in norg.items:
    #         date_str = item.name
    #         pdate = PDate.from_string(str(date_str))
    #         if pdate:
    #             date = pdate
    #         else:
    #             raise ValueError("Date not parsable: {date_str}")
    #         # attributes = section.get_attributes(section.text)
    #         cal.add(
    #             Day(
    #                 date,
    #                 # **attributes
    #             )
    #         )

    #     return cal

    def copy(self) -> "Calendar":
        cal = Calendar()
        cal.days = {k.copy(): v.copy() for k, v in self.days.items()}
        return cal

    def add(self, day: Day) -> None:
        self.days.update({day.date: day})

    @property
    def start_date(self) -> PDate:
        return min(self.days)

    @property
    def end_date(self) -> PDate:
        return max(self.days)

    def long_repr(self) -> str:
        spacer = tabularize(" ", thick=True) + "\n"
        # spacer += spacer
        return spacer.join(map(str, self.days.values()))

    def __getitem__(self, __date: PDate) -> Day:
        if not __date in self.days:
            self.days.update({__date: Day(__date)})
        return self.days[__date]

    def __setitem__(self, __name: PDate, __value: Any) -> None:
        ...

    def __str__(self) -> str:
        return "need to implement this"

    def __repr__(self) -> str:
        return self.__str__()
