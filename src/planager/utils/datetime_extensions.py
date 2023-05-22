from datetime import date, datetime, time, timedelta


class PlTime(time):
    def plain(self) -> time:
        return time(self.hour, self.minute)
    
    def tominutes(self) -> int:
        return 60 * self.hour + self.minute
    
    def timeto(self, time2: "PlTime") -> int:
        return time2.tominutes() - self.tominutes()
    
    def timefrom(self, time2: "PlTime") -> int:
        return self.tominutes() - time2.tominutes()
    
    @classmethod
    def fromminutes(cls, mins: int) -> "PlTime":
        return cls(*divmod(mins, 60))

    def __add__(self, mins: int) -> "PlDate":
        return PlTime.fromminutes(min(1439, max(0, self.tominutes() + mins)))
    
    def __sub__(self, mins: int) -> "PlDate":
        return PlTime.fromminutes(min(1439, max(0, self.tominutes() - mins)))

t = PlTime(4, 31)
t + 357


# class PlDateTime(datetime):
#     def __add__(self, days: int) -> "PlDate":
#         return PlDate.fromordinal(self.toordinal() + days)
    
#     def __sub__(self, days: int) -> "PlDate":
#         return PlDate.fromordinal(self.toordinal() - days)


class PlDate(date):
    def __add__(self, days: int) -> "PlDate":
        return PlDate.fromordinal(self.toordinal() + days)
    
    def __sub__(self, days: int) -> "PlDate":
        return PlDate.fromordinal(self.toordinal() - days)
    
    
