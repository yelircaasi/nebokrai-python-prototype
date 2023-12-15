from typing import Any, Optional


class NKTime:
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
    def from_string(cls, time_string: Optional[str]) -> "NKTime":
        if not isinstance(time_string, str):
            raise ValueError(
                f"Argument to NKTime.from_string must be str, not '{type(time_string)}'."
            )
        if time_string.lower().startswith("none"):
            return NKTime.nonetime()
        substrings = time_string.split(":")
        if not len(substrings) == 2:
            raise ValueError(
                "Argument to NKTime.from_string must have exactly one colon."
                f" Given: '{time_string}'."
            )
        hour, minute = map(int, substrings)
        return cls(hour, minute)

    def __bool__(self):
        return not self.isblank

    def copy(self):
        return NKTime(self.hour, self.minute)

    def tominutes(self) -> int:
        return 60 * self.hour + self.minute

    @classmethod
    def fromminutes(cls, mins: int) -> "NKTime":
        return cls(*divmod(mins, 60))

    @staticmethod
    def nonetime() -> "NoneTime":
        return NoneTime()

    def timeto(self, time2: "NKTime") -> int:
        t2, t1 = time2.tominutes(), self.tominutes()
        return t2 - t1

    def timefrom(self, time2: "NKTime") -> int:
        t2, t1 = self.tominutes(), time2.tominutes()
        return t2 - t1

    def __add__(self, mins: int) -> "NKTime":
        return NKTime.fromminutes(min(1440, max(0, self.tominutes() + mins)))

    def __sub__(self, mins: int) -> "NKTime":
        return NKTime.fromminutes(min(1440, max(0, self.tominutes() - mins)))

    def __str__(self) -> str:
        return f"{self.hour:0>2}:{self.minute:0>2}"

    def __repr__(self) -> str:
        return f"NKTime({self.__str__()})"

    def __eq__(self, nktime2: Any) -> bool:
        if isinstance(nktime2, NKTime):
            return self.tominutes() == nktime2.tominutes()
        return False

    def __lt__(self, nktime2: "NKTime") -> bool:
        return self.tominutes() < nktime2.tominutes()

    def __gt__(self, nktime2: "NKTime") -> bool:
        return self.tominutes() > nktime2.tominutes()

    def __le__(self, nktime2: "NKTime") -> bool:
        return self.tominutes() <= nktime2.tominutes()

    def __ge__(self, nktime2: "NKTime") -> bool:
        return self.tominutes() >= nktime2.tominutes()


class NoneTime(NKTime):
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
