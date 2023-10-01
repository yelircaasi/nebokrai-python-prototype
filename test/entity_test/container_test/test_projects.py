from typing import Any
import pytest
from planager.entity.base.project import Project

from planager.entity.container.projects import Projects
from planager.entity.container.tasks import Tasks
from planager.entity.patch.task_patch import TaskPatches
from planager.util.pdatetime.pdate import PDate


class ProjectsTest:
    # def test_init(self) -> None:

    def test_from_dict(self) -> None:
        projects_dict: dict[str, Any] = {}
        projects = Projects.from_dict(projects_dict)
        exp = Projects()

        assert projects == exp

    def test_add(self) -> None:
        projects = Projects()
        project = Project("", ("", ""))
        exp = Projects()

        projects.add(project)

        assert projects == exp

    def test_tasks(self) -> None:
        projects = Projects()
        tasks = Tasks()
        assert projects.tasks == tasks

    def test_get_tasks(self) -> None:
        projects = Projects()
        tasks = Tasks()
        assert projects._get_tasks() == tasks

    def test_patch_tasks(self) -> None:
        projects = Projects()
        task_patches = TaskPatches()
        exp = Projects()

        projects.patch_tasks(task_patches)

        assert projects == exp

    # def test_make_dependency_ordered_lists(self) -> None:
    #     projs1 = Projects([p.copy() for p in self.projects1])
    #     projs2 = Projects([p.copy() for p in self.projects2])

    #     patches1 = TaskPatches()
    #     patches2 = TaskPatches()

    #     exp1 = Projects()
    #     exp2 = Projects()

    #     projs1.order_by_dependency()
    #     projs2.order_by_dependency()

    #     assert projs1 == exp1
    #     assert projs2 == exp2

    def test_pretty(self) -> None:
        projects = Projects()
        exp = ()
        assert projects.pretty() == exp

    def test_iter(self) -> None:
        projects = Projects()
        exp: list[Project] = []
        assert list(projects) == exp

    def test_getitem(self) -> None:
        projects = Projects()
        proj_id = ("", "")
        exp: Project = Project("", proj_id)
        assert projects[proj_id] == exp

    def test_setitem(self) -> None:
        projects = Projects()
        project = Project("", ("", ""))
        proj_id = ("", "")

        projects[proj_id] = project

        assert projects[proj_id] == project

    def test_str(self) -> None:
        projects = Projects()
        exp = ()
        assert str(projects) == exp

    def test_repr(self) -> None:
        projects = Projects()
        exp = ()
        assert str(projects) == exp
