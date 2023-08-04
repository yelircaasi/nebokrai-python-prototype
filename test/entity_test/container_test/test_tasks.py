import pytest

from planager.entity.base.task import Task
from planager.entity.container.tasks import Tasks


class TasksTest:
    tasks1 = Tasks()
    tasks2 = Tasks()
    tasks3 = Tasks()

    exp_string1 = "\n" "\n" ""
    exp_string2 = "\n" "\n" ""
    exp_string3 = "\n" "\n" ""

    def test_init(self) -> None:
        assert self.tasks1
        assert self.tasks2
        assert self.tasks3

    def test_from_string_iterable(self) -> None:
        tasks4 = Tasks.from_string_iterable()
        tasks5 = Tasks.from_string_iterable()
        tasks6 = Tasks.from_string_iterable()

        assert tasks4 == self.tasks1
        assert tasks5 == self.tasks2
        assert tasks6 == self.tasks3

    def test_from_norg_path(self) -> None:
        tasks4 = Tasks.from_norg_path()
        tasks5 = Tasks.from_norg_path()
        tasks6 = Tasks.from_norg_path()

        assert tasks4 == self.tasks1
        assert tasks5 == self.tasks2
        assert tasks6 == self.tasks3

    def test_from_roadmaps(self) -> None:
        tasks4 = Tasks.from_roadmaps()
        tasks5 = Tasks.from_roadmaps()
        tasks6 = Tasks.from_roadmaps()

        assert tasks4 == self.tasks1
        assert tasks5 == self.tasks2
        assert tasks6 == self.tasks3

    def test_add(self) -> None:
        tasks4 = Tasks()
        tasks5 = Tasks()

        exp4 = Tasks()
        exp5 = Tasks()

        tasks4.add(Task())
        tasks5.add(Task())

        assert tasks4 == exp4
        assert tasks5 == exp5

    def test_task_ids(self) -> None:
        exp1 = [(), (), ()]
        exp2 = [(), (), ()]
        exp3 = [(), (), ()]

        assert self.tasks1.task_ids == exp1
        assert self.tasks2.task_ids == exp2
        assert self.tasks3.task_ids == exp3

    def test_pretty(self) -> None:
        assert self.tasks1.pretty() == self.exp_string1
        assert self.tasks2.pretty() == self.exp_string2
        assert self.tasks3.pretty() == self.exp_string3

    def test_iter(self) -> None:
        assert list(self.tasks1) == []
        assert list(self.tasks2) == []
        assert set(self.tasks3) == {}

    def test_getitem(self) -> None:
        assert self.tasks1[...] == ...
        assert self.tasks2[...] == ...
        assert self.tasks3[...] == ...

    def test_str(self) -> None:
        assert str(self.tasks1) == self.exp_string1
        assert str(self.tasks2) == self.exp_string2
        assert str(self.tasks3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.tasks1) == self.exp_string1
        assert repr(self.tasks2) == self.exp_string2
        assert repr(self.tasks3) == self.exp_string3
