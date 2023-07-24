import re
from datetime import date, datetime
from typing import Any, List, Optional, Tuple, Union


class PTime:
    def __init__(self, hour: int = 0, minute: int = 0, isblank: bool = False):
        if not (60 * hour + minute) in range(1441):
            raise ValueError("Time must be within 00:00..24:00")
        self.hour = hour
        self.minute = minute
        self.isblank = isblank

    @classmethod
    def from_string(cls, date_string: Optional[str]) -> "PTime":
        if not date_string:
            res = cls()
            res.isblank = True
            return res
        hour, minute = map(int, date_string.split(":"))
        return cls(hour, minute)

    @classmethod
    def ensure_is_ptime(
        cls,
        candidate: Any,
        default: Optional["PTime"] = None,
    ) -> Union["PTime", None]:
        if not candidate:
            return default if default else None
        if isinstance(candidate, PTime):
            return candidate
        elif isinstance(candidate, str):
            if not candidate.strip():
                return default if default else None
            try:
                return PTime.fromisoformat(candidate)
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{candidate}'")
        elif isinstance(candidate, tuple):
            try:
                hour, minute = map(int, candidate)
                return PTime(hour, minute)
            except:
                raise ValueError(f"Invalid input for `PTime` class: '{str(candidate)}'")
        elif isinstance(candidate, int):
            try:
                candidate = PTime(candidate)
            except:
                raise ValueError(f"Invalid input for `PTime` class: '{str(candidate)}'")
        else:
            raise ValueError(
                f"Invalid input type for `PTime` class: '{type(candidate)}' (value: '{candidate}')"
            )
        return None

    def __bool__(self):
        return not self.isblank

    def copy(self):
        return PTime(self.hour, self.minute)

    def tominutes(self) -> int:
        return 60 * self.hour + self.minute

    def timeto(self, time2: "PTime") -> int:
        return time2.tominutes() - self.tominutes()

    def timefrom(self, time2: "PTime") -> int:
        return self.tominutes() - time2.tominutes()

    @classmethod
    def fromminutes(cls, mins: int) -> "PTime":
        return cls(*divmod(mins, 60))

    def __add__(self, mins: int) -> "PTime":
        return PTime.fromminutes(min(1440, max(0, self.tominutes() + mins)))

    def __sub__(self, mins: int) -> "PTime":
        return PTime.fromminutes(min(1440, max(0, self.tominutes() - mins)))

    def __str__(self) -> str:
        return f"{self.hour:0>2}:{self.minute:0>2}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, ptime2: Any) -> bool:  # type: ignore
        if isinstance(ptime2, PTime):
            return self.tominutes() == ptime2.tominutes()
        return False

    def __lt__(self, ptime2: "PTime") -> bool:
        return self.tominutes() < ptime2.tominutes()

    def __gt__(self, ptime2: "PTime") -> bool:
        return self.tominutes() > ptime2.tominutes()

    def __le__(self, ptime2: "PTime") -> bool:
        return self.tominutes() <= ptime2.tominutes()

    def __ge__(self, ptime2: "PTime") -> bool:
        return self.tominutes() >= ptime2.tominutes()

    @classmethod
    def fromisoformat(cls, __str: str) -> "PTime":
        hour, minute = map(int, __str.split(":"))
        return cls(hour, minute)
