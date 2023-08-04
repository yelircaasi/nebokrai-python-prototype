import pytest

from planager.entity.base.plan import Plan
from planager.entity.base.task import Task
from planager.entity.container.tasks import Tasks
from planager.util.pdatetime import PDate


class PlanTest:
    plan1 = Plan()
    plan2 = Plan()
    plan3 = Plan()

    exp_string1 = "\n" "\n" "\n" "\n"
    exp_string2 = "\n" "\n" "\n" "\n"
    exp_string3 = "\n" "\n" "\n" "\n"

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

    def test_copy(self) -> None:
        copy1 = self.plan1.copy()
        copy2 = self.plan2.copy()
        copy3 = self.plan3.copy()
        
        assert self.plan1 == copy1
        assert self.plan2 == copy2
        assert self.plan3 == copy3
        
        assert id(self.plan1) != id(copy1)
        assert id(self.plan2) != id(copy2)
        assert id(self.plan3) != id(copy3)
        
    def test_add_tasks(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.plan1
        assert self.plan2
        assert self.plan3

    def test_add_subplan(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        plan4 = Plan()
        plan5 = Plan()
        subplan1 = {PDate(0, 0, 0): ("", "", ""), PDate(0, 0, 0): ("", "", "")}
        subplan2 = {PDate(0, 0, 0): ("", "", ""), PDate(0, 0, 0): ("", "", "")}
        tasks1 = Tasks([Task(""), Task(""), Task("")])
        tasks2 = Tasks([Task(""), Task(""), Task("")])

        plan4.add_subplan(subplan1, tasks1)
        assert plan4

        plan4.add_subplan(subplan2, tasks2)
        assert plan5

    def test_ensure_date(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        plan4 = Plan()
        d = PDate(0, 0, 0)

        plan4.ensure_date()
        assert plan4

    def test_end_date(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.plan1.end_date == PDate(0, 0, 0)
        assert self.plan2.end_date == PDate(0, 0, 0)
        assert self.plan3.end_date == PDate(0, 0, 0)

    def test_start_date(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.plan1.start_date == PDate(0, 0, 0)
        assert self.plan2.start_date == PDate(0, 0, 0)
        assert self.plan3.start_date == PDate(0, 0, 0)

    def test_tasks(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.plan1.tasks == ...
        assert self.plan2.tasks == ...
        assert self.plan3.tasks == ...

    def test_reorder_by_precedence(self) -> None:
        p1 = self.plan1.copy()
        p2 = self.plan2.copy()
        p3 = self.plan3.copy()

        p1.reorder_by_precedence()
        p2.reorder_by_precedence()
        p3.reorder_by_precedence()

        assert p1 == Plan()
        assert p2 == Plan()
        assert p3 == Plan()

    def test_adjust_tmpdate_to_neighbors(self) -> None:
        task1 = Task("", ("", "", ""))
        task2 = Task("", ("", "", ""))
        task3 = Task("", ("", "", ""))
        task4 = Task("", ("", "", ""))
        task5 = Task("", ("", "", ""))

        exp1 = Task("", ("", "", ""))
        exp2 = Task("", ("", "", ""))
        exp3 = Task("", ("", "", ""))

        assert Plan.adjust_tmpdate_to_neighbors(task2, task1, task3) == exp1
        assert Plan.adjust_tmpdate_to_neighbors(task3, task2, task4) == exp2
        assert Plan.adjust_tmpdate_to_neighbors(task4, task3, task5) == exp3

    def test_getitem(self) -> None:
        assert self.plan1[PDate(0, 0, 0)]
        assert self.plan2[PDate(0, 0, 0)]
        assert self.plan3[PDate(0, 0, 0)]

    def test_setitem(self) -> None:
        plan4 = Plan()

        plan4[PDate(0, 0, 0)] = plan4
        plan4[PDate(0, 0, 0)] = plan4
        plan4[PDate(0, 0, 0)] = plan4

        assert plan4 == plan4
        assert plan4 == plan4
        assert plan4 == plan4

    def test_str(self) -> None:
        assert str(self.plan1) == self.exp_string1
        assert str(self.plan2) == self.exp_string2
        assert str(self.plan3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.plan1) == self.exp_string1
        assert repr(self.plan2) == self.exp_string2
        assert repr(self.plan3) == self.exp_string3
