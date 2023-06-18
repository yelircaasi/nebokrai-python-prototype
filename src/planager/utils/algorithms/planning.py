from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from planager.utils.datetime_extensions import PDate

ClusterType = List[Union[List[Tuple[int, int, int]], List[int]]]
# SubplanType = Dict[PDate, List[int]]
SubplanType = Dict[PDate, Union[List[int], List[Tuple[int, int, int]]]]


################################################################################


class Adjustment(Enum):
    ROLLOVER = 0
    RIGID = 1
    BALANCE = 2
    MANUAL = 3


TODAY = PDate.today()


# def adjust_loads(
#     start: PDate = TODAY,
#     end: PDate = TODAY + 7,
#     algorithm: Adjustment = Adjustment.MANUAL,
#     n: Optional[int] = None,
# ) -> None:
#     if algorithm == Adjustment.ROLLOVER:
#         self.adjust_loads_rollover(start, end)
#     elif algorithm == Adjustment.RIGID:
#         self.adjust_loads_rigid(start, end, n=n or 1)
#     elif algorithm == Adjustment.BALANCE:
#         self.adjust_loads_balance(start, end)
#     elif algorithm == Adjustment.MANUAL:
#         self.adjust_loads_manual()
#     else:
#         raise ValueError("Invalid adjustment algorithm type.")


# def adjust_loads_rollover(start: PDate, end: PDate) -> None:
#     d = PDate.fromordinal(start.toordinal())
#     while d <= end:
#         self.ensure_day(d)
#         day_tasks = [self.tasks[i] for i in self.days[d].tasks]
#         day_tasks.sort(key=lambda t: t.priority.value, reverse=True)
#         max_load = self.days[d].max_load
#         total_load = sum(map(lambda t: t.duration, day_tasks))
#         while total_load > max_load:
#             task_to_move = day_tasks.pop()
#             id_to_move = task_to_move.id
#             self.edit_task(id_to_move, "date", d + 1)
#             total_load -= task_to_move.duration
#         d += 1
#     self.sort_days()


# def adjust_loads_rigid(start: PDate, end: PDate, n: int = 1) -> None:
#     for t in self.tasks:
#         if start <= self.tasks[t].date <= end:
#             self.tasks[t].date += n
#     for d in date_range(end, start):
#         tasks = self.days[d].tasks
#         self.days[d + n].tasks.extend(tasks)
#         self.days[d].tasks = []
#     for p in self.projects:
#         if self.projects[p].start <= end:
#             self.projects[p].start += n
#             if self.projects[p].end:
#                 self.projects[p].end += n
#     self.sort_days()


# def adjust_loads_balance(start: PDate, end: PDate) -> None:
#     loads: Dict[PDate, int] = self.get_loads_by_day(start=start, end=end)
#     mean_load = int(sum(loads.values()) / len(loads)) + 1
#     d = PDate.fromordinal(start.toordinal())
#     self.ensure_day(d)
#     while d <= end:
#         self.ensure_day(d + 1)
#         day_tasks = [self.tasks[i] for i in self.days[d].tasks]
#         day_tasks.sort(key=lambda t: t.priority.value, reverse=True)
#         next_day_tasks = [self.tasks[i] for i in self.days[d + 1].tasks]
#         next_day_tasks.sort(key=lambda t: t.priority.value, reverse=True)
#         max_load = mean_load + 30
#         total_load = sum(map(lambda t: t.duration, day_tasks))
#         while abs(total_load - max_load) > 31:
#             if total_load > max_load:
#                 task_to_move = day_tasks.pop()
#                 id_to_move = task_to_move.id
#                 self.edit_task(id_to_move, "date", d + 1)
#                 total_load -= task_to_move.duration
#                 if (max_load - total_load) > 31:
#                     continue
#             elif total_load < max_load:
#                 task_to_move = next_day_tasks.pop()
#                 id_to_move = task_to_move.id
#                 self.edit_task(id_to_move, "date", d + 1)
#                 total_load += task_to_move.duration
#                 if (total_load - max_load) > 31:
#                     continue
#         d += 1
#     self.sort_days()

# def adjust_loads_manual(self) -> None:

#     self.sort_days()


def sort_days(days) -> None:
    return dict(sorted([(k, v) for k, v in days.items()]))
