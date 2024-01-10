from typing import Any, Iterable, Iterator, Union

from ...configuration import config
from ...util import NKDate, tabularize
from ...util.nkdatetime.nktime import NKTime
from ...util.serde.custom_dict_types import (
    CalendarDictRaw,
    DayDictRaw,
    RoutinesInCalendarDictRaw,
)
from ..container.entries import Entries
from ..container.routines import Routines
from .entry import Entry


class Day:
    """
    Designed as a component of `Calendar`. To be used as an input to scheduling,
      containing most importantly the max load, routines, and the 'big rock' entries
      planned in advance, around which other entries are to be automatically be scheduled.
    """

    def __init__(
        self,
        date: NKDate,
        start: NKTime,
        end: NKTime,
        entries: Entries,
        routines: Entries,
    ) -> None:
        self.date = date
        self.entries = entries
        self.routines = routines
        self.start = start
        self.end = end

        waketime = min(start, self.entries.start, self.routines.start)
        bedtime = max(
            min(end, self.routines.end),
            self.entries.end,
        )
        morning_normaltime = NKTime(0).timeto(waketime)
        evening_normaltime = bedtime.timeto(NKTime(24))
        morning_sleep = Entry(
            "Sleep",
            NKTime(0),
            end=waketime,
            priority=config.default_sleep_priority,
            normaltime=morning_normaltime,
            idealtime=morning_normaltime,
            mintime=morning_normaltime - config.default_sleep_delta_min,
            maxtime=morning_normaltime + config.default_sleep_delta_max,
            ismovable=False,
        )
        evening_sleep = Entry(
            "Sleep",
            bedtime,
            end=NKTime(24),
            priority=config.default_sleep_priority,
            normaltime=evening_normaltime,
            idealtime=evening_normaltime,
            mintime=evening_normaltime - config.default_sleep_delta_min,
            maxtime=evening_normaltime + config.default_sleep_delta_max,
            ismovable=False,
        )
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
                raise ValueError("Day init: last_entry:", last_entry)
            else:
                self.entries.append(evening_sleep)

        else:
            self.entries.append(morning_sleep)
            self.entries.append(evening_sleep)

        self.entries.extend(routines)
        self.entries.sort()

    def copy(self) -> "Day":
        return Day(
            self.date.copy(),
            self.start.copy(),
            self.end.copy(),
            self.entries.copy(),
            self.routines.copy(),
        )

    @classmethod
    def deserialize(cls, routines: Routines, date: NKDate, day_dict: DayDictRaw) -> "Day":
        """
        Instantiates from config, json-derived dic, and project information.
        """

        entries = Entries()
        for entry_dict in day_dict["entries"]:
            # entry_dict = parse_entry_dict(_entry_dict)
            entries.append(Entry.deserialize(entry_dict))

        routines_dict = {}
        for routine_dict in day_dict["routines"]:
            routines_dict.update({routine_dict["name"].split("  ")[0].lower(): routine_dict})
        routine_entries = cls.make_routine_entries(routines_dict, routines)

        start = NKTime.from_string(day_dict.get("start", str(config.default_day_start)))
        end = NKTime.from_string(day_dict.get("end", str(config.default_day_end)))

        return cls(date, start, end, entries, routine_entries)

    @staticmethod
    def make_routine_entries(
        routines_dict: RoutinesInCalendarDictRaw, routines: Routines
    ) -> Entries:
        """
        Creates routine entries from the declaration and from the Routines instance.
        """

        entries = Entries()

        for routine_spec in routines_dict.values():
            routine_name = routine_spec["name"]

            routine_entry = routines[routine_name].as_entry(
                start=NKTime.from_string(
                    routine_spec.get("start") or str(routines[routine_name].start)
                ),
                priority=int(routine_spec.get("priority") or routines[routine_name].priority),
                normaltime=int(routine_spec.get("normaltime") or routines[routine_name].normaltime),
                idealtime=int(routine_spec.get("idealtime") or routines[routine_name].idealtime),
                mintime=int(routine_spec.get("mintime") or routines[routine_name].mintime),
                maxtime=int(routine_spec.get("maxtime") or routines[routine_name].maxtime),
                ismovable=bool(
                    routine_spec.get("ismovable")
                    if routine_spec.get("ismovable") is not None
                    else routines[routine_name].ismovable
                ),
                order=float(
                    routine_spec["order"]
                    if "order" in routine_spec
                    else routines[routine_name].order
                ),
            )

            entries.append(routine_entry)

        return entries

    @property
    def routine_names(self) -> list[str]:
        return [rout.name.split(" ")[0] for rout in self.routines]

    @property
    def blocks(self) -> set[str]:
        """
        Property returning the set of all blocks contained by the consituent entries of the day.
        """
        blocks = set()
        for entry in self.entries:
            blocks.update(entry.blocks)
        return blocks

    @property
    def empty_time(self) -> int:
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
        """
        Returns a dictionary containing available time by block, for unspecified categories
          (i.e. empty time), and total time available.
        """
        time_dict: dict[str, int] = {}
        time_dict.update({"empty": self.empty_time})
        time_dict.update({"total": self.total_available})
        for block in self.blocks:
            time_dict.update({block: self.available_for_block(block)})
        return time_dict

    @property
    def repr1(self) -> str:
        return f""

    def __str__(self) -> str:
        width = config.repr_width
        header_thickbeam = "┣━━━━━━━━━━━━━┯" + (width - 16) * "━" + "┫\n"
        header_thinbeam = "\n┠─────────────┴" + (width - 16) * "─" + "┨\n"
        bottombeam = "\n┣" + (width - 2) * "━" + "┫\n"
        header = (
            header_thickbeam
            + tabularize(str(self.date) + "  │", width, thick=True)
            + header_thinbeam
            + tabularize("Routines: " + ", ".join(self.routine_names), width, thick=True)
            # + "XXX"
            + "\n"
        )

        return header + "\n".join(map(str, self.entries)) + bottombeam


class Calendar:
    """
    Container for all days, with a few helper methods.
    """

    def __init__(self, days: Union[dict[NKDate, Day], Iterable[Day]]) -> None:
        self.days: dict[NKDate, Day] = days if isinstance(days, dict) else {d.date: d for d in days}

    @classmethod
    def deserialize(cls, routines: Routines, calendar_dict: CalendarDictRaw) -> "Calendar":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        days = {}
        for date_string, day_dict in calendar_dict.items():
            day_date = NKDate.from_string(date_string)
            day = Day.deserialize(routines, day_date, day_dict)
            days.update({day_date: day})

        return cls(days)

    def copy(self) -> "Calendar":
        cal = Calendar({})
        cal.days = {k.copy(): v.copy() for k, v in self.days.items()}
        return cal

    def add(self, day: Day) -> None:
        self.days.update({day.date: day})

    @property
    def start_date(self) -> NKDate:
        return min(self.days)

    @property
    def end_date(self) -> NKDate:
        return max(self.days)

    def long_repr(self) -> str:
        spacer = tabularize(" ", config.repr_width, thick=True) + "\n"
        return spacer.join(map(str, self.days.values()))

    def __getitem__(self, __date: NKDate) -> Day:
        return self.days[__date]

    def __setitem__(self, __name: NKDate, __value: Any) -> None:
        ...

    def __iter__(self) -> Iterator[NKDate]:
        return iter(self.days.keys())

    @property
    def summary(self) -> str:
        return "Calendar.summary property is not yet implemented."

    def __str__(self) -> str:
        return "need to implement this"

    def __repr__(self) -> str:
        return self.__str__()
