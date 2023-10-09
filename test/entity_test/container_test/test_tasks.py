from pathlib import Path
from typing import Any

import pytest

from planager.entity.base.task import Task
from planager.entity.container.roadmaps import Roadmaps
from planager.entity.container.tasks import Tasks


class TasksTest:
    # def test_init(self) -> None:

    def test_from_string_iterable(self) -> None:
        tasks_list = Tasks.from_string_iterable(["", ""], ("", ""), "")
        tasks_tuple = Tasks.from_string_iterable(["", ""], ("", ""), "")
        exp_list = Tasks()
        exp_tuple = Tasks()

        assert tasks_list == exp_list
        assert tasks_tuple == exp_tuple

    def test_from_dict(self) -> None:
        tasks_dict_list: list[dict[str, Any]] = [{}]
        project_id = ("", "")
        tasks = Tasks.from_dict(project_id, tasks_dict_list)
        exp = Tasks()

        assert tasks == exp

    def test_from_norg_path(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        tasks1 = Tasks.from_norg_path(path1, ("", ""), "")
        tasks2 = Tasks.from_norg_path(path2, ("", ""), "")
        tasks3 = Tasks.from_norg_path(path3, ("", ""), "")

        exp1 = Tasks()
        exp2 = Tasks()
        exp3 = Tasks()

        assert tasks1 == exp1
        assert tasks2 == exp2
        assert tasks3 == exp3

    def test_from_roadmaps(self) -> None:
        roadmaps = Roadmaps()
        tasks = Tasks.from_roadmaps(roadmaps)
        exp = Tasks()
        assert tasks == exp

    def test_add(self) -> None:
        tasks = Tasks()
        task = Task("", ("", "", ""))
        exp = Tasks()

        tasks.add(Task("", ("", "", "")))

        assert tasks == exp

    def test_task_ids(self) -> None:
        tasks = Tasks()
        task_ids = [(), (), ()]

        assert tasks.task_ids == task_ids

    def test_pretty(self) -> None:
        tasks = Tasks()
        exp = ()

        assert tasks.pretty() == exp

    def test_iter(self) -> None:
        tasks = Tasks()
        exp: list[Task] = []

        assert list(tasks) == []

    def test_getitem(self) -> None:
        tasks = Tasks()
        task_id = ("", "", "")
        task = Task("", ("", "", ""))

        assert tasks[task_id] == task

    def test_str(self) -> None:
        tasks = Tasks()
        exp = ()
        assert str(tasks) == exp

    def test_repr(self) -> None:
        tasks = Tasks()
        exp = ()
        assert repr(tasks) == exp
