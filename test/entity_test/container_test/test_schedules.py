import pytest

from planager.entity.container.schedules import Schedules
from planager.entity.base.schedule import Schedule


class SchedulesTest:
    schedules1 = Schedules()
    schedules2 = Schedules()

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

    def test_init(self) -> None:
        assert self.schedules1
        assert self.schedules2

    def test_from_norg_workspace(self) -> None:
        schedules3 = Schedules.from_norg_workspace()
        schedules4 = Schedules.from_norg_workspace()

        assert schedules3 == self.schedules1
        assert schedules4 == self.schedules2

    def test_len(self) -> None:
        assert len(self.schedules1) == 4
        assert len(self.schedules2) == 3

    def test_getitem(self) -> None:
        assert self.schedules1[...] == ...
        assert self.schedules2[...] == ...

    def test_setitem(self) -> None:
        sched = Schedules()

        exp = Schedules()

        sched[3] = Schedule()
        sched[1] = Schedule()

        assert sched == exp

    def test_str(self) -> None:
        assert str(self.schedules1) == self.exp_string1
        assert str(self.schedules2) == self.exp_string2

    def test_repr(self) -> None:
        assert repr(self.schedules1) == self.exp_string1
        assert repr(self.schedules2) == self.exp_string2
