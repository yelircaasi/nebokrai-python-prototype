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
        routine_dict: dict[str, dict] = {
            "Morning Routine": {
                "default_start": PTime(5),
                "priority": 80,
                "normaltime": 60,
                "mintime": 15,
                "maxtime": 180,
            },
            "Midday Routine": {
                "default_start": PTime(13),
                "priority": 60,
                "normaltime": 30,
                "mintime": 10,
                "maxtime": 60,
            },
            "Evening Routine": {
                "default_start": PTime(21),
                "priority": 80,
                "normaltime": 60,
                "mintime": 15,
                "maxtime": 180,
            },
        },
        start: PTime = PTime(5),
        end: PTime = PTime(21),
    ) -> None:
        self.date = date
        self.entries = entries
        self.routine_dict = routine_dict

        # self.entries.insert(0, FIRST_ENTRY)
        # self.entries.append(LAST_ENTRY)
        waketime = min(start, self.entries.start)
        bedtime = max(end, self.entries.end)
        morning_normaltime = PTime(0).timeto(waketime)
        evening_normaltime = bedtime.timeto(PTime(24))
        morning_sleep = Entry(
            "Sleep",
            PTime(0),
            end=waketime,
            priority=70,
            normaltime=morning_normaltime,
            idealtime=morning_normaltime,
            mintime=morning_normaltime - 1,
            maxtime=morning_normaltime + 1,
            ismovable=False,
        )
        evening_sleep = Entry(
            "Sleep",
            bedtime,
            end=PTime(24),
            priority=70,
            normaltime=evening_normaltime,
            idealtime=evening_normaltime,
            mintime=evening_normaltime - 1,
            maxtime=evening_normaltime + 1,
            ismovable=False,
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
        return Day(self.date.copy(), self.entries.copy(), self.routine_dict.copy())

    # @classmethod
    # def default_day(cls, date: PDate) -> "Day":
    #     return cls(
    #         date
    #         entries: Entries = Entries(),
    #         routine_dict: list[str] = [
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

        routines_dict = {}
        for routine_dict in day_dict["routines"]:
            routines_dict.update(
                {routine_dict["name"].split("  ")[0].lower(): routine_dict}
            )

        start = PTime.from_string(day_dict.get("start", str(cls.DAY_START_DEFAULT)))
        end = PTime.from_string(day_dict.get("end", str(cls.DAY_END_DEFAULT)))

        # print(entries)
        # print('routines_dict:', routines_dict)

        return cls(date, entries, routines_dict, start=start, end=end)

    def add_routines(self, routines: Routines) -> None:
        for routine_name, routine_spec in self.routine_dict.items():
            # print(self.routine_dict)
            # print(routine_spec.get("start"))
            # print(self.entries[0].end)
            # print(PTime(5) - 15)
            # exit()
            # if routine_name == "midday":
            #     exit()
            routine_entry = routines[routine_name].as_entry(
                routine_name,
                start=PTime.ensure_is_ptime(
                    routine_spec.get("start") or routines[routine_name].start
                ),
                priority=int(
                    routine_spec.get("priority") or routines[routine_name].priority
                ),
                normaltime=int(
                    routine_spec.get("normaltime") or routines[routine_name].normaltime
                ),
                idealtime=int(
                    routine_spec.get("normaltime") or routines[routine_name].idealtime
                ),
                mintime=int(
                    routine_spec.get("mintime") or routines[routine_name].mintime
                ),
                maxtime=int(
                    routine_spec.get("maxtime") or routines[routine_name].maxtime
                ),
            )

            self.entries.append(routine_entry)
            self.entries.sort()

    @property
    def blocks(self) -> set[str]:
        blocks = set()
        for entry in self.entries:
            blocks.update(entry.blocks)
        return blocks

    @property
    def empty_time(self) -> int:
        # for e in self.entries:
        #     print(e.name, e.duration)
        # return int(1440 - sum(map(lambda e: e.duration * (e.priority > 0), self.entries)))
        return int(1440 - sum(map(lambda e: e.duration, self.entries)))

    @property
    def total_available(self) -> int:
        return int(1440 - sum(map(lambda e: e.unavailable, self.entries)))

    def available_for_block(self, block: str) -> int:
        return sum(
            map(
                lambda ent: ent.available,
                filter(lambda e: block in e.blocks, self.entries),
            )
        )

    @property
    def available_dict(self) -> dict[str, int]:
        time_dict: dict[str, int] = {}
        time_dict.update({"empty": self.empty_time})
        time_dict.update({"total": self.total_available})
        for block in self.blocks:
            time_dict.update({block: self.available_for_block(block)})
        return time_dict

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
            + tabularize(", ".join(self.routine_dict), width, thick=True)
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

    def add_routines(self, routines: Routines) -> None:
        for day in self.days.values():
            day.add_routines(routines)

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
