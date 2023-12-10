from typing import NamedTuple


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

    def __contains__(self, __id: object) -> bool:
        if isinstance(__id, (RoadmapID, ProjectID, TaskID)):
            return self.roadmap == __id.roadmap
        raise TypeError(
            "RoadmapID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
            f"not type '{type(__id)}' (value: '{__id}')."
        )

    def __str__(self) -> str:
        return self.roadmap

    def __repr__(self) -> str:
        return f"RoadmapID('{self.roadmap}')"


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

    @classmethod
    def from_string(cls, s: str) -> "ProjectID":
        return cls(*s.split("-"))

    def __contains__(self, __id: object) -> bool:
        if isinstance(__id, RoadmapID):
            return self.roadmap == __id.roadmap
        if isinstance(__id, (ProjectID, TaskID)):
            return (self.roadmap == __id.roadmap) and (self.project == __id.project)
        raise TypeError(
            "ProjectID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
            f"not type '{type(__id)}' (value: '{__id}')."
        )

    def __str__(self) -> str:
        return f"{self.roadmap}-{self.project}"

    def __repr__(self) -> str:
        return f"ProjectID('{self.roadmap}-{self.project}')"


class TaskID(NamedTuple):
    """
    Unique identifier for a project, containing a roadmap code, and project code, a task code,
      and several utility functions to facilitate creation and comparison of roadmap and project
      IDs.
    """

    roadmap: str
    project: str
    task: str

    @classmethod
    def from_string(cls, s: str) -> "TaskID":
        segments = s.split("-")
        assert len(segments) == 3, f"Invalid input to TaskID.from_string: {segments}"
        return cls(*segments)

    @property
    def roadmap_id(self) -> RoadmapID:
        return RoadmapID(self.roadmap)

    @property
    def project_id(self) -> ProjectID:
        return ProjectID(self.roadmap, self.project)

    def __contains__(self, __id: object) -> bool:
        if isinstance(__id, RoadmapID):
            return self.roadmap == __id.roadmap
        if isinstance(__id, ProjectID):
            return (self.roadmap == __id.roadmap) and (self.project == __id.project)
        if isinstance(__id, TaskID):
            return (
                (self.roadmap == __id.roadmap)
                and (self.project == __id.project)
                and (self.task == __id.task)
            )
        raise TypeError(
            "TaskID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
            f"not type '{type(__id)}' (value: '{__id}')."
        )

    def __str__(self) -> str:
        return f"{self.roadmap}-{self.project}-{self.task}"

    def __repr__(self) -> str:
        return f"TaskID('{self.roadmap}-{self.project}-{self.task}')"
