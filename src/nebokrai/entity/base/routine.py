from typing import Any, Callable, Iterable, Optional, Union

from ...configuration import config
from ...util import NKDate, NKTime, tabularize
from ...util.serde.custom_dict_types import RoutineDictRaw
from ..container.entries import Entries
from .entry import Entry


class Routine:
    """
    Contains all information needed to add a routine to `Day`.
    """

    def __init__(
        self,
        name: str,
        start: NKTime,
        items: Iterable[Entry],
        priority: int,
        notes: str,
        normaltime: int,
        idealtime: int,
        mintime: int,
        maxtime: int,
        ismovable: bool,
        order: float,
        valid_dates: Union[Callable[[NKDate], bool], set[NKDate]] = lambda d: True,
    ) -> None:
        self.name = name
        self.start = start
        self.items = Entries(items)
        self.priority = int(priority)
        self.notes = notes
        self.normaltime = normaltime
        self.idealtime = idealtime
        self.mintime = mintime
        self.maxtime = maxtime
        self.ismovable = ismovable
        self.order = order

        def validator(d: NKDate) -> bool:
            ret: bool = (
                (d in valid_dates) if hasattr(valid_dates, "__contains__") else valid_dates(d)
            )
            return ret

        self.valid_dates = validator

    @classmethod
    def deserialize(cls, routine_dict: RoutineDictRaw) -> "Routine":
        """
        Creates instance from dict, intended to be used with .json declaration format.
        """
        items: list[Entry] = []
        for item_dict in routine_dict["items"]:
            items.append(Entry.deserialize(item_dict))

        return cls(
            routine_dict["name"],
            NKTime.from_string(routine_dict["default_start"]),
            items,
            priority=int(routine_dict["default_priority"]),
            notes=routine_dict.get("default_notes", ""),
            normaltime=int(routine_dict["default_normaltime"]),
            idealtime=int(routine_dict["default_idealtime"]),
            mintime=int(routine_dict["default_mintime"]),
            maxtime=int(routine_dict["default_maxtime"]),
            ismovable=bool(routine_dict.get("default_ismovable"))
            if "default_ismovable" in routine_dict
            else True,
            order=float(
                routine_dict["default_order"]
                if "default_order" in routine_dict
                else config.default_order
            ),
        )

    def valid_on(self, date: NKDate) -> bool:
        return self.valid_dates(date)

    def as_entry(
        self,
        start: NKTime,
        priority: Optional[float],
        normaltime: int,
        idealtime: int,
        mintime: int,
        maxtime: int,
        ismovable: bool,
        order: float,
    ) -> Entry:
        """
        Converts instance of Routine into an instance of Entry.
        """
        return Entry(
            self.name,
            start or self.start,
            priority=self.priority if priority is None else priority,
            normaltime=normaltime,
            idealtime=idealtime,
            mintime=mintime,
            maxtime=maxtime,
            ismovable=ismovable,
            order=order if order is not None else self.order,
        )

    def pretty(self) -> str:
        """
        Creates a detailed and aesthetic string representation of the given Routine instance.
        """

        def format_number(s: Any) -> str:
            return (len(str(s)) == 1) * " " + f"{s} │ "

        width = config.repr_width
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = (
            thickbeam
            + tabularize(f"{self.name}", width, thick=True)
            + "\n"
            + tabularize(f"  Priority: {self.priority}", width, thick=True)
            + thinbeam
        )
        return header + "\n".join(
            [
                tabularize(format_number(i) * (len(s.name) > 0) + s.name, width, thick=True)
                for i, s in enumerate(self.items, start=1)
            ]
        )

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()
