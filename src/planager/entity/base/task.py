from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union

from ...util import ConfigType, Norg, PDate, PTime, tabularize
from .entry import Entry


class Task:
    tmpdate: PDate = PDate.nonedate()

    def __init__(
        self,
        name: str,
        task_id: Tuple[str, str, str],
        priority: int = 10,
        project_name: str = "?",
        after: Set[Tuple[str, str, str]] = set()
        
    ) -> None:
        assert len(task_id) == 3

        self.name = name
        self.task_id = task_id
        self.priority = priority
        self.project_name = project_name
        self.dependencies = after

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
            f"Task: {self.project_name[:30]} :: {self.name} (ID {'::'.join(self.task_id)})",
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
    
    def __eq__(self, __other: Any) -> bool:
        return self.__dict__ == __other.__dict__
    
    def __lt__(self, __other: Any) -> bool:
        return (self.task_id in __other.dependencies) and (__other.task_id not in self.dependencies) or (__other.tmpdate > self.tmpdate)
    
    def __gt__(self, __other: Any) -> bool:
        return (__other.task_id in self.dependencies) and (self.task_id not in __other.dependencies) or (self.tmpdate > __other.tmpdate)
    
    def __le__(self, __other: Any) -> bool:
        return (not self.task_id not in __other.dependencies) and (__other.task_id not in self.dependencies) and (__other.tmpdate >= self.tmpdate)
    
    def __ge__(self, __other: Any) -> bool:
        return (__other.task_id not in self.dependencies) and (self.task_id not in __other.dependencies) and (self.tmpdate >= __other.tmpdate)

    def isafter(self, __other: "Task") -> bool:
        return self.task_id in __other.dependencies
'''
t1 = Task("Task1", ("a", "b", "c"), after={("a", "b", "d")})
t2 = Task("Task2", ("a", "b", "d"))
t3 = Task("Task3", ("a", "b", "e"), after={("a", "b", "c")})
sorted((t1, t2, t3))
'''
