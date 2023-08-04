import pytest

from planager.entity.base.entry import Entry
from planager.entity.base.routine import Routine
from planager.entity.base.task import Task
from planager.util.pdatetime.pdate import PDate
from planager.util.pdatetime.ptime import PTime


class RoutineTest:
    routine1 = Routine("")
    routine2 = Routine("")
    routine3 = Routine("")

    exp_string1 = "\n" "\n" "\n" "\n"
    exp_string2 = "\n" "\n" "\n" "\n"
    exp_string3 = "\n" "\n" "\n" "\n"

    def test_init(self) -> None:
        assert self.routine1
        assert self.routine2
        assert self.routine3

    def test_valid_on(self) -> None:
        assert self.routine1.valid_on(PDate(0, 0, 0))
        assert self.routine2.valid_on(PDate(0, 0, 0))
        assert self.routine3.valid_on(PDate(0, 0, 0))

        assert not self.routine1.valid_on(PDate(0, 0, 0))
        assert not self.routine2.valid_on(PDate(0, 0, 0))
        assert not self.routine3.valid_on(PDate(0, 0, 0))

    def test_as_entry(self) -> None:
        entry1 = Entry("", PTime())
        entry2 = Entry("", PTime())
        entry3 = Entry("", PTime())

        assert self.routine1.as_entry()
        assert self.routine2.as_entry()
        assert self.routine3.as_entry()

    def test_as_task(self) -> None:
        task1 = Task()
        task2 = Task()
        task3 = Task()

        assert self.routine1.as_task()
        assert self.routine2.as_task()
        assert self.routine3.as_task()

    def test_pretty(self) -> None:
        assert self.routine1.pretty() == self.exp_string1
        assert self.routine2.pretty() == self.exp_string2
        assert self.routine3.pretty() == self.exp_string3

    def test_str(self) -> None:
        assert str(self.routine1) == self.exp_string1
        assert str(self.routine2) == self.exp_string2
        assert str(self.routine3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.routine1) == self.exp_string1
        assert repr(self.routine2) == self.exp_string2
        assert repr(self.routine3) == self.exp_string3
