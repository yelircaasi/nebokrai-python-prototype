from pathlib import Path
from typing import Any, Dict, Union

from planager.entities import Roadmaps
from planager.utils.data.norg.norg_utils import Norg
from planager.utils.misc import tabularize


class Routine:
    def __init__(
        self,
        name: str,
        attributes: dict,
        items: list,
    ) -> None:
        self.name = name
        self.items = items
        if attributes:
            self.__dict__.update(attributes)
        if not attributes.get("priority"):
            self.priority = 80
        if not attributes.get("notes"):
            self.notes = ""

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


class Routines:
    """
    Container class for routines, designed to be

    """

    def __init__(self) -> None:
        self.routines = []

    def add(self, routine: Routine) -> None:
        self.routines.append(routine)

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
            + "\n".join(map(str, self.routines))
            + bottombeam
        )

    def __getitem__(self, __name: str) -> Routine:
        routine = ...
        return routine

    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    @classmethod
    def from_norg_workspace(cls, workspace_root: Path) -> "Routines":
        routines = cls()
        return routines

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "Roadmaps":
        file = workspace_dir / "routines.norg"
        parsed = Norg.from_path(file)
        routines = Routines()
        for section in parsed.sections:
            title = section["title"]
            attributes = Norg.parse_preasterix_attributes(section["text"])
            # items = list(map(lambda x: x if isinstance(x, str) else x["title"], Norg.parse_subsections(section)))
            items = section["subsections"]
            routines.add(
                Routine(
                    section["title"],
                    attributes,
                    items,
                )
            )
        return routines
