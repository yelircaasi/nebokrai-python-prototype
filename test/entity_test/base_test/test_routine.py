import pytest

from planager.entity.base.entry import Entry
from planager.entity.base.routine import Routine
from planager.entity.base.task import Task
from planager.util.pdatetime.pdate import PDate
from planager.util.pdatetime.ptime import PTime


class RoutineTest:
    def test_init(self) -> None:
        routine = Routine()

    def test_valid_on__via_list(self) -> None:
        routine = Routine()
        valid_date = PDate()
        invalid_date = PDate()

        assert routine.valid_on(valid_date)
        assert not routine.valid_on(invalid_date)

    def test_valid_on__via_callable(self) -> None:
        routine = Routine()
        valid_date1 = PDate()
        valid_date2 = PDate()
        valid_date3 = PDate()
        invalid_date1 = PDate()
        invalid_date2 = PDate()
        invalid_date3 = PDate()

        assert routine.valid_on(valid_date1)
        assert routine.valid_on(valid_date2)
        assert routine.valid_on(valid_date3)
        assert not routine.valid_on(invalid_date1)
        assert not routine.valid_on(invalid_date2)
        assert not routine.valid_on(invalid_date3)

    def test_as_entry(self) -> None:
        routine = Routine()
        entry = Entry()
        assert routine.as_entry == entry

    def test_as_task(self) -> None:
        routine = Routine()
        task = Task()
        assert routine.as_task == task

    def test_pretty(self) -> None:
        routine = Routine()
        exp = ()
        assert routine.pretty() == exp

    def test_str(self) -> None:
        routine = Routine()
        exp = ()
        assert str(routine) == exp

    def test_repr(self) -> None:
        routine = Routine()
        exp = ()
        assert repr(routine) == exp
