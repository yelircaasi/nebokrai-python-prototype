import pytest

from planager.entity.base.calendar import Calendar
from planager.entity.base.project import Project
from planager.entity.container.roadmaps import Roadmaps
from planager.operator.planner import Planner


config1 = ...
config2 = ...
config3 = ...

calendar1 = Calendar()
calendar2 = Calendar()
calendar3 = Calendar()

project1 = Project()
project2 = Project()
project3 = Project()
project4 = Project()
project5 = Project()
project6 = Project()

roadmaps1 = Roadmaps()
roadmaps2 = Roadmaps()
roadmaps3 = Roadmaps()

clusters1 = []
clusters2 = []
clusters3 = []

subplan1 = {}
subplan2 = {}
subplan3 = {}
subplan4 = {}
subplan5 = {}
subplan6 = {}
subplan7 = {}
subplan8 = {}
subplan9 = {}


class PlannerTest:
    def __init__(self) -> None:
        ...
   
    def test_init(self) -> None:
        assert True

    def test_call(self) -> None:
        assert True

    def test_get_subplan_from_project(self) -> None:
        assert True

    def test_cluster_task_ids(self) -> None:
        assert True

    def allocate_in_time(self) -> None:
        assert True

    

