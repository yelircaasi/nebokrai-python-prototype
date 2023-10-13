from typing import Any, NamedTuple


class RoadmapID(NamedTuple):
    """
    Unique identifier for a roadmap, containing a roadmap code and several utility functions
      to facilitate creation and comparison of project and task IDs.
    """

    roadmap: str

    def project_id(self, project_code: str) -> "ProjectID":
        return ProjectID(self.roadmap, project_code)

    def task_id(self, project_code: str, task_code: str) -> "TaskID":
        return TaskID(self.roadmap, project_code, task_code)

    def __contains__(self, __id: Any) -> bool:
        if isinstance(__id, (RoadmapID, ProjectID)):
            return self.roadmap == __id.roadmap
        return False

    def __str__(self) -> str:
        # return f"RoadmapID('{self.roadmap}')"
        return self.roadmap

    def __repr__(self) -> str:
        return self.__str__()


class ProjectID(NamedTuple):
    """
    Unique identifier for a project, containing a roadmap code, and project code, and several
      utility functions to facilitate creation and comparison of roadmap and task IDs.
    """

    roadmap: str
    project: str

    @property
    def roadmap_id(self) -> RoadmapID:
        return RoadmapID(self.roadmap)

    def task_id(self, task_code: str) -> "TaskID":
        return TaskID(self.roadmap, self.project, task_code)

    def __contains__(self, __id: Any) -> bool:
        if isinstance(__id, RoadmapID):
            return self.roadmap == __id.roadmap
        if isinstance(__id, TaskID):
            return (self.roadmap == __id.roadmap) and (self.project == __id.project)
        return False

    def __str__(self) -> str:
        # return f"ProjectID('{self.roadmap}-{self.project}')"
        return f"{self.roadmap}-{self.project}"

    def __repr__(self) -> str:
        return self.__str__()


class TaskID(NamedTuple):
    """
    Unique identifier for a project, containing a roadmap code, and project code, a task code,
      and several utility functions to facilitate creation and comparison of roadmap and project
      IDs.
    """

    roadmap: str
    project: str
    task: str

    @property
    def roadmap_id(self) -> RoadmapID:
        return RoadmapID(self.roadmap)

    @property
    def project_id(self) -> ProjectID:
        return ProjectID(self.roadmap, self.project)

    def __contains__(self, __id: Any) -> bool:
        if isinstance(__id, RoadmapID):
            return self.roadmap == __id.roadmap
        if isinstance(__id, ProjectID):
            return (self.roadmap == __id.roadmap) and (self.project == __id.project)
        return False

    def __str__(self) -> str:
        # return f"TaskID('{self.roadmap}-{self.project}-{self.task}')"
        return f"{self.roadmap}-{self.project}-{self.task}"

    def __repr__(self) -> str:
        return self.__str__()
