from pathlib import Path
import re
from typing import Optional, Union

from ...regex import Regexes


class NorgItemHead:
    re_namefirst: re.Pattern = Regexes.link_namefirst
    # re_namelast: re.Pattern = Regexes.link_namelast

    def __init__(
        self,
        name: str,
        status: str = " ",
        link: Optional[str] = None,
        segment_string: Optional[str] = None,
    ) -> None:
        self.name: str = name
        self.link: Optional[str] = link
        self.status: Optional[str] = status
        self.segment_string: Optional[str] = segment_string
        self._path: Optional[Path] = None

    @classmethod
    def from_string(cls, raw_string: str) -> "NorgItemHead":
        name = None
        link = None
        status = " "
        segment_string = None

        s = re.search(r" ?\((.)\) (.+)", raw_string)
        if s:
            status, raw_string = s.groups()
        else:
            raise ValueError(raw_string)

        if "||" in raw_string:
            s = re.search(Regexes.name_and_segments, raw_string)
            if s:
                name, segment_string = s.groups()

        s = re.search(NorgItemHead.re_namefirst, name or raw_string)
        if s:
            name, link = s.groups()
        if not name:
            name = raw_string

        return cls(name, status=status, link=link, segment_string=segment_string)

    @property
    def path(self) -> Union[Path, None]:
        if self._path:
            return self._path
        elif self.link:
            return Path(self.link.strip(":$/"))
        else:
            return None

    @path.setter
    def path(self, new_path: Path) -> None:
        self._path = new_path

    def as_norg(self) -> str:
        segment_string = f" || {self.segment_string}" * bool(self.segment_string)
        status = f"({self.status})" * bool(self.status)
        name = f"[{self.name}]{{:{self.link}:}}" if self.link else self.name
        return f"{status} {name}{segment_string}"

    def __str__(self) -> str:
        return self.as_norg()

    def __repr__(self) -> str:
        return self.__str__()

    def __bool__(self) -> bool:
        return bool(self.link)
