from typing import Iterable
import pytest
from planager.entity.base.calendar import Calendar, Day
from planager.entity.base.entry import Empty, Entry

from planager.entity.base.plan import Plan
from planager.entity.base.task import Task
from planager.entity.container.entries import Entries
from planager.entity.container.tasks import Tasks
from planager.util.pdatetime import PDate
from planager.util.pdatetime.ptime import PTime


def make_plan(
    calendar: Calendar,
    tasks: Iterable[Task],
    plan: dict[PDate, list[tuple[str, str, str]]],
) -> Plan:
    p = Plan(calendar=calendar)
    p._tasks = {t.task_id: t for t in tasks}
    p._plan = plan
    return p


def sort_task_by_id(task_ids: list[Task], task_dict: dict) -> list[Task]:
    return sorted(task_ids, key=lambda t: t.priority)


def sort_task_ids(task_ids: list[tuple[str, str, str]], task_dict: dict) -> list[tuple[str, str, str]]:
    return sorted(task_ids, key=lambda t: task_dict[t].priority)


class PlanTest:
    # def test_init(self) -> None:

    # def test_copy(self) -> None:

    def test_add_tasks(self) -> None:
        """
        Cases:
        1) tasks fit
        2) tasks do not fit
        """
        plan_date = PDate(2023, 10, 15)
        plan_tasks = [
            Task("task 1", ("0", "0", "1"), priority=50, duration=30),
            Task("task 2", ("0", "0", "2"), priority=70, duration=20),
            Task("task 3", ("0", "0", "3"), priority=80, duration=20),
            Task("task 4", ("0", "0", "4"), priority=20, duration=40),
            Task("task 5", ("0", "0", "5"), priority=10, duration=30),
        ]
        calendar_norollover = Calendar(
            [
                Day(
                    plan_date,
                    Entries(
                        [
                            Entry("Sleep", PTime(0), PTime(5)),
                            Entry("Morning Routine", PTime(5), PTime(6, 20)),
                            Entry("Travel", PTime(6, 20), PTime(7, 30)),
                            Entry("Work", PTime(7, 30), PTime(16, 30)),
                            Entry("Travel", PTime(16, 30), PTime(17, 30)),
                            Empty(PTime(17, 30), PTime(21)),
                            Entry("Sleep", PTime(21), PTime(24)),
                        ]
                    ),
                ),
            ]
        )
        calendar_excess = Calendar(
            [
                Day(
                    plan_date,
                    Entries(
                        [
                            Entry("Sleep", PTime(0), PTime(5)),
                            Entry("Morning Routine", PTime(5), PTime(6, 20)),
                            Entry("Travel", PTime(6, 20), PTime(7, 30)),
                            Entry("Work", PTime(7, 30), PTime(16, 30)),
                            Entry("Travel", PTime(16, 30), PTime(17, 30)),
                            Entry("Maintenance", PTime(17, 30), PTime(20, 10)),
                            Empty(PTime(17, 30), PTime(21)),
                            Entry("Sleep", PTime(21), PTime(24)),
                        ]
                    ),
                ),
            ]
        )
        plan_start = {plan_date: [("0", "0", "1")]}

        plan_norollover = make_plan(
            calendar_norollover,
            plan_tasks,
            plan_start,
        )
        plan_excess = make_plan(
            calendar_excess,
            plan_tasks,
            plan_start,
        )

        to_add = [
            ("0", "0", "2"),
            ("0", "0", "3"),
            ("0", "0", "4"),
            ("0", "0", "5"),
        ]

        exp_tasks_norollover: list[tuple[str, str, str]] = sort_task_ids(
            [("0", "0", "1")] + to_add, plan_norollover._tasks
        )
        exp_tasks_excess: list[tuple[str, str, str]] = sort_task_ids(
            [("0", "0", "1"), ("0", "0", "2"), ("0", "0", "3")], plan_excess._tasks
        )

        exp_plan_norollover = make_plan(
            calendar_norollover,
            plan_tasks,
            {plan_date: exp_tasks_norollover},
        )
        exp_plan_excess = make_plan(
            calendar_excess,
            plan_tasks,
            {plan_date: exp_tasks_excess},
        )

        to_add_norollover: list[tuple[str, str, str]] = []
        to_add_excess: list[tuple[str, str, str]] = []

        exp_return_norollover: list[tuple[str, str, str]] = []
        exp_return_excess: list[tuple[str, str, str]] = [
            ("0", "0", "3"),
            ("0", "0", "4"),
            ("0", "0", "5"),
        ]

        return_norollover = plan_norollover.add_tasks(plan_date, to_add)
        return_excess = plan_excess.add_tasks(plan_date, to_add)

        assert return_norollover == exp_return_norollover
        assert plan_norollover == exp_plan_norollover
        assert return_excess == exp_return_excess
        assert plan_excess == exp_plan_excess

    def test_add_subplan(self) -> None:
        """
        Cases:
        1) no rollover
        2) rollover
        """
        plan_date = PDate(2023, 10, 15)
        plan_tasks = Tasks([
            Task("task 1", ("0", "0", "1"), priority=50, duration=30),
            Task("task 2", ("0", "0", "2"), priority=70, duration=20),
            Task("task 3", ("0", "0", "3"), priority=80, duration=20),
            Task("task 4", ("0", "0", "4"), priority=20, duration=40),
            Task("task 5", ("0", "0", "5"), priority=10, duration=30),
        ])
        calendar_norollover = Calendar(
            [
                Day(
                    plan_date,
                    Entries([
                        Entry("Sleep", PTime(0), PTime(5)),
                        Entry("Morning Routine", PTime(5), PTime(6, 20)),
                        Entry("Travel", PTime(6, 20), PTime(7, 30)),
                        Entry("Work", PTime(7, 30), PTime(16, 30)),
                        Entry("Travel", PTime(16, 30), PTime(17, 30)),
                        Empty(PTime(17, 30), PTime(21)),
                        Entry("Sleep", PTime(21), PTime(24)),
            ]),
                ),
            ]
        )
        calendar_rollover = Calendar(
            [
                Day(
                    plan_date,
                    Entries([
                        Entry("Sleep", PTime(0), PTime(5)),
                        Entry("Morning Routine", PTime(5), PTime(6, 20)),
                        Entry("Travel", PTime(6, 20), PTime(7, 30)),
                        Entry("Work", PTime(7, 30), PTime(16, 30)),
                        Entry("Travel", PTime(16, 30), PTime(17, 30)),
                        Empty(PTime(17, 30), PTime(21)),
                        Entry("Sleep", PTime(21), PTime(24)),
            ]),
                ),
            ]
        )
        calendar_excess = Calendar(
            [
                Day(
                    plan_date,
                    Entries([
                        Entry("Sleep", PTime(0), PTime(5)),
                        Entry("Morning Routine", PTime(5), PTime(6, 20)),
                        Entry("Travel", PTime(6, 20), PTime(7, 30)),
                        Entry("Work", PTime(7, 30), PTime(16, 30)),
                        Entry("Travel", PTime(16, 30), PTime(17, 30)),
                        Entry("Maintenance", PTime(17, 30), PTime(20, 10)),
                        Empty(PTime(17, 30), PTime(21)),
                        Entry("Sleep", PTime(21), PTime(24)),
            ]),
                ),
            ]
        )
        plan_start = (
            {
                plan_date: [("0", "0", "1")],
            }
        )

        plan_norollover = make_plan(
            calendar_norollover,
            plan_tasks,
            plan_start,
        )
        plan_rollover = make_plan(
            calendar_rollover,
            plan_tasks,
            plan_start,
        )
        plan_excess = make_plan(
            calendar_excess,
            plan_tasks,
            plan_start,
        )

        to_add = [
            ("0", "0", "2"),
            ("0", "0", "3"),
            ("0", "0", "4"),
            ("0", "0", "5"),
        ]

        exp_tasks_norollover = sort_task_ids(
            [("0", "0", "1")] + to_add, plan_norollover._tasks
        )
        exp_tasks_rollover = sort_task_ids(
            [("0", "0", "1")] + to_add, plan_norollover._tasks
        )
        exp_tasks_excess = sort_task_ids(
            [("0", "0", "1"), ("0", "0", "2"), ("0", "0", "3")], plan_excess._tasks
        )

        exp_plan_norollover = make_plan(
            calendar_norollover,
            plan_tasks,
            {plan_date: exp_tasks_norollover},
        )
        exp_plan_rollover = make_plan(
            calendar_rollover,
            plan_tasks,
            {plan_date: exp_tasks_rollover},
        )
        exp_plan_excess = make_plan(
            calendar_excess,
            plan_tasks,
            {plan_date: exp_tasks_excess},
        )

        subplan_norollover: dict[PDate, list[tuple[str, str, str]]] = {}
        subplan_rollover: dict[PDate, list[tuple[str, str, str]]] = {}
        subplan_excess: dict[PDate, list[tuple[str, str, str]]] = {}

        exp_return_norollover: list[tuple[str, str, str]] = []
        exp_return_rollover: list[tuple[str, str, str]] = []
        exp_return_excess: list[tuple[str, str, str]] = [
            ("0", "0", "3"),
            ("0", "0", "4"),
            ("0", "0", "5"),
        ]

        return_norollover = plan_norollover.add_subplan(subplan_norollover, plan_tasks)
        return_rollover = plan_rollover.add_subplan(subplan_rollover, plan_tasks)
        return_excess = plan_excess.add_subplan(subplan_excess, plan_tasks)

        assert return_norollover == exp_return_norollover
        assert plan_norollover == exp_plan_norollover
        assert return_rollover == exp_return_rollover
        assert plan_rollover == exp_plan_rollover
        assert return_excess == exp_return_excess
        assert plan_excess == exp_plan_excess

    def test_ensure_date(self) -> None:
        """
        Cases:
        1) date already exists
        2) date missing
        """
        date_present = PDate(2024, 12, 24)
        date_absent = PDate(2025, 1, 7)
        date_never = PDate(2024, 7, 13)

        plan = make_plan(
            Calendar(),
            [],
            {date_present: []},
        )

        plan.ensure_date(date_present)
        plan.ensure_date(date_absent)

        assert date_present in plan
        assert date_absent in plan
        assert not date_never in plan

    def test_end_date(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {
                PDate(2025, 5, 6): [],
                PDate(2025, 5, 23): [],
                PDate(2024, 12, 12): [],
                PDate(2025, 6, 6): [],
            },
        )
        assert plan.end_date == PDate(2025, 6, 6)

    def test_start_date(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {
                PDate(2025, 5, 6): [],
                PDate(2025, 5, 23): [],
                PDate(2024, 12, 12): [],
                PDate(2025, 6, 6): [],
            },
        )
        assert plan.start_date == PDate(2024, 12, 12)

    def test_tasks(self) -> None:
        plan = make_plan(
            Calendar(),
            [
                Task("", ("", "", "")),
                Task("", ("", "", "")),
                Task("", ("", "", "")),
                Task("", ("", "", "")),
            ],
            {},
        )
        assert plan.tasks == Tasks([
            Task("", ("", "", "")),
            Task("", ("", "", "")),
            Task("", ("", "", "")),
            Task("", ("", "", "")),
        ])

    # def test_reorder_by_precedence(self) -> None:
    #     """
    #     Cases:
    #     1)
    #     2)
    #     3)
    #     """
    #     plan = Plan()
    #     exp = Plan()

    #     plan.reorder_by_precedence()

    #     assert plan == exp

    def test_adjust_tmpdate_to_neighbors(self) -> None:
        task = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_pre = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post_impossible = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post0 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post1 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post2 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post3 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post7 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        task_post16 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_impossible = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_0 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_1 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_2 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_3 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_7 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))
        exp_16 = Task("", ("", "", ""), tmpdate=PDate(2100, 1, 1))

        # TODO: add error test
        assert (
            Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post_impossible)
            == exp_impossible
        )
        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post0) == exp_0
        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post1) == exp_1
        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post2) == exp_2
        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post3) == exp_3
        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post7) == exp_7
        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post16) == exp_16

    # def test_contains(self) -> None:

    # def test_getitem(self) -> None:

    # def test_setitem(self) -> None:

    def test_str(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        exp = (
            "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            "┃                                                    October 2023                                                      ┃\n"
            "┣━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┫\n"
            "┃      Mon       ┃      Tue       ┃      Wed       ┃      Thu       ┃      Fri       ┃      Sat       ┃      Sun       ┃\n"
            "┣━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┫\n"
            "┃       9        │       10       │       11       │       12       │       13       │       14       │       15       ┃\n"
            "┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨\n"
            "┃ Avail.: xx:xx  │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      ┃\n"
            "┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨\n"
            "┃ W:I:Testing… 1 │ W:I:Testing… 2 │ W:I:Testing… 3 │ W:I:Testing… 4 │ W:I:Testing… 5 │ W:I:Testing… 6 │ W:I:Testing… 7 ┃\n"
            "┃ W:I:Testing… 1 │ W:I:Testing… 2 │ W:I:Testing… 3 │ W:I:Testing… 4 │ W:I:Testing… 5 │ W:I:Testing… 6 │                ┃\n"
            "┃                │ W:I:Testing… 2 │ W:I:Testing… 3 │ W:I:Testing… 4 │                │ W:I:Testing… 6 │                ┃\n"
            "┃                │                │ W:I:Testing… 3 │ W:I:Testing… 4 │                │                │                ┃\n"
            "┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨\n"
            "┃ Rem.: xx:xx    │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      ┃\n"
            "┣━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┿━━━━━━━━━━━━━━━━┫\n"
            "┃       16       │       17       │       18       │       19       │       20       │       21       │       22       ┃\n"
            "┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨\n"
            "┃ Avail.: xx:xx  │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      ┃\n"
            "┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨\n"
            "┃ W:I:Testing… 1 │ W:I:Testing… 2 │ W:I:Testing… 3 │ W:I:Testing… 4 │ W:I:Testing… 5 │ W:I:Testing… 6 │ W:I:Testing… 7 ┃\n"
            "┃ W:I:Testing… 1 │ W:I:Testing… 2 │ W:I:Testing… 3 │ W:I:Testing… 4 │ W:I:Testing… 5 │ W:I:Testing… 6 │                ┃\n"
            "┃                │ W:I:Testing… 2 │ W:I:Testing… 3 │ W:I:Testing… 4 │                │ W:I:Testing… 6 │                ┃\n"
            "┃                │                │ W:I:Testing… 3 │ W:I:Testing… 4 │                │                │                ┃\n"
            "┠┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┼┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┨\n"
            "┃ Rem.: xx:xx    │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      │     xx:xx      ┃\n"
            "┗━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━┛\n"
        )
        assert str(plan) == exp

    def test_repr(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        exp = "" "" ""
        assert repr(plan) == exp
