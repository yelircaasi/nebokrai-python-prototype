from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

from planager.config import _Config as ConfigType
from planager.config import config
from planager.util.algorithm.planning import SubplanType
from planager.util.data.norg import norg_util as norg
from planager.util.data.norg.norg_util import Norg
from planager.util.datetime_extensions import PDate

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
