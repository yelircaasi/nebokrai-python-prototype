import re
from datetime import date, datetime
from typing import Any, List, Optional, Tuple, Union

# from ..type import Any, PTimeInputType
from .pdate import PDate
from .ptime import PTime


class PDateTime:
    nondigit_regex: re.Pattern = re.compile(r"[^\d]")

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int = 0,
        second: int = 0,
        isblank=False,
    ):
        if not (60 * hour + minute + int(bool(second))) in range(1441):
            raise ValueError("Time must be within 00:00..24:00")
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.isblank = isblank

        self.date = PDate(year, month, day)
        self.time = PTime(self.hour, self.minute)

    @classmethod
    def now_str(cls) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def now(cls) -> "PDateTime":
        n = datetime.now()
        return cls(n.year, n.month, n.day, n.hour, n.minute, n.second)

    @classmethod
    def from_string(cls, date_string: str) -> "PDateTime":
        if not date_string:
            return cls(2023, 1, 1, 0, 0, 0)
        year, month, day, hour, minute, second = map(
            int, re.split(cls.nondigit_regex, date_string.strip())
        )
        # print(year, month, day, hour, minute, second)
        return cls(year, month, day, hour, minute, second)

    def __bool__(self):
        return not self.isblank

    def copy(self):
        return PTime(self.hour, self.minute)

    def tominutes(self) -> int:
        return 60 * self.hour + self.minute

    def toseconds(self) -> int:
        return 3600 * self.hour + 60 * self.minute + self.second

    def timeto(self, time2: "PTime") -> int:
        return time2.tominutes() - self.tominutes()

    def timefrom(self, time2: "PTime") -> int:
        return self.tominutes() - time2.tominutes()

    # @classmethod
    # def fromminutes(cls, mins: int) -> "PDateTime":
    #     return #cls(*divmod(mins, 60))

    # def __add__(self, mins: int) -> "PDateTime":
    #     #return PTime.fromminutes(min(1440, max(0, self.tominutes() + mins)))
    #     raise NotImplementedError

    # def __sub__(self, mins: int) -> "PDateTime":
    #     #return PTime.fromminutes(min(1440, max(0, self.tominutes() - mins)))
    #     raise NotImplementedError

    def __str__(self) -> str:
        # return f"{self.year}-{self.month:0>2}-{self.day:0>2} {self.hour:0>2}:{self.minute:0>2}:{self.second:0>2}"
        return f"{self.year}-{self.month:0>2}-{self.day:0>2} {self.hour:0>2}:{self.minute:0>2}:{self.second:0>2}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, pdt2: "PDateTime") -> bool:  # type: ignore
        return (self.date == pdt2.date) and (self.toseconds() == pdt2.toseconds())

    def __lt__(self, pdt2: "PDateTime") -> bool:
        return (self.date < pdt2.date) or (
            (self.date == pdt2.date) and (self.toseconds() < pdt2.toseconds())
        )

    def __gt__(self, pdt2: "PDateTime") -> bool:
        return (self.date > pdt2.date) or (
            (self.date == pdt2.date) and (self.toseconds() > pdt2.toseconds())
        )

    def __le__(self, pdt2: "PDateTime") -> bool:
        return (self.date < pdt2.date) or (
            (self.date == pdt2.date) and (self.toseconds() <= pdt2.toseconds())
        )

    def __ge__(self, pdt2: "PDateTime") -> bool:
        return (self.date > pdt2.date) or (
            (self.date == pdt2.date) and (self.toseconds() >= pdt2.toseconds())
        )
