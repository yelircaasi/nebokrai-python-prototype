from taskager import entities
from taskager.operators.task_patcher import TaskPatcher
from taskager.config import config


class Taskmaker:
    def __init__(self, config):
        ...
        self.patch_task = TaskPatcher(config)

    def __call__(
        
            self, 
            projects: entities.Task, 
            task_patch: entities.taskPatch
        
        ) -> entities.task:
        #tasks = get_tasks_from_projects(projects)
        task = self.patch_task(self.config, task, task_patch)
        return task