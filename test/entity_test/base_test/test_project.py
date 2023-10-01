from pathlib import Path
from typing import Any

import pytest

from planager.entity.base.project import Project
from planager.entity.base.task import Task
from planager.util.pdatetime.pdate import PDate


class ProjectTest:
    def test_init(self) -> None:
        project_default = Project("", ("", ""))
        project_custom = Project("", ("", ""))

        assert project_default.name == ...
        assert project_default.project_id == ...
        assert project_default.tasks == ...
        assert project_default.priority == ...
        assert project_default.start == ...
        assert project_default.end == ...
        assert project_default.interval == ...
        assert project_default.cluster_size == ...
        assert project_default.duration == ...
        assert project_default.tags == ...
        assert project_default.description == ...
        assert project_default.notes == ...
        assert project_default.path == ...
        assert project_default.dependencies == ...
        assert project_default.categories == ...

        assert project_custom.name == ...
        assert project_custom.project_id == ...
        assert project_custom.tasks == ...
        assert project_custom.priority == ...
        assert project_custom.start == ...
        assert project_custom.end == ...
        assert project_custom.interval == ...
        assert project_custom.cluster_size == ...
        assert project_custom.duration == ...
        assert project_custom.tags == ...
        assert project_custom.description == ...
        assert project_custom.notes == ...
        assert project_custom.path == ...
        assert project_custom.dependencies == ...
        assert project_custom.categories == ...

    def test_from_dict(self) -> None:
        project_dict: dict[str, Any] = {}
        roadmap_id = ""
        project = Project.from_dict(roadmap_id, project_dict)
        exp = Project("", ("", ""))

        assert project == exp

    def test_from_norg_path(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        project1 = Project.from_norg_path(path1, "Project 1")
        project2 = Project.from_norg_path(path2, "Project 2")
        project3 = Project.from_norg_path(path3, "Project 3")

        exp1 = Project("", ("", ""))
        exp2 = Project("", ("", ""))
        exp3 = Project("", ("", ""))

        assert project1 == exp1
        assert project2 == exp2
        assert project3 == exp3

    def test_from_roadmap_item(self) -> None:
        roadmap_str = ""
        project = Project.from_roadmap_item(roadmap_str, "", Path(""))
        exp = Project("", ("", ""))

        assert project == exp

    def test_copy(self) -> None:
        project = Project("", ("", ""))
        copy = project.copy()

        assert id(project) != id(copy)
        assert project.__dict__ == copy.__dict__

    def test_get_start(self) -> None:
        project = Project("", ("", ""))
        start = PDate(2100, 1, 1)

        assert project.get_start() == start

    def test_get_end(self) -> None:
        project = Project("", ("", ""))
        end = PDate(2100, 1, 1)

        assert project.get_end() == end

    def test_task_ids(self) -> None:
        project = Project("", ("", ""))
        task_ids: list[tuple[str, str, str]] = []

        assert project.task_ids == task_ids

    def test_pretty(self) -> None:
        project = Project("", ("", ""))
        exp = ()
        assert project.pretty() == exp

    def test_iter(self) -> None:
        project = Project("", ("", ""))

    def test_getitem(self) -> None:
        project = Project("", ("", ""))
        task = Task("", ("", "", ""))

        assert project[("", "", "")] == task

    def test_str(self) -> None:
        project = Project("", ("", ""))
        exp = ()
        assert str(project) == exp

    def test_repr(self) -> None:
        project = Project("", ("", ""))
        exp = ()
        assert repr(project) == exp
