from typing import Any

from planager.utils.datetime_extensions import PDate


class Calendar:
    def __init__(self, date0: PDate = PDate.today()) -> None:
        self.date0 = date0

    def __getitem__(self, __name: str) -> Any:
        item = ...
        return item
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...
