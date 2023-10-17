from ..config import Config
from ..util import PathManager


class Tracker:
    emptysquare: str = '□'
    square: str = '■'
    emptycircle: str = '○'
    circle: str = '●'
    emptydiamond: str = '◇'
    diamond: str = '◆'
    block1: str = '▁' # Lower one eighth block
    block2: str = '▂' #Lower one quarter block
    block3: str = '▃' #Lower three eighths block
    block4: str = '▄' #Lower half block
    block5: str = '▅' #Lower five eighths block
    block6: str = '▆' #Lower three quarters block
    block7: str = '▇' #Lower seven eighths block
    block8: str = '█' #Full block
    shade1: str = '░'
    shade2: str = '▒'
    shade3: str = '▓'

    def __init__(self, config: Config, pathmanager: PathManager) -> None:
        self.config = config
        self.pathmanager = pathmanager
        ...

    def from_dict(cls, config: Config, pathmanager: PathManager, tracking_dict) -> "Tracker":
        ...

    def record(self) -> None:
        ...

    def record_interactive(self) -> None:
        ...
    
    def dashboard(self) -> str:
        ...
