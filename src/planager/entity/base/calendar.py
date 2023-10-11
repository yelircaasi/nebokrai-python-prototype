from typing import Any, Iterable, Iterator, Union

from ...config import Config
from ...util import PDate, tabularize
from ...util.pdatetime.ptime import PTime
from ..container.entries import Entries
from ..container.routines import Routines
from .entry import Entry


class Day:
    """
    Designed as a component of `Calendar`. To be used as an input to scheduling,
      contining most importantly the max load, routines, and the 'big rock' entries
      planned in advance, around which other entries are to be automatically be scheduled.
    """

    def __init__(
        self,
        config: Config,
        date: PDate,
        start: PTime,
        end: PTime,
        entries: Entries,
        routines: Entries,
    ) -> None:
        self.config = config
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
        morning_normaltime = PTime(0).timeto(waketime)
        evening_normaltime = bedtime.timeto(PTime(24))
        morning_sleep = Entry(
            config,
            "Sleep",
            PTime(0),
            end=waketime,
            priority=config.default_sleep_priority,
            normaltime=morning_normaltime,
            idealtime=morning_normaltime,
            mintime=morning_normaltime - config.default_sleep_delta_min,
            maxtime=morning_normaltime + config.default_sleep_delta_max,
            ismovable=False,
        )
        evening_sleep = Entry(
            config,
            "Sleep",
            bedtime,
            end=PTime(24),
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
            self.config,
            self.date.copy(),
            self.start.copy(),
            self.end.copy(),
            self.entries.copy(),
            self.routines.copy(),
        )

    @classmethod
    def from_dict(
        cls, config: Config, routines: Routines, date: PDate, day_dict: dict[str, Any]
    ) -> "Day":
        """
        Instantiates from config, json-derived dic, and project information.
        """

        entries = Entries(config)
        for entry_dict in day_dict["entries"]:
            entries.append(Entry.from_dict(config, entry_dict))

        routines_dict = {}
        for routine_dict in day_dict["routines"]:
            routines_dict.update({routine_dict["name"].split("  ")[0].lower(): routine_dict})
        routine_entries = cls.make_routine_entries(routines_dict, routines)

        start = PTime.from_string(day_dict.get("start", str(config.default_day_start)))
        end = PTime.from_string(day_dict.get("end", str(config.default_day_end)))

        return cls(config, date, start, end, entries, routine_entries)

    @staticmethod
    def make_routine_entries(routine_dict: dict[str, dict], routines: Routines) -> Entries:
        """
        Creates routine entries from the declaration and from the Routines instance.
        """

        entries = Entries(routines.config)

        for routine_spec in routine_dict.values():
            routine_name = routine_spec["name"]

            routine_entry = routines[routine_name].as_entry(
                start=PTime.ensure_is_ptime(
                    routine_spec.get("start") or routines[routine_name].start
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

    def __str__(self) -> str:
        width = self.config.repr_width
        # thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        header_thickbeam = "┣━━━━━━━━━━━━━┯" + (width - 16) * "━" + "┫\n"
        header_thinbeam = "\n┠─────────────┴" + (width - 16) * "─" + "┨\n"
        # thinbeam = "\n┠" + +(width - 2) * "─" + "┨\n"
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

    def __init__(self, config: Config, days: Union[dict[PDate, Day], Iterable[Day]]) -> None:
        self.config = config
        self.days: dict[PDate, Day] = days if isinstance(days, dict) else {d.date: d for d in days}

    @classmethod
    def from_dict(
        cls, config: Config, routines: Routines, calendar_dict: dict[str, Any]
    ) -> "Calendar":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        days = {}
        for date_string, day_dict in calendar_dict["days"].items():
            day_date = PDate.from_string(date_string)
            day = Day.from_dict(config, routines, day_date, day_dict)
            days.update({day_date: day})

        return cls(config, days)

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
        cal = Calendar(self.config, {})
        cal.days = {k.copy(): v.copy() for k, v in self.days.items()}
        return cal

    def add(self, day: Day) -> None:
        self.days.update({day.date: day})

    # def add_routines(self, routines: Routines) -> None:
    #     for day in self.days.values():
    #         day.add_routines(routines)

    @property
    def start_date(self) -> PDate:
        return min(self.days)

    @property
    def end_date(self) -> PDate:
        return max(self.days)

    def long_repr(self) -> str:
        spacer = tabularize(" ", self.config.repr_width, thick=True) + "\n"
        return spacer.join(map(str, self.days.values()))

    def __getitem__(self, __date: PDate) -> Day:
        return self.days[__date]

    def __setitem__(self, __name: PDate, __value: Any) -> None:
        ...

    def __iter__(self) -> Iterator[PDate]:
        return iter(self.days.keys())

    def __str__(self) -> str:
        return "need to implement this"

    def __repr__(self) -> str:
        return self.__str__()
