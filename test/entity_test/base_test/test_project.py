from pathlib import Path

import pytest

from planager.entity.base.project import Project


class ProjectTest:
    project1 = Project()
    project2 = Project()
    project3 = Project()

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
    exp_string3 = '\n'.join(
        "",
        "",
        "",
    )

    def test_init(self) -> None:
        assert True

    def test_from_norg_path(self) -> None:
        path1 = Path()
        path2 = Path()
        
        p1 = Project.from_norg_path()
        p2 = Project.from_norg_path()

        assert p1
        assert p2

    def test_from_roadmap_item(self) -> None:
        item1 = '\n'.join(
            "",
            "",
            "",
        )
        item2 = '\n'.join(
            "",
            "",
            "",
        )

        p1 = Project.from_roadmap_item()
        p2 = Project.from_roadmap_item()

    def test_copy(self) -> None:
        assert self.project1.copy()
        assert self.project2.copy()
        assert self.project3.copy()

    def test_get_start(self) -> None:
        assert self.project1
        assert self.project2
        assert self.project3

    def test_get_end(self) -> None:
        assert self.project1
        assert self.project2
        assert self.project3

    def test_task_ids(self) -> None:
        assert self.project1.task_ids
        assert self.project2.task_ids
        assert self.project3.task_ids

    def test_pretty(self) -> None:
        assert self.project1.pretty() == self.exp_string1
        assert self.project2.pretty() == self.exp_string2
        assert self.project3.pretty() == self.exp_string3

    def test_str(self) -> None:
        assert str(self.project1) == self.exp_string1
        assert str(self.project2) == self.exp_string2
        assert str(self.project3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.project1) == self.exp_string1
        assert repr(self.project2) == self.exp_string2
        assert repr(self.project3) == self.exp_string3

    def test_iter(self) -> None:
        assert list(self.project1) == []
        assert list(self.project2) == []
        assert list(self.project3) == []

    def test_getitem(self) -> None:
        assert self.self.project1[...] == ...
        assert self.self.project2[...] == ...
        assert self.self.project3[...] == ...
