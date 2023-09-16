from typing import Dict, List, Tuple, Union
import pytest

from planager.entity.base.calendar import Calendar
from planager.entity.base.plan import Plan
from planager.entity.base.project import Project
from planager.entity.container.projects import Projects
from planager.entity.container.roadmaps import Roadmaps
from planager.operator.planner import Planner
from planager.util import PDate


class PlannerTest:
    # def test_init(self) -> None:

    def test_call(self) -> None:
        assert True

    def test_get_subplan_from_project(self) -> None:
        planner = Planner()
        project = Project()
        subplan = {}

        assert planner.get_subplan_from_project(project) == subplan

    def test_cluster_task_ids(self) -> None:
        task_ids = []
        subplan = {}

        exp1 = []
        exp2 = []
        exp3 = []
        exp4 = []
        exp7 = []  # length of list
        exp9 = []  # larger

        assert exp1 == Planner.cluster_task_ids(task_ids, 1)
        assert exp1 == Planner.cluster_task_ids(task_ids, 2)
        assert exp1 == Planner.cluster_task_ids(task_ids, 3)
        assert exp1 == Planner.cluster_task_ids(task_ids, 4)
        assert exp1 == Planner.cluster_task_ids(task_ids, 7)
        assert exp1 == Planner.cluster_task_ids(task_ids, 9)

    def test_allocate_in_time(self) -> None:
        """
        Cases:
        1) cluster length 1
        2) end
        3) interval
        """
        clusters1 = []
        clusters3 = []
        clusters7 = []
        clusters12 = []

        project_int1 = Project()
        project_int3 = Project()
        project_int5 = Project()

        project_end4 = Project()
        project_end12 = Project()
        project_end60 = Project()

        exp1 = {}
        exp3_int1 = {}
        exp3_int3 = {}
        exp3_int5 = {}
        exp3_end4 = {}
        exp3_end12 = {}
        exp3_end60 = {}
        exp7_int1 = {}
        exp7_int3 = {}
        exp7_int5 = {}
        exp7_end4 = {}
        exp7_end12 = {}
        exp7_end60 = {}
        exp12_int1 = {}
        exp12_int3 = {}
        exp12_int5 = {}
        exp12_end4 = {}
        exp12_end12 = {}
        exp12_end60 = {}

        assert Planner.allocate_in_time(clusters1, project_end60) == exp1
        assert Planner.allocate_in_time(clusters3, project_int1) == exp3_int1
        assert Planner.allocate_in_time(clusters3, project_int3) == exp3_int3
        assert Planner.allocate_in_time(clusters3, project_int5) == exp3_int5
        assert Planner.allocate_in_time(clusters3, project_end4) == exp3_end4
        assert Planner.allocate_in_time(clusters3, project_end12) == exp3_end12
        assert Planner.allocate_in_time(clusters3, project_end60) == exp3_end60
        assert Planner.allocate_in_time(clusters7, project_int1) == exp7_int1
        assert Planner.allocate_in_time(clusters7, project_int3) == exp7_int3
        assert Planner.allocate_in_time(clusters7, project_int5) == exp7_int5
        assert Planner.allocate_in_time(clusters7, project_end4) == exp7_end4
        assert Planner.allocate_in_time(clusters7, project_end12) == exp7_end12
        assert Planner.allocate_in_time(clusters7, project_end60) == exp7_end60
        assert Planner.allocate_in_time(clusters12, project_int1) == exp12_int1
        assert Planner.allocate_in_time(clusters12, project_int3) == exp12_int3
        assert Planner.allocate_in_time(clusters12, project_int5) == exp12_int5
        assert Planner.allocate_in_time(clusters12, project_end4) == exp12_end4
        assert Planner.allocate_in_time(clusters12, project_end12) == exp12_end12
        assert Planner.allocate_in_time(clusters12, project_end60) == exp12_end60

    # def test_get_end_from_id(self) -> None:
    #     assert True

    def test_enforce_precedence_constraints(self) -> None:
        projects = Projects()
        planner = Planner()
        plan_valid = Plan()
        plan_invalid = Plan()

        assert planner.enforce_precedence_constraints(plan_valid, projects) is None
        with pytest.raises(ValueError) as excinfo:
            planner.enforce_precedence_constraints(plan_invalid, projects)
        # TODO: fix error
        assert (
            str(excinfo.value)
            == "Task {'<>'.join(task_id)} assigned to {plan_date}, but earliest permissible date is {earliest_date}. Please adjust the declaration and run the derivation again. \n  Limiting dependency: {'<>'.join(limiting_dependency)}."
        )
