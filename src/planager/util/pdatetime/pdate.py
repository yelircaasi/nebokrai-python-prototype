import re
from datetime import date, datetime
from typing import Any, List, Optional, Tuple, Union


class PDate(date):
    date_regex: re.Pattern = re.compile(r"(\d{2,4})[^\d](\d\d?)[^\d](\d\d?)")

    def __init__(self, year: int, month: int, day: int) -> None:
        self._year = year
        self._month = month
        self._day = day

    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, year: int) -> None:
        self._year = year

    @property
    def month(self) -> int:
        return self._month

    @month.setter
    def month(self, month: int) -> None:
        self._month = month

    @property
    def day(self) -> int:
        return self._day

    @day.setter
    def day(self, day: int) -> None:
        self._day = day

    def copy(self):
        return PDate(self.year, self.month, self.day)

    @classmethod
    def from_string(cls, date_str: str) -> Optional["PDate"]:
        result = re.search(cls.date_regex, date_str)
        if result:
            year, month, day = map(int, result.groups())
            return cls(year, month, day)
        else:
            return None

    def __int__(self) -> int:
        return self.toordinal()

    def __add__(self, days: Any) -> "PDate":
        return PDate.fromordinal(self.toordinal() + int(days))

    def __sub__(self, days: Any) -> "PDate":  # type: ignore
        return PDate.fromordinal(self.toordinal() - int(days))

    def pretty(self):
        DAYS = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        MONTHS = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        ORDINAL_ENDINGS = {
            1: "st",
            2: "nd",
            3: "rd",
            21: "st",
            22: "nd",
            23: "rd",
            31: "st",
        }
        ending = ORDINAL_ENDINGS.get(self.day, "th")
        return f"{DAYS[self.weekday()]}, {MONTHS[self.month]} {self.day}{ending}, {self.year}"

    @classmethod
    def ensure_is_pdate(
        cls,
        candidate: Any,
        default: Optional["PDate"] = None,
    ) -> Union["PDate", None]:
        if not candidate:
            return default if default else None
        if isinstance(candidate, PDate):
            return candidate
        elif isinstance(candidate, str):
            if not candidate.strip():
                return default if default else None
            try:
                return PDate.fromisoformat(candidate)
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{candidate}'")
        elif isinstance(candidate, tuple):
            try:
                return PDate(*map(int, candidate))
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{str(candidate)}'")
        elif isinstance(candidate, int):
            try:
                return PDate.today() + candidate
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{str(candidate)}'")
        else:
            raise ValueError(
                f"Invalid input type for `PDate` class: '{type(candidate)}' (value: '{candidate}')"
            )
        return None

    def range(self, date2: "PDate", inclusive: bool = True) -> List["PDate"]:
        date1 = self.copy()
        reverse: bool = False

        if date1 > date2:
            date1, date2 = date2, date1
            reverse = True

        if not inclusive:
            date2 -= 1

        date_i = date1
        dates = [date_i]

        while date_i < date2:
            dates.append(date_i := date_i + 1)

        if reverse:
            dates.reverse()

        return dates

    @classmethod
    def tomorrow(cls) -> "PDate":
        return cls.today() + 1
    
    @staticmethod
    def nonedate() -> "NoneDate":
        return NoneDate()

    def __eq__(self, __other: Any) -> bool:
        return self.__int__ == int(__other)
    
    def __lt__(self, __other: Any) -> bool:
        return self.__int__ < int(__other)
    
    def __gt__(self, __other: Any) -> bool:
        return self.__int__ > int(__other)
    
    def __le__(self, __other: Any) -> bool:
        return self.__int__ <= int(__other)
    
    def __ge__(self, __other: Any) -> bool:
        return self.__int__ >= int(__other)


class NoneDate:
    def __eq__(self, __other: Any) -> bool:
        return self.__dict__ == __other.__dict__
    
    def __lt__(self, __other: Any) -> bool:
        return False
    
    def __gt__(self, __other: Any) -> bool:
        return False
    
    def __le__(self, __other: Any) -> bool:
        return True
    
    def __ge__(self, __other: Any) -> bool:
        return True
