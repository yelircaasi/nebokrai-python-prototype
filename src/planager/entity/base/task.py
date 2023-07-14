from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from ...util import ConfigType, Norg, PDate, PTime, tabularize
from .entry import Entry


class Task:
    def __init__(
        self,
        name: str,
        task_id: Tuple[str, str, str],
        priority: int = 10,
        project_name: str = "?",
        # **kwargs,
    ) -> None:
        assert len(task_id) == 3

        self.name = name
        self.task_id = task_id
        self.priority = priority
        self.project_name = project_name
        # self.__dict__.update(**kwargs)

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        thinbeam = "┠" + (width - 2) * "─" + "┨"
        format_number = lambda s: (len(str(s)) == 1) * " " + f" {s} │ "
        top = tabularize(
            f"Task: {self.project_name[:30]} :: {self.name} (ID {self.task_id})",
            width,
            pad=1,
        )
        empty = tabularize("", width)
        priority = tabularize(f"  Priority: {self.priority}", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, thinbeam, empty, ""))
            + priority
            + "\n"
            + empty
            + bottombeam
        )

    def as_entry(self, start: Optional[PTime]) -> Entry:
        # TODO
        return Entry(self.name, start)
