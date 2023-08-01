import pytest

from planager.entity.container.routines import Routines
from planager.entity.base.routine import Routine


class RoutinesTest:
    routines1 = Routines()
    routines2 = Routines()

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
        assert self.routines1
        assert self.routines2

    def test_from_norg_workspace(self) -> None:
        routines3 = Routines.from_norg_workspace()
        routines4 = Routines.from_norg_workspace()

        assert routines3 == self.routines1
        assert routines4 == self.routines2

    def test_add(self) -> None:
        routines4 = Routines()
        routines5 = Routines()

        exp4 = Routines()
        exp5 = Routines()

        routines4.add(Routine())
        routines5.add(Routine())

        assert routines4 == exp4
        assert routines5 == exp5

    def test_pretty(self) -> None:
        assert self.routines1.pretty() == self.exp_string1
        assert self.routines2.pretty() == self.exp_string2
        
    def test_iter(self) -> None:
        assert list(self.routines1) == []
        assert set(self.routines2) == {}

    def test_getitem(self) -> None:
        assert self.routines1[...] == ...
        assert self.routines2[...] == ...

    def test_str(self) -> None:
        assert str(self.routines1) == self.exp_string1
        assert str(self.routines2) == self.exp_string2

    def test_repr(self) -> None:
        assert repr(self.routines1) == self.exp_string1
        assert repr(self.routines2) == self.exp_string2
