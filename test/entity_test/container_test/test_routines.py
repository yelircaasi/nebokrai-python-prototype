from pathlib import Path
from typing import Any

import pytest

from planager.entity.base.routine import Routine
from planager.entity.container.routines import Routines
from planager.util.pdatetime.ptime import PTime


class RoutinesTest:
    def test_init_and_from_norg_workspace(self) -> None:
        path = Path()
        routines = Routines.from_norg_workspace(path)
        exp = Routines()

        assert routines == exp

    def test_from_dict(self) -> None:
        routines_dict: dict[str, Any] = {}
        routines = Routines.from_dict(routines_dict)
        exp = Routines()

        assert routines == exp

    def test_add(self) -> None:
        routines = Routines()
        routine = Routine("", PTime())
        exp = Routines()

        routines.add(routine)

        assert routines == exp

    def test_pretty(self) -> None:
        routines = Routines()
        exp = ()
        assert routines.pretty() == exp

    def test_iter(self) -> None:
        routines = Routines()
        routine_list: list[Routine] = []

        assert list(routines) == routine_list

    def test_getitem(self) -> None:
        routines = Routines()
        routine = Routine("", PTime())
        routine_id = ""

        assert routines[routine_id] == routine

    def test_str(self) -> None:
        routines = Routines()
        exp = ()
        assert str(routines) == exp

    def test_repr(self) -> None:
        routines = Routines()
        exp = ()
        assert repr(routines) == exp
