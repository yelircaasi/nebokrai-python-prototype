from typing import Any, Optional


class PTime:
    """
    Bespoke time class designed to simplify the planager codebase.
    """

    def __init__(self, hour: int = 0, minute: int = 0, isblank: bool = False):
        if not ((hour >= 0) and (minute >= 0) and (60 * hour + minute) in range(1441)):
            raise ValueError("Time must be within 00:00..24:00")
        self.hour = hour
        self.minute = minute
        self.isblank = isblank

    @classmethod
    def from_string(cls, date_string: Optional[str]) -> "PTime":
        assert isinstance(date_string, str)
        if not date_string:
            res = cls()
            res.isblank = True
            return res
        hour, minute = map(int, date_string.split(":")[:2])
        return cls(hour, minute)

    @classmethod
    def ensure_is_ptime(
        cls,
        candidate: Any,
        default: Optional["PTime"] = None,
    ) -> "PTime":
        """
        Converts values of several types into the corresponding PTime
        """
        if (candidate is None) and default:
            return default
        if isinstance(candidate, PTime):
            return candidate
        if isinstance(candidate, str):
            if not candidate.strip():
                pass
            try:
                return PTime.from_string(candidate)
            except AssertionError:
                pass
        elif isinstance(candidate, tuple):
            try:
                assert len(candidate) == 2
                hour, minute = map(int, candidate)
                return PTime(hour, minute)
            except AssertionError:
                pass
        elif isinstance(candidate, int):
            try:
                return PTime(candidate)
            except ValueError:
                pass
        else:
            pass
        if isinstance(default, PTime):
            return default
        raise ValueError(f"Impossible conversion requested: {str(candidate)} -> 'PTime'.")

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
        return t2 - t1  # if ((t1 is not None) and (t2 is not None)) else None

    def timefrom(self, time2: "PTime") -> int:
        t2, t1 = self.tominutes(), time2.tominutes()
        return t2 - t1  # if ((t1 is not None) and (t2 is not None)) else None

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


class NoneTime(PTime):
    """
    Empty time for cases where this may be superior to using None
    """

    def __init__(self) -> None:
        super().__init__()

    def __bool__(self) -> bool:
        return False

    def __eq__(self, __other: Any) -> bool:
        return isinstance(__other, NoneTime)

    def __lt__(self, __other: Any) -> bool:
        return False

    def __gt__(self, __other: Any) -> bool:
        return False

    def __le__(self, __other: Any) -> bool:
        return True

    def __ge__(self, __other: Any) -> bool:
        return True

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "NoneTime"
