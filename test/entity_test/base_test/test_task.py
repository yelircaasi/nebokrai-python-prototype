import pytest

from planager.entity import Entry, Task
from planager.util.pdatetime.ptime import PTime


class TaskTest:
    def test_init(self) -> None:
        task_default = Task()
        task_custom = Task()

        assert task_default.name == ""
        assert task_default.task_id == ()
        assert task_default.priority == ...
        assert task_default.duration == ...
        assert task_default.dependencies == ()
        assert task_custom.name == ""
        assert task_custom.task_id == ()
        assert task_custom.priority == ...
        assert task_custom.duration == ...
        assert task_custom.dependencies == ()

    def test_eq_copy(self) -> None:
        task = Task()

        assert task == task.copy()
        assert task.__dict__ == task.copy().__dict__

    def test_isafter(self) -> None:
        task1 = Task()
        task2 = Task()

        assert task1.isafter(task2)
        assert not task2.isafter(task1)
        assert not task1.isafter(task1)
        assert not task2.isafter(task2)

    def test_as_entry(self) -> None:
        task = Task()
        entry = Entry("", PTime())
        assert task.as_entry(PTime(0, 0)) == entry

    def test_pretty(self) -> None:
        task = Task()
        exp = ()
        assert task.pretty() == exp

    def test_eq(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()
        assert task1 == task2
        assert not task1 == task3
        assert task2 != task3

    def test_lt(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()
        assert task1 < task2 < task3
        assert not task2 < task1
        assert not task3 < task2

    def test_gt(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()
        assert task1 > task2 > task3
        assert not task2 > task1
        assert not task3 > task2

    def test_le(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()
        assert task1 <= task2 <= task3
        assert task2 <= task1
        assert not task3 <= task2

    def test_ge(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()
        assert task1 >= task2 <= task3
        assert task2 >= task1
        assert not task3 >= task2

    def test_str(self) -> None:
        task = Task()
        exp = ()
        assert str(task) == exp

    def test_repr(self) -> None:
        task = Task()
        exp = ()
        assert repr(task) == exp
