import re
from datetime import date
from typing import Any, Union


class PDate:
    """
    Bespoke date class designed to simplify the planager codebase.
    """

    date_regex: re.Pattern = re.compile(r"(\d{2,4})[^\d](\d\d?)[^\d](\d\d?)")

    def __init__(self, year: int, month: int, day: int) -> None:
        assert (year > 1969) and (month in range(1, 13)) and (day in range(1, 32))
        self._year = year
        self._month = month
        self._day = day
        self._date = date(year, month, day)

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
    def today(cls) -> "PDate":
        d = date.today()
        return cls(d.year, d.month, d.day)

    @classmethod
    def from_string(cls, date_str: str) -> "PDate":
        if not isinstance(date_str, str):
            raise TypeError(
                f"Invalid type for PDate.from_string: '{type(date_str)}' (value: '{date_str}')."
            )
        result = re.search(cls.date_regex, str(date_str))
        if result:
            year, month, day = map(int, result.groups())
            return cls(year, month, day)
        raise ValueError(f"Invalid string for conversion to PDate: '{date_str}'.")

    def toordinal(self) -> int:
        return self._date.toordinal()

    @classmethod
    def fromordinal(cls, __ord: int) -> "PDate":
        d = date.fromordinal(__ord)
        return cls(d.year, d.month, d.day)

    def weekday(self) -> int:
        return self._date.weekday()

    def daysto(self, date2: "PDate") -> int:
        return date2.toordinal() - self.toordinal()

    def __int__(self) -> int:
        return self.toordinal()

    def __add__(self, days: int) -> "PDate":
        d = date.fromordinal(self.toordinal() + int(days))
        return PDate(d.year, d.month, d.day)

    def __sub__(self, days: int) -> "PDate":  # type: ignore
        return PDate.fromordinal(self.toordinal() - int(days))

    def pretty(self) -> str:
        """
        Returns a the date written out in long form.
        """

        days = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        months = {
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
        ordinal_endings = {
            1: "st",
            2: "nd",
            3: "rd",
            21: "st",
            22: "nd",
            23: "rd",
            31: "st",
        }
        ending = ordinal_endings.get(self.day, "th")
        return f"{days[self.weekday()]}, {months[self.month]} {self.day}{ending}, {self.year}"

    def range(self, end: Union["PDate", int], inclusive: bool = True) -> list["PDate"]:
        """
        Returns a list of consecutive days, default inclusive. Supports reverse-order ranges.
        """
        inclusive = inclusive and (self != end) and (end != 0)

        date1 = self.copy()
        if isinstance(end, int):
            date2 = date1 + end
        else:
            date2 = end

        reverse: bool = False

        if date1 > date2:
            date1, date2 = date2, date1
            reverse = True

        if not inclusive:
            if not reverse:
                date2 -= 1
            else:
                date1 += 1

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

    def __hash__(self) -> int:
        return hash((self.year, self.month, self.day))

    def __eq__(self, __other: object) -> bool:
        if not isinstance(__other, (date, PDate)):
            return False
        return (self.year, self.month, self.day) == (
            __other.year,
            __other.month,
            __other.day,
        )

    def __lt__(self, __other: Any) -> bool:
        if isinstance(__other, NoneDate):
            return False
        return self.__int__() < int(__other)

    def __gt__(self, __other: Any) -> bool:
        if isinstance(__other, NoneDate):
            return False
        return self.__int__() > int(__other)

    def __le__(self, __other: Any) -> bool:
        if isinstance(__other, NoneDate):
            return False
        return self.__int__() <= int(__other)

    def __ge__(self, __other: Any) -> bool:
        if isinstance(__other, NoneDate):
            return False
        return self.__int__() >= int(__other)

    def __str__(self) -> str:
        return f"{self.year}-{self.month:0>2}-{self.day:0>2}"

    def __repr__(self) -> str:
        return f"PDate({self.__str__()})"


class NoneDate(PDate):
    """
    Empty date for cases where this may be superior to using None
    """

    def __init__(self) -> None:
        super().__init__(1970, 1, 1)

    def __bool__(self) -> bool:
        return False

    def __eq__(self, __other: object) -> bool:
        return isinstance(__other, NoneDate)

    def __lt__(self, __other: object) -> bool:
        return False

    def __gt__(self, __other: object) -> bool:
        return False

    def __le__(self, __other: object) -> bool:
        return False

    def __ge__(self, __other: object) -> bool:
        return False

    def __str__(self) -> str:
        return "NoneDate"

    def __repr__(self) -> str:
        return self.__str__()
