from typing import Any, Optional


class PTime:
    """
    Bespoke time class designed to simplify the nebokrai codebase.
    """

    def __init__(self, hour: int = 0, minute: int = 0, isblank: bool = False):
        if not ((hour >= 0) and (minute >= 0) and (60 * hour + minute) in range(1441)):
            raise ValueError("Time must be within 00:00..24:00")
        self.hour = hour
        self.minute = minute
        self.isblank = isblank

    @classmethod
    def from_string(cls, date_string: Optional[str]) -> "PTime":
        assert isinstance(
            date_string, str
        ), f"Argument to PTime.from_string must be str, not '{type(date_string)}'."
        if date_string.lower().startswith("none"):
            return PTime.nonetime()
        substrings = date_string.split(":")
        assert (
            len(substrings) == 2
        ), f"Argument to PTime.from_string must have exactly one colon. Given: '{date_string}'."
        hour, minute = map(int, substrings)
        return cls(hour, minute)

    def __bool__(self):
        return not self.isblank

    def copy(self):
        return PTime(self.hour, self.minute)

    def tominutes(self) -> int:
        return 60 * self.hour + self.minute

    @classmethod
    def fromminutes(cls, mins: int) -> "PTime":
        return cls(*divmod(mins, 60))

    @staticmethod
    def nonetime() -> "NoneTime":
        return NoneTime()

    def timeto(self, time2: "PTime") -> int:
        t2, t1 = time2.tominutes(), self.tominutes()
        return t2 - t1

    def timefrom(self, time2: "PTime") -> int:
        t2, t1 = self.tominutes(), time2.tominutes()
        return t2 - t1

    def __add__(self, mins: int) -> "PTime":
        return PTime.fromminutes(min(1440, max(0, self.tominutes() + mins)))

    def __sub__(self, mins: int) -> "PTime":
        return PTime.fromminutes(min(1440, max(0, self.tominutes() - mins)))

    def __str__(self) -> str:
        return f"{self.hour:0>2}:{self.minute:0>2}"

    def __repr__(self) -> str:
        return f"PTime({self.__str__()})"

    def __eq__(self, ptime2: Any) -> bool:
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


class NoneTime(PTime):
    """
    Empty time for cases where this may be superior to using None
    """

    def __init__(self) -> None:
        super().__init__()

    def __bool__(self) -> bool:
        return False

    def __add__(self, _: Any) -> "NoneTime":
        return NoneTime()

    def __sub__(self, _: Any) -> "NoneTime":
        return NoneTime()

    def __eq__(self, __other: Any) -> bool:
        return isinstance(__other, NoneTime)

    def __lt__(self, __other: Any) -> bool:
        return False

    def __gt__(self, __other: Any) -> bool:
        return False

    def __le__(self, __other: Any) -> bool:
        return False

    def __ge__(self, __other: Any) -> bool:
        return False

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "XX:XX"
