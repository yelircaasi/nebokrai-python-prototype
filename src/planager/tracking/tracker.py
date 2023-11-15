from ..configuration import path_manager


class Tracker:
    """
    Responsible for entry of tasks completed, as well as for summary and
      display.
    """

    emptysquare: str = "□"
    square: str = "■"
    emptycircle: str = "○"
    circle: str = "●"
    emptydiamond: str = "◇"
    diamond: str = "◆"
    block1: str = "▁"  # Lower one eighth block
    block2: str = "▂"  # Lower one quarter block
    block3: str = "▃"  # Lower three eighths block
    block4: str = "▄"  # Lower half block
    block5: str = "▅"  # Lower five eighths block
    block6: str = "▆"  # Lower three quarters block
    block7: str = "▇"  # Lower seven eighths block
    block8: str = "█"  # Full block
    shade1: str = "░"
    shade2: str = "▒"
    shade3: str = "▓"

    def __init__(self, tracking_dict: dict) -> None:
        self.path_manager = path_manager
        self.raw = tracking_dict  # change later

    @classmethod
    def from_dict(cls, tracking_dict: dict) -> "Tracker":
        return cls(tracking_dict)

    def record(self) -> None:
        ...

    def record_interactive(self) -> None:
        ...

    def dashboard(self) -> str:
        return "Not yet implemented!"
