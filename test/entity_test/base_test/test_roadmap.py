from pathlib import Path

import pytest
from planager.entity.base.project import Project

from planager.entity.base.roadmap import Roadmap
from planager.entity.container.projects import Projects


class RoadmapTest:
    def test_init(self) -> None:
        roadmap_default = Roadmap("", roadmap_id="", projects=Projects())
        roadmap_custom = Roadmap("", roadmap_id="", projects=Projects())

        assert roadmap_default.name == ...
        assert roadmap_default.roadmap_id == ...
        assert roadmap_default._projects == ...
        assert roadmap_default.updated == ...
        assert roadmap_default.updated == ...
        assert roadmap_default.categories == ...

        assert roadmap_custom.name == ...
        assert roadmap_custom.roadmap_id == ...
        assert roadmap_custom._projects == ...
        assert roadmap_custom.updated == ...
        assert roadmap_custom.categories == ...

    # def test_from_norg_path(self) -> None:
    #     path1 = Path()
    #     path2 = Path()
    #     path3 = Path()

    #     roadmap1 = Roadmap.from_norg_path(path1, "Roadmap 1")
    #     roadmap2 = Roadmap.from_norg_path(path2, "Roadmap 2")
    #     roadmap3 = Roadmap.from_norg_path(path3, "Roadmap 3")

    #     exp1 = Roadmap("", roadmap_id="", projects=Projects())
    #     exp2 = Roadmap("", roadmap_id="", projects=Projects())
    #     exp3 = Roadmap("", roadmap_id="", projects=Projects())

    #     assert roadmap1 == exp1
    #     assert roadmap2 == exp2
    #     assert roadmap3 == exp3

    def test_pretty(self) -> None:
        roadmap = Roadmap("", roadmap_id="", projects=Projects())
        exp = ()
        assert roadmap.pretty() == exp

    def test_str(self) -> None:
        roadmap = Roadmap("", roadmap_id="", projects=Projects())
        exp = ()
        assert str(roadmap) == exp

    def test_repr(self) -> None:
        roadmap = Roadmap("", roadmap_id="", projects=Projects())
        exp = ()
        assert repr(roadmap) == exp

    def test_iter(self) -> None:
        roadmap = Roadmap("", roadmap_id="", projects=Projects())
        projects: list[Project] = []
        assert list(roadmap) == projects
