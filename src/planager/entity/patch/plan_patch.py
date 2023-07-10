from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

from ...config import _Config as ConfigType
from ...config import config
from ...util.algorithm.planning import SubplanType
from ...util.data.norg import norg_util as norg
from ...util.data.norg.norg_util import Norg
from ...util.pdatetime import PDate
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
