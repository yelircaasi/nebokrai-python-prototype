from datetime import date, datetime
from typing import List, Tuple, Union


def now() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class PTime:
    def __init__(self, hour=0, minute=0, isblank=False):
        if not (60 * hour + minute) in range(1441):
            raise ValueError("Time must be within 00:00..24:00")
        self.__dict__.update(locals())

    @classmethod
    def from_string(cls, date_string: str) -> "PTime":
        hour, minute = map(int, date_string.split(":"))
        return cls(hour, minute)
    
    def __bool__(self):
        return (not self.isblank)

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

    def __add__(self, mins: int) -> "PDate":
        return PTime.fromminutes(min(1440, max(0, self.tominutes() + mins)))
    
    def __sub__(self, mins: int) -> "PDate":
        return PTime.fromminutes(min(1440, max(0, self.tominutes() - mins)))
    
    def __str__(self) -> str:
        return f"{self.hour:0>2}:{self.minute:0>2}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, ptime2: "PTime") -> bool:
        return self.tominutes() == ptime2.tominutes()

    def __lt__(self, ptime2: "PTime") -> bool:
        return self.tominutes() < ptime2.tominutes()
    
    def __gt__(self, ptime2: "PTime") -> bool:
        return self.tominutes() > ptime2.tominutes()
    
    def __le__(self, ptime2: "PTime") -> bool:
        return self.tominutes() <= ptime2.tominutes()
    
    def __ge__(self, ptime2: "PTime") -> bool:
        return self.tominutes() >= ptime2.tominutes()

#t = PTime(4, 31)
#t + 357


# class PDateTime(datetime):
#     def __add__(self, days: int) -> "PDate":
#         return PDate.fromordinal(self.toordinal() + days)
    
#     def __sub__(self, days: int) -> "PDate":
#         return PDate.fromordinal(self.toordinal() - days)


PDateInputType = Union["PDate", str, Tuple[int, int, int], int]


class PDate(date):
    def copy(self):
        return PDate(self.year, self.month, self.day)
    
    def __add__(self, days: int) -> "PDate":
        return PDate.fromordinal(self.toordinal() + days)
    
    def __sub__(self, days: int) -> "PDate":
        return PDate.fromordinal(self.toordinal() - days)
    
    def pretty(self):
        DAYS = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        MONTHS = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        ORDINAL_ENDINGS = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}
        ending = ORDINAL_ENDINGS.get(self.day, "th")
        return f"{DAYS[self.weekday()]}, {MONTHS[self.month]} {self.day}{ending}, {self.year}"   
    
    @classmethod
    def ensure_is_pdate(cls, candidate: Union["PDate", str, Tuple[int, int, int], int]) -> "PDate":
        if isinstance(candidate, PDate):
            pass
        elif isinstance(candidate, str):
            try:
              candidate = PDate.fromisoformat(candidate)
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{candidate}'")
        elif isinstance(candidate, tuple):
            try:
              candidate = PDate(*candidate)
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{str(candidate)}'")
        elif isinstance(candidate, int):
            try:
              candidate = PDate.today() + candidate
            except:
                raise ValueError(f"Invalid input for `PDate` class: '{str(candidate)}'")
        else:
            raise ValueError(f"Invalid input type for `PDate` class: '{type(candidate)}' (value: '{candidate}')")
        return candidate
    
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


class PDateTime:
    ...


ZERODATE = PDate(2023, 1, 1)



