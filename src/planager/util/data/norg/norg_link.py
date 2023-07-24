from pathlib import Path
import re
from typing import Optional, Union

from ...regex import Regexes


class NorgLink:
    re_namefirst: re.Pattern = Regexes.link_namefirst
    re_namelast: re.Pattern = Regexes.link_namelast

    def __init__(self, name: str, link: Optional[str] = None) -> None:
        self.name: str = name
        self.link: Optional[str] = link

    @classmethod
    def from_string(cls, raw_string) -> "NorgLink":
        name = raw_string
        link = None

        s = re.search(NorgLink.re_namefirst, raw_string)
        if s:
            name, link = s.groups()
        if not link:
            s = re.search(NorgLink.re_namelast, raw_string)
            if s:
                name, link = s.groups()

        return cls(name, link=link)

    def __str__(self) -> str:
        return self.name

    def __bool__(self) -> bool:
        return bool(self.link)

    def as_norg(self) -> str:
        if not self.link:
            return self.name
        else:
            return f"[{self.name}]{{{self.link}}}"

    @property
    def path(self) -> Union[Path, None]:
        if self.link:
            return Path(self.link.strip(":$/"))
        else:
            return None
