import pytest

from planager.entity.base.plan import Plan
from planager.entity.base.task import Task
from planager.entity.container.tasks import Tasks
from planager.util.pdatetime import PDate


def make_plan(
    tasks: dict[tuple[str, str, str], Task],
    plan: dict[PDate, list[tuple[str, str, str]]],
) -> Plan:
    p = Plan()
    p._tasks = tasks
    p._plan = plan
    return p


class PlanTest:
    # plan1 = Plan()
    # plan2 = Plan()
    # plan3 = Plan()

    # exp_string1 = "\n" "\n" "\n" "\n"
    # exp_string2 = "\n" "\n" "\n" "\n"
    # exp_string3 = "\n" "\n" "\n" "\n"

    # def test_init(self) -> None:
    # """
    # Cases:
    # 1)
    # 2)
    # 3)
    # """
    #     assert self.plan1
    #     assert self.plan2
    #     assert self.plan3

    # def test_copy(self) -> None:
    #     copy1 = self.plan1.copy()
    #     copy2 = self.plan2.copy()
    #     copy3 = self.plan3.copy()

    #     assert self.plan1 == copy1
    #     assert self.plan2 == copy2
    #     assert self.plan3 == copy3

    #     assert id(self.plan1) != id(copy1)
    #     assert id(self.plan2) != id(copy2)
    #     assert id(self.plan3) != id(copy3)

    def test_add_tasks(self) -> None:
        """
        Cases:
        1) tasks fit
        2) tasks do not fit
        """
        plan_fit = make_plan(
            {},
            {},
        )
        plan_excess = make_plan(
            {},
            {},
        )

        exp_fit = make_plan(
            {},
            {},
        )
        exp_excess = make_plan(
            {},
            {},
        )

        assert plan_fit.add_tasks(PDate(), []) == []
        assert plan_fit == exp_fit
        assert plan_excess.add_tasks(PDate(), []) == []
        assert plan_excess == exp_excess

    def test_add_subplan(self) -> None:
        """
        Cases:
        1) no rollover
        2) rollover
        """
        no_rollover = Plan()
        rollover = Plan()

        subplan_no_rollover = {}
        subplan_rollover = {}

        exp_no_rollover = Plan()
        exp_rollover = Plan()

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
        plan = Plan()
        date_present = PDate(0, 0, 0)
        date_absent = PDate(0, 0, 0)
        date_never = PDate(0, 0, 0)

        plan.ensure_date(date_present)
        plan.ensure_date(date_absent)

        assert date_present in plan
        assert date_absent in plan
        assert not date_never in plan

    def test_end_date(self) -> None:
        plan = Plan()
        assert plan.end_date == PDate(0, 0, 0)

    def test_start_date(self) -> None:
        plan = Plan()
        assert plan.start_date == PDate(0, 0, 0)

    def test_tasks(self) -> None:
        plan = Plan()
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
        plan = Plan()
        exp = "" "" ""
        assert str(plan) == exp

    def test_repr(self) -> None:
        plan = Plan()
        exp = "" "" ""
        assert repr(plan) == exp
