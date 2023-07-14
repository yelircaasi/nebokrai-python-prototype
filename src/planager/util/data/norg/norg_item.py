from pathlib import Path
import re
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union

from ...display import wrap_string
from ...pdatetime import ZERODATETIME, PDate, PDateTime, PTime
from ...regex import Regexes

BOOL2STR = {True: "true", False: "false"}
STR2BOOL = {"true": True, "false": False}


class NorgItem:
    def __init__(
        self,
        name: str,
        path: Optional[str],
        item_id: Optional[str],
        parent: Optional[str],
        start: Optional[str],
        end: Optional[str],
        priority: Optional[str],
        ismovable: Optional[str],
        notes: Optional[str],
        normaltime: Optional[str],
        idealtime: Optional[str],
        mintime: Optional[str],
        maxtime: Optional[str],
        interval: Optional[str],
        duration: Optional[str],
        cluster_size: Optional[str],
        tags: Optional[str],
        description: Optional[str],
        alignend: Optional[str],
        before: Optional[str],
        after: Optional[str],
    ) -> None:
        self.name = str(name)
        self.item_id = str(item_id) if item_id else None
        self.path = path if path else None
        self.parent = parent if parent else None
        self.start = start if start else None
        self.end = end if end else None
        self.priority = priority if priority else None
        self.ismovable = ismovable if ismovable else None
        self.notes = notes if notes else None
        self.normaltime = normaltime if normaltime else None
        self.idealtime = idealtime if idealtime else None
        self.mintime = mintime if mintime else None
        self.maxtime = maxtime if maxtime else None
        self.duration = duration if duration else None
        self.interval = interval if interval else None
        self.cluster_size = cluster_size if cluster_size else None
        self.tags = tags if tags else None
        self.description = description if description else None
        self.alignend = alignend if alignend else None
        self.before = before if before else None
        self.after = after if after else None
        # self.before: List[Tuple[str, ...]] = before
        # self.after: List[Tuple[str, ...]] = after

    @classmethod
    def from_string(cls, norg_str) -> "NorgItem":
        s = re.search(Regexes.item_title, norg_str.split("||").strip())
        if s:
            name = s.groups()[0]
        else:
            raise ValueError(f"Norg item must have a name. Item string: '{norg_str}'")
        attributes = dict(re.findall(Regexes.attribute_pair, norg_str))

        return cls(
            name=name,
            path=attributes.get("path"),
            item_id=attributes.get("id"),
            parent=attributes.get("parent"),
            start=attributes.get("start"),
            end=attributes.get("end"),
            priority=attributes.get("priority"),
            ismovable=attributes.get("ismovable"),
            notes=attributes.get("notes"),
            normaltime=attributes.get("normaltime"),
            idealtime=attributes.get("idealtime"),
            mintime=attributes.get("mintime"),
            maxtime=attributes.get("maxtime"),
            interval=attributes.get("interval"),
            duration=attributes.get("duration"),
            cluster_size=attributes.get("cluster_size"),
            tags=attributes.get("tags"),
            description=attributes.get("description"),
            alignend=attributes.get("alignend"),
            before=attributes.get("before"),
            after=attributes.get("after"),
        )

    @staticmethod
    def make_norg_entry(
        name: str,
        parent: str,
        start: Any,
        priority: int,
        ismovable: bool,
        notes: str,
        normaltime: int,
        idealtime: int,
        mintime: int,
        maxtime: int,
        alignend: bool,
    ) -> str:
        booldict = BOOL2STR
        notes = wrap_string(notes, width=102, trailing_spaces=18)
        return "\n".join(
            (
                f"** {str(start)} | {name}",
                "",
                f"  - parent:   {parent}",
                f"  - priority:   {priority}",
                f"  - ismovable:  {booldict[ismovable]}",
                f"  - notes:      {notes}",
                f"  - normaltime: {normaltime}",
                f"  - idealtime:  {idealtime}",
                f"  - mintime:    {mintime}",
                f"  - maxtime:    {maxtime}",
                f"  - alignend:   {booldict[alignend]}",
                "",
            )
        )

    @staticmethod
    def parse_norg_entry(entry: str):
        regx = Regexes.entry_old
        result = re.search(regx, entry)
        groups = result.groups() if result else []
        if not len(groups) == 10:
            raise ValueError("Invalid norg entry format.")
        groupnames = [
            "start",
            "name",
            "priority",
            "ismovable",
            "notes",
            "normaltime",
            "idealtime",
            "mintime",
            "maxtime",
            "alignend",
        ]
        booldict = STR2BOOL
        kwdict = dict(zip(groupnames, groups))
        kwdict["notes"] = re.sub("\s+", " ", kwdict["notes"]).strip()
        kwdict["start"] = PTime.from_string(kwdict["start"])
        for integer in ["normaltime", "idealtime", "mintime", "maxtime"]:
            kwdict[integer] = int(kwdict[integer])
        for boolean in ["ismovable", "alignend"]:
            kwdict[boolean] = booldict[kwdict[boolean]]
        return kwdict

    def get_name(self) -> Optional[str]:
        return self.name or None

    def get_path(self) -> Optional[Path]:
        if not self.path:
            return None
        return Path(self.path)

    def get_id(self) -> Optional[str]:
        if not self.item_id:
            return None
        return self.item_id

    def get_parent(self) -> Optional[str]:
        if not self.parent:
            return None
        return self.parent

    def get_start_date(self) -> Optional[PDate]:
        return PDate.ensure_is_pdate(self.start)

    def get_start_time(self) -> Optional[PTime]:
        return PTime.ensure_is_ptime(self.start)

    def get_end_date(self) -> Optional[PDate]:
        return PDate.ensure_is_pdate(self.end)

    def get_end_time(self) -> Optional[PTime]:
        return PTime.ensure_is_ptime(self.end)

    def get_priority(self) -> Optional[int]:
        if not self.priority:
            return None
        return int(self.priority)

    def get_ismovable(self) -> Optional[bool]:
        if not self.ismovable:
            return True
        return STR2BOOL[self.ismovable.lower()]

    def get_notes(self) -> str:
        return self.notes or ""

    def get_normaltime(self) -> Optional[int]:
        if not self.normaltime:
            return None
        return int(self.normaltime)

    def get_idealtime(self) -> Optional[int]:
        if not self.idealtime:
            return None
        return int(self.idealtime)

    def get_mintime(self) -> Optional[int]:
        if not self.mintime:
            return None
        return int(self.mintime)

    def get_maxtime(self) -> Optional[int]:
        if not self.maxtime:
            return None
        return int(self.maxtime)

    def get_interval(self) -> Optional[int]:
        if not self.interval:
            return None
        return int(self.interval)

    def get_duration(self) -> Optional[int]:
        if not self.duration:
            return None
        return int(self.duration)

    def get_cluster_size(self) -> Optional[int]:
        if not self.cluster_size:
            return None
        return int(self.cluster_size)

    def get_tags(self) -> set:
        if not self.tags:
            return set()
        return set(re.split(", ?", self.tags))

    def get_description(self) -> str:
        return self.description or ""

    def get_alignend(self) -> Optional[bool]:
        if not self.alignend:
            return None
        return STR2BOOL[self.alignend.lower()]

    def get_before(self) -> Set[Tuple[str, ...]]:
        if not self.before:
            return set()
        return set(
            map(lambda x: tuple(re.split(" ?:: ?", x)), re.split(", ?", self.before))
        )

    def get_after(self) -> Set[Tuple[str, ...]]:
        if not self.after:
            return set()
        return set(
            map(lambda x: tuple(re.split(" ?:: ?", x)), re.split(", ?", self.after))
        )


class NorgItems:
    def __init__(self, items: List[NorgItem] = []):
        self._items = items

    @classmethod
    def from_dict(cls, __dict: dict) -> "NorgItems":
        ...
        return cls()

    def __iter__(self) -> Iterator[NorgItem]:
        return iter(self._items)

    def __getitem__(self, __index: int) -> NorgItem:
        return self._items[__index]

    @staticmethod
    def parse_item_with_attributes(item: str) -> dict:
        if not item.strip():
            print("Tried to parse empty item!")
            return {}
        regx1 = Regexes.first_line
        regx2 = Regexes.item_split
        result = re.search(regx1, item)
        title = result.groups()[0] if result else "<placeholder title>"
        attributes = dict(map(lambda s: s.split(": ", 1), re.split(regx2, item)[1:]))
        return {"title": title, "attributes": attributes}
