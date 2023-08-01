import pytest
from planager.entity.base.project import Project

from planager.entity.container.projects import Projects
from planager.entity.patch.task_patch import TaskPatches


class ProjectsTest:
    projects1 = Projects()
    projects2 = Projects()

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
        assert self.projects1
        assert self.projects2

    def test_projects(self) -> None:
        exp1 = []
        exp2 = []

        assert self.projects1.projects == exp1
        assert self.projects2.projects == exp2

    def test_projects_setter(self) -> None:
        projs1 = Projects([p.copy() for p in self.projects1])
        projs2 = Projects([p.copy() for p in self.projects2])

        exp1 = Projects()
        exp2 = Projects()

        projs1.projects == ... # NEED TO TEST FOR AN ERROR HERE
        projs2.projects == ...

        assert projs1 == exp1
        assert projs2 == exp2

    def test_add(self) -> None:
        projs1 = Projects([p.copy() for p in self.projects1])
        projs2 = Projects([p.copy() for p in self.projects2])

        exp1 = Projects()
        exp2 = Projects()

        projs1.projects == ... # NEED TO TEST FOR AN ERROR HERE
        projs2.projects == ...

        assert projs1 == exp1
        assert projs2 == exp2

    def test_get_tasks(self) -> None:
        assert True

    def test_patch_tasks(self) -> None:
        projs1 = Projects([p.copy() for p in self.projects1])
        projs2 = Projects([p.copy() for p in self.projects2])

        patches1 = TaskPatches()
        patches2 = TaskPatches()

        exp1 = Projects()
        exp2 = Projects()

        projs1.patch_tasks(patches1)
        projs2.patch_tasks(patches2)

        assert projs1 == exp1
        assert projs2 == exp2

    def test_order_by_dependency(self) -> None:
        projs1 = Projects([p.copy() for p in self.projects1])
        projs2 = Projects([p.copy() for p in self.projects2])

        patches1 = TaskPatches()
        patches2 = TaskPatches()

        exp1 = Projects()
        exp2 = Projects()

        projs1.order_by_dependency(patches1)
        projs2.order_by_dependency(patches2)

        assert projs1 == exp1
        assert projs2 == exp2

    def test_pretty(self) -> None:
        assert self.projects1.pretty() == self.exp_string1
        assert self.projects2.pretty() == self.exp_string2

    def test_iter(self) -> None:
        assert list(self.projects1) == []
        assert set(self.projects2) == {}

    def test_getitem(self) -> None:
        assert self.projects1[...] == ...
        assert self.projects2[...] == ...

    def test_setitem(self) -> None:
        projs1 = Projects([p.copy() for p in self.projects1])
        projs2 = Projects([p.copy() for p in self.projects2])

        exp1 = Projects()
        exp2 = Projects()

        projs1[...] == ...
        projs2[...] == ...

        assert projs1 == exp1
        assert projs2 == exp2

    def test_str(self) -> None:
        assert str(self.projects1) == self.exp_string1
        assert str(self.projects2) == self.exp_string2

    def test_repr(self) -> None:
        assert repr(self.projects1) == self.exp_string1
        assert repr(self.projects2) == self.exp_string2
