import pytest

from planager.entity import Entry, Task
from planager.util.pdatetime.ptime import PTime


class TaskTest:
    task1 = Task("", ("", "", ""))
    task2 = Task("", ("", "", ""))
    task3 = Task("", ("", "", ""))
    task4 = Task("", ("", "", ""))
    task5 = Task("", ("", "", ""))

    exp_string1 = "\n" "\n" ""
    exp_string2 = "\n" "\n" ""
    exp_string3 = "\n" "\n" ""
    exp_string4 = "\n" "\n" ""
    exp_string5 = "\n" "\n" ""

    def test_init(self) -> None:
        assert self.task1
        assert self.task2
        assert self.task3
        assert self.task4
        assert self.task5

    def test_eq_copy(self) -> None:
        copy1 = self.task1.copy()
        copy2 = self.task2.copy()
        copy3 = self.task3.copy()
        copy4 = self.task4.copy()
        copy5 = self.task5.copy()

        assert self.task1 == copy1
        assert self.task2 == copy2
        assert self.task3 == copy3
        assert self.task4 == copy4
        assert self.task5 == copy5

        assert id(self.task1) != id(copy1)
        assert id(self.task2) != id(copy2)
        assert id(self.task3) != id(copy3)
        assert id(self.task4) != id(copy4)
        assert id(self.task5) != id(copy5)

    def test_isafter(self) -> None:
        assert self.task1.isafter(self.task2)
        assert not self.task1.isafter(self.task3)

    def test_as_entry(self) -> None:
        entry1 = Entry("", PTime())
        entry2 = Entry("", PTime())
        entry3 = Entry("", PTime())
        entry4 = Entry("", PTime())
        entry5 = Entry("", PTime())

        assert self.task1.as_entry() == entry1
        assert self.task2.as_entry() == entry2
        assert self.task3.as_entry() == entry3
        assert self.task4.as_entry() == entry4
        assert self.task5.as_entry() == entry5

    def test_pretty(self) -> None:
        assert self.task1.pretty() == self.exp_string1
        assert self.task2.pretty() == self.exp_string2
        assert self.task3.pretty() == self.exp_string3
        assert self.task4.pretty() == self.exp_string4
        assert self.task5.pretty() == self.exp_string5

    def test_eq(self) -> None:
        assert self.task1 == Task("", ("", "", ""))
        assert self.task2 == Task("", ("", "", ""))
        assert self.task3 == Task("", ("", "", ""))
        assert self.task4 == Task("", ("", "", ""))
        assert self.task5 == Task("", ("", "", ""))

    def test_lt(self) -> None:
        assert self.task1 < self.task4
        assert self.task2 < self.task5
        assert not self.task3 < self.task1
        assert not self.task4 < self.task1
        assert not self.task5 < self.task2

    def test_gt(self) -> None:
        assert self.task4 > self.task1
        assert self.task5 > self.task2
        assert not self.task1 > self.task3
        assert not self.task1 > self.task4
        assert not self.task2 > self.task5

    def test_le(self) -> None:
        assert self.task1 <= self.task4
        assert self.task2 <= self.task5
        assert self.task3 <= self.task1
        assert not self.task4 <= self.task1
        assert not self.task5 <= self.task2

    def test_ge(self) -> None:
        assert self.task4 >= self.task1
        assert self.task5 >= self.task2
        assert self.task1 >= self.task3
        assert not self.task1 >= self.task4
        assert not self.task2 >= self.task5

    def test_str(self) -> None:
        assert str(self.task1) == self.exp_string1
        assert str(self.task1) == self.exp_string2
        assert str(self.task1) == self.exp_string3
        assert str(self.task1) == self.exp_string4
        assert str(self.task1) == self.exp_string5

    def test_repr(self) -> None:
        assert repr(self.task1) == self.exp_string1
        assert repr(self.task1) == self.exp_string2
        assert repr(self.task1) == self.exp_string3
        assert repr(self.task1) == self.exp_string4
        assert repr(self.task1) == self.exp_string5
