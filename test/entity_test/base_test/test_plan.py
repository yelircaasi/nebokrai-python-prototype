import pytest

from planager.entity.base.plan import Plan
from planager.entity.base.task import Task
from planager.util.pdatetime import PDate


class PlanTest:
    plan1 = Plan()
    plan2 = Plan()
    plan3 = Plan()

    exp_string1 = '\n'.join(
        "",
        "",
        "",
    )
    exp_string2 = '\n'.join(
        "",
        "",
        "",
    )
    exp_string3 = '\n'.join(
        "",
        "",
        "",
    )

    def test_init(self) -> None:
        assert self.plan1
        assert self.plan2
        assert self.plan3

    def test_getitem(self) -> None:
        assert self.plan1[...]
        assert self.plan2[...]
        assert self.plan3[...]

    def test_setitem(self) -> None:
        plan4 = Plan()

        plan4[...] = ...
        plan4[...] = ...
        plan4[...] = ...

        assert plan4 == ...
        assert plan4 == ...
        assert plan4 == ...
        
    def test_add_tasks(self) -> None:
        assert self.plan1
        assert self.plan2
        assert self.plan3

    def test_add_subplan(self) -> None:
        plan4 = Plan()

        plan4.add_subplan()
        assert plan4

        plan4.add_subplan()
        assert plan4

    def test_ensure_date(self) -> None:
        plan4 = Plan()
        d = PDate()

        plan4.ensure_date()
        assert plan4

    def test_end_date(self) -> None:
        assert self.plan1.end_date == PDate()
        assert self.plan2.end_date == PDate()
        assert self.plan3.end_date == PDate()

    def test_start_date(self) -> None:
        assert self.plan1.start_date == PDate()
        assert self.plan2.start_date == PDate()
        assert self.plan3.start_date == PDate()

    def test_tasks(self) -> None:
        assert self.plan1.tasks == ...
        assert self.plan2.tasks == ...
        assert self.plan3.tasks == ...

    def test_reorder_by_precedence(self) -> None:
        p1 = self.plan1.copy()
        p2 = self.plan2.copy()
        p3 = self.plan3.copy()

        assert p1.reorder_by_precedence()
        assert p2.reorder_by_precedence()
        assert p3.reorder_by_precedence()

        assert p1 
        assert p2
        assert p3

    def test_adjust_tmpdate_to_neighbors(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()
        task4 = Task()
        task5 = Task()

        exp1 = Task()
        exp2 = Task()
        exp3 = Task()

        assert Plan.adjust_template_to_neighbors(task2, task1, task3) == exp1
        assert Plan.adjust_template_to_neighbors(task3, task2, task4) == exp2
        assert Plan.adjust_template_to_neighbors(task4, task3, task5) == exp3

    def test_str(self) -> None:
        assert str(self.plan1) == self.exp_string1
        assert str(self.plan2) == self.exp_string2
        assert str(self.plan3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.plan1) == self.exp_string1
        assert repr(self.plan2) == self.exp_string2
        assert repr(self.plan3) == self.exp_string3
