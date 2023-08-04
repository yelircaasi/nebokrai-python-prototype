from pathlib import Path
import pytest

from planager.entity.base.roadmap import Roadmap
from planager.entity.container.projects import Projects
from planager.entity.container.roadmaps import Roadmaps


class RoadmapsTest:
    roadmaps1 = Roadmaps()
    roadmaps2 = Roadmaps()

    exp_string1 = "\n" "\n" ""
    exp_string2 = "\n" "\n" ""

    def test_init(self) -> None:
        assert self.roadmaps1
        assert self.roadmaps2

    def test_from_norg_workspace(self) -> None:
        path1 = Path("")
        path2 = Path("")

        roadmaps3 = Roadmaps.from_norg_workspace(path1)
        roadmaps4 = Roadmaps.from_norg_workspace(path2)

        assert roadmaps3 == self.roadmaps1
        assert roadmaps4 == self.roadmaps2

    def test_open_projects_norg(self) -> None:
        exp1 = Projects()
        exp2 = Projects()

        rm1 = Roadmaps([r.copy() for r in self.roadmaps1])
        rm2 = Roadmaps([r.copy() for r in self.roadmaps2])

        rm1.open_projects_norg()
        rm2.open_projects_norg()

        assert rm1 == exp1
        assert rm2 == exp2

    def test_get_projects(self) -> None:
        exp1 = Projects()
        exp2 = Projects()

        assert self.roadmaps1.get_projects() == exp1
        assert self.roadmaps2.get_projects() == exp2

    def test_pretty(self) -> None:
        assert self.roadmaps1.pretty() == self.exp_string1
        assert self.roadmaps2.pretty() == self.exp_string2

    def test_iter(self) -> None:
        assert list(self.roadmaps1) == []
        assert list(self.roadmaps2) == []

    def test_getitem(self) -> None:
        assert self.roadmaps1[...] == ...
        assert self.roadmaps2[...] == ...

    def test_setitem(self) -> None:
        rm = Roadmaps()

        exp = Roadmaps()

        rm[3] = Roadmap("", "", Projects())
        rm[1] = Roadmap("", "", Projects())

        assert rm == exp

    def test_str(self) -> None:
        assert str(self.roadmaps1) == self.exp_string1
        assert str(self.roadmaps2) == self.exp_string2

    def test_repr(self) -> None:
        assert repr(self.roadmaps1) == self.exp_string1
        assert repr(self.roadmaps2) == self.exp_string2
