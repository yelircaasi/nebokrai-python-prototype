from typing import Dict, List, Tuple, Union
import pytest

from planager.entity.base.calendar import Calendar
from planager.entity.base.project import Project
from planager.entity.container.roadmaps import Roadmaps
from planager.operator.planner import Planner
from planager.util import PDate


config1 = ...
config2 = ...
config3 = ...

calendar1 = Calendar()
calendar2 = Calendar()
calendar3 = Calendar()

project1: Project = Project("Project 1", ("", "1"))
project2: Project = Project("Project 2", ("", "2"))
project3: Project = Project("Project 3", ("", "3"))
project4: Project = Project("Project 4", ("", "4"))
project5: Project = Project("Project 5", ("", "5"))
project6: Project = Project("Project 6", ("", "6"))

roadmaps1: Roadmaps = Roadmaps()
roadmaps2: Roadmaps = Roadmaps()
roadmaps3: Roadmaps = Roadmaps()

clusters1: List[List[Tuple[str, ...]]] = []
clusters2: List[List[Tuple[str, ...]]] = []
clusters3: List[List[Tuple[str, ...]]] = []

subplan1: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan2: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan3: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan4: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan5: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan6: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan7: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan8: Dict[PDate, List[Tuple[str, ...]]] = {}
subplan9: Dict[PDate, List[Tuple[str, ...]]] = {}


class PlannerTest:
    def test_init(self) -> None:
        assert True

    def test_call(self) -> None:
        assert True

    def test_get_subplan_from_project(self) -> None:
        assert True

    def test_cluster_task_ids(self) -> None:
        assert True

    def test_allocate_in_time(self) -> None:
        assert True

    # def test_get_end_from_id(self) -> None:
    #     assert True

    def test_enforce_precedence_constraints(self) -> None:
        assert True
