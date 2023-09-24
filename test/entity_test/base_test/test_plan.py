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
    tasks: list[Task],
    plan: dict[PDate, list[tuple[str, str, str]]],
) -> Plan:
    p = Plan(calendar=calendar)
    p._tasks = {t.task_id: t for t in tasks}
    p._plan = plan
    return p


def sort_task_ids(task_ids: list[Task], task_dict: dict) -> list[Task]:
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
        calendar_fit = Calendar(
            [
                Day(
                    plan_date,
                    Entries(
                        Entry("Sleep", PTime(0), PTime(5)),
                        Entry("Morning Routine", PTime(5), PTime(6, 20)),
                        Entry("Travel", PTime(6, 20), PTime(7, 30)),
                        Entry("Work", PTime(7, 30), PTime(16, 30)),
                        Entry("Travel", PTime(16, 30), PTime(17, 30)),
                        Empty(PTime(17, 30), PTime(21)),
                        Entry("Sleep", PTime(21), PTime(24)),
                    ),
                ),
            ]
        )
        calendar_excess = Calendar(
            [
                Day(
                    plan_date,
                    Entries(
                        Entry("Sleep", PTime(0), PTime(5)),
                        Entry("Morning Routine", PTime(5), PTime(6, 20)),
                        Entry("Travel", PTime(6, 20), PTime(7, 30)),
                        Entry("Work", PTime(7, 30), PTime(16, 30)),
                        Entry("Travel", PTime(16, 30), PTime(17, 30)),
                        Entry("Maintenance", PTime(17, 30), PTime(20, 10)),
                        Empty(PTime(17, 30), PTime(21)),
                        Entry("Sleep", PTime(21), PTime(24)),
                    ),
                ),
            ]
        )
        plan_start = (
            {
                plan_date: [("0", "0", "1")],
            },
        )

        plan_fit = make_plan(
            calendar_fit,
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

        exp_tasks_fit = sort_task_ids([("0", "0", "1")] + to_add, plan_fit._tasks)
        exp_tasks_excess = sort_task_ids(
            [("0", "0", "1"), ("0", "0", "2"), ("0", "0", "3")], plan_excess._tasks
        )

        exp_plan_fit = make_plan(
            calendar_fit,
            plan_tasks,
            {plan_date: exp_tasks_fit},
        )
        exp_plan_excess = make_plan(
            calendar_excess,
            plan_tasks,
            {plan_date: exp_tasks_excess},
        )

        to_add_fit = []
        to_add_excess = []

        exp_return_fit = []
        exp_return_excess = [
            ("0", "0", "3"),
            ("0", "0", "4"),
            ("0", "0", "5"),
        ]

        return_fit = plan_fit.add_tasks(plan_date, to_add)
        return_excess = plan_excess.add_tasks(plan_date, to_add)

        assert return_fit == exp_return_fit
        assert plan_fit == exp_plan_fit
        assert return_excess == exp_return_excess
        assert plan_excess == exp_plan_excess

    def test_add_subplan(self) -> None:
        """
        Cases:
        1) no rollover
        2) rollover
        """
        no_rollover = make_plan(
            Calendar(),
            [],
            {},
        )
        rollover = make_plan(
            Calendar(),
            [],
            {},
        )

        subplan_no_rollover = {}
        subplan_rollover = {}

        exp_no_rollover = make_plan(
            Calendar(),
            [],
            {},
        )
        exp_rollover = make_plan(
            Calendar(),
            [],
            {},
        )

        no_rollover.add_subplan(subplan_no_rollover)
        rollover.add_subplan(subplan_rollover)

        assert no_rollover == exp_no_rollover
        assert rollover == exp_rollover

    def test_ensure_date(self) -> None:
        """
        Cases:
        1) date already exists
        2) date missing
        """
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        date_present = PDate(0, 0, 0)
        date_absent = PDate(0, 0, 0)
        date_never = PDate(0, 0, 0)

        plan.ensure_date(date_present)
        plan.ensure_date(date_absent)

        assert date_present in plan
        assert date_absent in plan
        assert not date_never in plan

    def test_end_date(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        assert plan.end_date == PDate(0, 0, 0)

    def test_start_date(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        assert plan.start_date == PDate(0, 0, 0)

    def test_tasks(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        assert plan.tasks == ...

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
        task = Task("", ("", "", ""))
        task_pre = Task("", ("", "", ""))
        task_post = Task("", ("", "", ""))
        exp = Task("", ("", "", ""))

        assert Plan.adjust_tmpdate_to_neighbors(task, task_pre, task_post) == exp

    # def test_contains(self) -> None:

    # def test_getitem(self) -> None:

    # def test_setitem(self) -> None:

    def test_str(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        exp = "" "" ""
        assert str(plan) == exp

    def test_repr(self) -> None:
        plan = make_plan(
            Calendar(),
            [],
            {},
        )
        exp = "" "" ""
        assert repr(plan) == exp
