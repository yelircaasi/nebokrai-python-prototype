class Logs:
    """
    Holds entire history of everything tracked.
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

    @property
    def summary(self) -> str:
        return "Logs.summary property is not yet implemented."

    def dashboard(self) -> str:
        return "Dashboard not yet implemented!"

    def __str__(self) -> str:
        return "need to implement this"

    def __repr__(self) -> str:
        return self.__str__()
