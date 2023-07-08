from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

from planager.utils.data.norg.norg_utils import Norg
from planager.utils.datetime_extensions import PDate, PTime
from planager.utils.misc import round5, tabularize

from .entry import Entry
from .roadmap import Roadmaps
from .task import Task


class Routine:
    def __init__(
        self,
        name: str,
        routine_num: int,
        attributes: dict,
        items: list,
    ) -> None:
        self.name = name
        self.items = items
        self.id = (-1, 0, routine_num)
        
        if attributes:
            self.__dict__.update(attributes)
        self.priority = attributes.get("priority") or 80
        self.priority = int(self.priority)
        self.notes = attributes.get("notes") or ""
        self.normaltime = attributes.get("normaltime", 60)
        self.mintime = attributes.get("mintime", round5(self.normaltime / 4))
        self.mintime = attributes.get("mintime", round5(self.normaltime * 2))


    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        thickbeam = "┣" + (width - 2) * "━" + "┫\n"
        thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        header = (
            thickbeam
            + tabularize(f"{self.name}", width)
            + "\n"
            + tabularize(f"  Priority: {self.priority}", width)
            + thinbeam
        )
        format_number = lambda s: (len(str(s)) == 1) * " " + f"{s} │ "
        return header + "\n".join(
            [
                tabularize(format_number(i) * (len(s) > 0) + s, width, pad=1)
                for i, s in enumerate((self.items + [""]), start=1)
            ]
        )

    def valid_on(self, date: PDate) -> bool:
        # TODO
        return True

    def as_entry(self, start: Optional[PTime]) -> Entry:
        return Entry(self.name, start, priority=self.priority)  # TODO

    def as_task(self) -> Task:
        return Task(self.name, self.id, priority=self.priority)  # TODO


class Routines:
    """
    Container class for routines, designed to be

    """

    def __init__(self) -> None:
        self._routines: List[Routine] = []

    def __iter__(self) -> Iterator[Routine]:
        return iter(self._routines)

    def add(self, routine: Routine) -> None:
        self._routines.append(routine)

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        top = tabularize("Routines", width, pad=1)
        empty = tabularize("", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, ""))
            + "\n".join(map(str, self._routines))
            + bottombeam
        )

    def __getitem__(self, __name: str) -> Routine: 
        return list(filter(lambda x: x.name == __name, self._routines))[0]

    # def __setitem__(self, __name: str, __value: Any) -> None:
    #     ...

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Routines":
        file = workspace_dir / "routines.norg"
        parsed = Norg.from_path(file)
        routines = Routines()
        for i, section in enumerate(parsed.sections):
            title = section["title"]
            # attributes = Norg.parse_preasterix_attributes(section["text"])
            attributes = section["attributes"]
            # items = list(map(lambda x: x if isinstance(x, str) else x["title"], Norg.parse_subsections(section)))
            items = section["subsections"]
            routines.add(
                Routine(
                    title,
                    i,
                    attributes,
                    items,
                )
            )
        for routine in routines:
            print(routine.priority)
        return routines
