from pathlib import Path

import pytest

from planager.entity.base.roadmap import Roadmap
from planager.entity.container.projects import Projects


class RoadmapTest:
    roadmap1 = Roadmap(name="", roadmap_id="", projects=Projects())
    roadmap2 = Roadmap(name="", roadmap_id="", projects=Projects())

    exp_string1 = "\n" "\n" "\n" "\n"
    exp_string2 = "\n" "\n" "\n" "\n"

    def test_init(self) -> None:
        assert self.roadmap1
        assert self.roadmap2

    def test_from_norg_path(self) -> None:
        path1 = Path("")
        path2 = Path("")

        assert Roadmap.from_norg_path(path1) == self.roadmap1
        assert Roadmap.from_norg_path(path2) == self.roadmap2

    def test_pretty(self) -> None:
        assert self.roadmap1.pretty() == self.exp_string1
        assert self.roadmap2.pretty() == self.exp_string2

    def test_str(self) -> None:
        assert str(self.roadmap1) == self.exp_string1
        assert str(self.roadmap2) == self.exp_string2

    def test_repr(self) -> None:
        assert str(self.roadmap1) == self.exp_string1
        assert str(self.roadmap2) == self.exp_string2

    def test_iter(self) -> None:
        assert list(self.roadmap1) == []
        assert list(self.roadmap2) == []
