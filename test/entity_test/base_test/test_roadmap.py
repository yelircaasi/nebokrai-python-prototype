from pathlib import Path

import pytest

from planager.entity.base.roadmap import Roadmap


class RoadmapTest:
    roadmap1 = Roadmap()
    roadmap2 = Roadmap()

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
        assert self.roadmap1
        assert self.roadmap2

    def test_from_norg_path(self) -> None:
        path1 = Path("")
        path2 = Path("")

        assert Roadmap.from_norg_path(path1) == self.roadmap1
        assert Roadmap.from_norg_path(path2) == self.roadmap2

    def test_pretty(self) -> None:
        assert self.roamdmap1.pretty() == self.exp_string1
        assert self.roamdmap2.pretty() == self.exp_string2

    def test_str(self) -> None:
        assert str(self.roamdmap1) == self.exp_string1
        assert str(self.roamdmap2) == self.exp_string2

    def test_repr(self) -> None:
        assert str(self.roamdmap1) == self.exp_string1
        assert str(self.roamdmap2) == self.exp_string2

    def test_iter(self) -> None:
        assert list(self.roadmap1) == []
        assert list(self.roadmap2) == []
