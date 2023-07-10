""" EXAMPLE DOCUMENT:
@document.meta
title: Schedule for 2023-05-27
authors: [yelircaasi]
categories: 
version: 0.1
@end

.toc

* Items

** Pay the bill to ZDF
   - due: 2023-06-14-18:00
   - duration: 10
   - priority: 100

** Get the system setup
   - start: none
   - due: 2023-06-15
   - priority: 70

"""

from pathlib import Path
from typing import Any, Dict, Iterator, List, Union

from ...util import Norg, PDate, PTime, now, tabularize
from .entry import Entry


class AdHoc:
    def __init__(self, entries: List[Entry] = []) -> None:
        self.title = "Ad Hoc Entries"
        self.entries = entries
        # self.author = config.author

        # NEW FORMAT
        self._adhocs: Dict[PDate, List[Entry]] = {}

    def __iter__(self) -> Iterator[Entry]:
        return iter(self.entries)

    def __getitem__(self, __date: PDate) -> List[Entry]:
        return self._adhocs.get(__date, [])

    def __str__(self) -> str:
        return self.pretty()

    def __repr__(self) -> str:
        return self.__str__()

    def pretty(self, width: int = 80) -> str:
        topbeam = "┏" + (width - 2) * "━" + "┓"
        bottombeam = "\n┗" + (width - 2) * "━" + "┛"
        # thickbeam = "┣" + (width - 2) * "━" + "┫"
        # thinbeam = "\n┠" + (width - 2) * "─" + "┨\n"
        top = tabularize(self.title, width, pad=1)
        empty = tabularize("", width)
        return (
            "\n".join(("", topbeam, empty, top, empty, ""))
            + "\n".join(map(str, self.entries))
            + bottombeam
        )

    # def __getitem__(self, __name: str) -> Any:
    #     schedule = ...
    #     return schedule

    # def __setitem__(self, __name: str, __value: Any) -> None:
    #     ...

    @classmethod
    def from_norg(cls, fp_or_str: Union[Path, str]) -> "AdHoc":
        ...  # TODO
        return cls()

    @classmethod
    def from_json(cls, fp_or_str: Union[Path, str]) -> "AdHoc":
        ...  # TODO
        return cls()

    @classmethod
    def from_html(cls, fp_or_str: Union[Path, str]) -> "AdHoc":
        ...  # TODO
        return cls()

    def to_norg(self, fp: Path) -> None:
        with open(fp, "w") as f:
            f.write(self.to_norg_str())

    def to_json(self, fp: Path) -> None:
        with open(fp, "w") as f:
            f.write(self.to_json_str())

    def to_html(self, fp: Path) -> None:
        with open(fp, "w") as f:
            f.write(self.to_html_str())

    def to_norg_str(self) -> str:
        header = Norg.make_header(
            title=self.title,
            # author=self.author,
            updated=now(),
        )
        return ""  # TODO

    @classmethod
    def from_norg_workspace(cls, workspace_dir: Path) -> "AdHoc":
        file = workspace_dir / "adhoc.norg"
        parsed = Norg.from_path(file)
        entries = []
        for section in parsed.sections:
            # attributes = Norg.get_attributes(section["text"])
            attributes = section["attributes"]
            start = PTime.from_string(attributes["start"])
            entries.append(
                Entry(
                    name=section["title"] or "<Placeholder Entry Name>",
                    start=start,
                    end=PTime.from_string(attributes.get("end")) or start + 30,
                    priority=int(attributes.get("priority") or 0),
                    ismovable=bool(str(attributes.get("ismovable")).lower() == "true"),
                    notes=attributes.get("notes") or "",
                    normaltime=attributes.get("normaltime") or 30,
                    idealtime=attributes.get("idealtime"),
                    mintime=attributes.get("mintime"),
                    maxtime=attributes.get("maxtime"),
                    alignend=bool(str(attributes.get("alignend")).lower() == "true"),
                )
            )
        return cls(entries)

    def to_json_str(self) -> str:
        ...
        return ""  # TODO

    def to_html_str(self) -> str:
        ...
        return ""  # TODO

    @property
    def end_date(self) -> PDate:
        if not self._adhocs:
            return PDate.tomorrow()
        return max(self._adhocs)

    @property
    def start_date(self) -> PDate:
        if not self._adhocs:
            return PDate.tomorrow()
        return min(self._adhocs)
