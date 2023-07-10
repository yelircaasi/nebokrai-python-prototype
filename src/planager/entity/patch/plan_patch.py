from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

from ...util import Norg, PDate
from ..container.tasks import Tasks


class PlanPatch:
    def __init__(self) -> None:
        ...


class PlanPatches:
    def __init__(self, patches: List[PlanPatch] = []) -> None:
        self.patches = patches

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "PlanPatches":
        # file = workspace_dir / "roadmaps.norg"
        # parsed = Norg.from_path(file)
        # ...
        # return cls()
        return cls()
