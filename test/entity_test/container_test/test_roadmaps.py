from pathlib import Path

import pytest

from planager.entity.base.roadmap import Roadmap
from planager.entity.container.projects import Projects
from planager.entity.container.roadmaps import Roadmaps


class RoadmapsTest:
    def test_init(self) -> None:
        roadmaps = Roadmaps()
        roadmap_dict: dict[str, Roadmap] = {}
        workspace_dir = Path()

        assert roadmaps.workspace_dir == workspace_dir
        assert roadmaps._roadmaps == roadmap_dict

    def test_from_dict(self) -> None:
        roadmaps_dict: dict[str, Roadmap] = {}
        roadmaps = Roadmaps.from_dict(roadmaps_dict)
        exp = Roadmaps()

        assert roadmaps == exp

    def test_from_norg_workspace(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        roadmaps1 = Roadmaps.from_norg_workspace(path1)
        roadmaps2 = Roadmaps.from_norg_workspace(path2)
        roadmaps3 = Roadmaps.from_norg_workspace(path3)

        exp1 = Roadmaps()
        exp2 = Roadmaps()
        exp3 = Roadmaps()

        assert roadmaps1 == exp1
        assert roadmaps2 == exp2
        assert roadmaps3 == exp3

    # def test_open_projects_norg(self) -> None:

    def test_projects(self) -> None:
        roadmaps = Roadmaps()
        projects = Projects()

        assert roadmaps.projects == projects

    def test_pretty(self) -> None:
        roadmaps = Roadmaps()
        exp = ()
        assert roadmaps.pretty() == exp

    def test_iter(self) -> None:
        roadmaps_list: list[Roadmap] = []
        roadmaps = Roadmaps()
        assert roadmaps_list == list(roadmaps)

    def test_getitem(self) -> None:
        roadmaps = Roadmaps()
        roadmap = Roadmap("", roadmap_id="", projects=Projects())
        roadmap_id = ""

        assert roadmaps[roadmap_id] == roadmap

    def test_setitem(self) -> None:
        roadmaps = Roadmaps()
        roadmap = Roadmap("", roadmap_id="", projects=Projects())
        roadmap_id = ""

        roadmaps[roadmap_id] = roadmap

        assert roadmaps[roadmap_id] == roadmap

    def test_str(self) -> None:
        roadmaps = Roadmaps()
        exp = ()
        assert str(roadmaps) == exp

    def test_repr(self) -> None:
        roadmaps = Roadmaps()
        exp = ()
        assert repr(roadmaps) == exp
