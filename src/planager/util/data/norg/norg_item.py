from pathlib import Path
import re
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union

from .norg_item_head import NorgItemHead
from ...display import wrap_string
from ...pdatetime import PDate, PDateTime, PTime
from ...regex import Regexes


class NorgItem:
    BOOL2STR = {True: "true", False: "false"}
    STR2BOOL = {
        "true": True,
        "false": False,
        "True": True,
        "False": False,
        True: True,
        False: False,
    }
    DONEDICT = {"x": True, " ": False, "✓": True, None: False}

    def __init__(
        self,
        head: Optional[Union[str, NorgItemHead]] = None,
        name: Optional[str] = None,
        path: Optional[Union[str, Path]] = None,
        link: Optional[str] = None,
        status: Optional[str] = None,
        item_id: Optional[Union[str, Tuple[str, ...]]] = None,
        parent: Optional[Union[str, Tuple[str, ...]]] = None,
        start: Optional[Union[str, PDate, PTime]] = None,
        end: Optional[Union[str, PDate, PTime]] = None,
        priority: Optional[Union[str, int]] = None,
        ismovable: Optional[Union[str, bool]] = None,
        notes: Optional[str] = None,
        normaltime: Optional[Union[str, int]] = None,
        idealtime: Optional[Union[str, int]] = None,
        mintime: Optional[Union[str, int]] = None,
        maxtime: Optional[Union[str, int]] = None,
        interval: Optional[Union[str, int]] = None,
        duration: Optional[Union[str, int]] = None,
        cluster_size: Optional[Union[str, int]] = None,
        tags: Optional[Union[str, Set[str]]] = None,
        description: Optional[str] = None,
        alignend: Optional[Union[str, bool]] = None,
        before: Optional[Union[str, Set[Tuple[str, ...]]]] = None,
        after: Optional[Union[str, Set[Tuple[str, ...]]]] = None,
    ) -> None:
        self._head: NorgItemHead = self.convert_head(head)
        if name:
            self._head.name = name
        if not self._head.name:
            raise ValueError("Nameless item is invalid.")
        if path:
            self._head.path = Path(path)
        if link:
            self._head.link = link
        if status:
            self._head.status = status
        self.item_id: Optional[Tuple[str, ...]] = self.convert_tuple(item_id)
        self.parent: Optional[Tuple[str, ...]] = self.convert_tuple(parent)
        self._start: Optional[Union[PDate, PTime, str]] = start if start else None
        self._end: Optional[Union[PDate, PTime, str]] = end if end else None
        self.priority: Optional[int] = self.convert_int(priority)
        self.ismovable: Optional[bool] = self.convert_bool(ismovable)
        self.notes: Optional[str] = notes
        self.normaltime: Optional[int] = self.convert_int(normaltime)
        self.idealtime: Optional[int] = self.convert_int(idealtime)
        self.mintime: Optional[int] = self.convert_int(mintime)
        self.maxtime: Optional[int] = self.convert_int(maxtime)
        self.duration: Optional[int] = self.convert_int(duration)
        self.interval: Optional[int] = self.convert_int(interval)
        self.cluster_size: Optional[int] = self.convert_int(cluster_size)
        self.tags: Optional[Set[str]] = self.convert_tags(tags)
        self.description: Optional[str] = description
        self.alignend: Optional[bool] = self.convert_bool(alignend)
        self.before: Optional[Set[Tuple[str, ...]]] = self.convert_tupleset(before)
        self.dependencies: Optional[Set[Tuple[str, ...]]] = self.convert_tupleset(after)

    @classmethod
    def from_string(cls, norg_str) -> "NorgItem":
        head = NorgItemHead.from_string(norg_str)

        attributes = dict(re.findall(Regexes.attribute_pair, norg_str))

        return cls(
            head=head,
            # path=head.path,
            # link=head.link,
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
    def convert_head(head: Optional[Union[NorgItemHead, str]]):
        if head is None:
            return NorgItemHead("")
        return NorgItemHead(head) if isinstance(head, str) else head

    @property
    def name(self) -> str:
        return self._head.name

    @property
    def path(self) -> Optional[Path]:
        return Path(self._head.path) if self._head.path else None

    @property
    def link(self) -> Optional[str]:
        return self._head.link

    @property
    def isdone(self) -> bool:
        return bool(self.DONEDICT.get(self.status))

    @property
    def status(self) -> Optional[str]:
        return self._head.status

    @property
    def segment_string(self) -> Optional[str]:
        return self._head.segment_string

    # -------------------------------------------------
    @property
    def start_date(self) -> Optional[PDate]:
        if re.search(r"\d{4}-\d\d?-\d\d?", str(self._start)):
            return PDate.ensure_is_pdate(self._start)
        return None

    @property
    def start_time(self) -> Optional[PTime]:
        if re.search(r"\d\d?:\d\d", str(self._start)):
            return PTime.ensure_is_ptime(self._start)
        return None

    @property
    def start_string(self) -> Optional[str]:
        if not self._start:
            return None
        start_time = self.start_time
        if start_time:
            return str(start_time)
        else:
            start_date = self.start_date
            if not start_date:
                raise ValueError(f"Invalid date/time string: {self._start}")
            return str(start_date)

    @property
    def end_date(self) -> Optional[PDate]:
        if re.search(r"\d{4}-\d\d?-\d\d?", str(self._end)):
            return PDate.ensure_is_pdate(self._end)
        return None

    @property
    def end_time(self) -> Optional[PTime]:
        if re.search(r"\d\d?:\d\d", str(self._end)):
            return PTime.ensure_is_ptime(self._end)
        return None

    @property
    def end_string(self) -> Optional[str]:
        if not self._end:
            return None
        end_time = self.end_time
        if end_time:
            return str(end_time)
        else:
            end_date = self.end_date
            if not end_date:
                raise ValueError(f"Invalid date/time string: {self._end}")
            return str(end_date)

    # --------------------------------------------------

    @staticmethod
    def convert_int(conv_candidate: Optional[Union[str, int]]) -> Optional[int]:
        if conv_candidate is None:
            return None
        return int(conv_candidate)

    @staticmethod
    def convert_bool(conv_candidate: Optional[Union[str, bool]]) -> Optional[bool]:
        if conv_candidate is None:
            return None
        return NorgItem.STR2BOOL[conv_candidate]

    @staticmethod
    def convert_tags(tags: Optional[Union[str, Set[str]]]) -> Optional[Set[str]]:
        if tags is None:
            return None
        elif isinstance(tags, str):
            return set(re.split(r", ?", tags))
        return tags

    @staticmethod
    def convert_tuple(
        conv_candidate: Optional[Union[str, Tuple[str, ...]]]
    ) -> Optional[Tuple[str, ...]]:
        if conv_candidate is None:
            return None
        elif isinstance(conv_candidate, str):
            return tuple(re.split(" ?:: ?", conv_candidate))
        return conv_candidate

    @staticmethod
    def convert_tupleset(
        conv_candidate: Optional[Union[str, Set[Tuple[str, ...]]]]
    ) -> Optional[Set[Tuple[str, ...]]]:
        if conv_candidate is None:
            return None
        return (
            set(
                map(
                    lambda x: tuple(re.split(" ?:: ?", x)),
                    re.split(", ?", conv_candidate),
                )
            )
            if isinstance(conv_candidate, str)
            else set(conv_candidate)
        )

    def __str__(self) -> str:
        attributes = [""]
        if self.parent is not None:
            attributes.append(f"parent: {' :: '.join(sorted(self.parent))}")
        if self.start_string is not None:
            attributes.append(f"start: {self.start_string}")
        if self.end_string is not None:
            attributes.append(f"end: {self.end_string}")
        if self.priority is not None:
            attributes.append(f"priority: {self.priority}")
        if self.ismovable is not None:
            attributes.append(f"ismovable: {self.BOOL2STR[self.ismovable]}")
        if self.notes is not None:
            attributes.append(f"notes: {self.notes}")
        if self.normaltime is not None:
            attributes.append(f"normaltime: {self.normaltime}")
        if self.idealtime is not None:
            attributes.append(f"idealtime: {self.idealtime}")
        if self.mintime is not None:
            attributes.append(f"mintime: {self.mintime}")
        if self.maxtime is not None:
            attributes.append(f"maxtime: {self.maxtime}")
        if self.interval is not None:
            attributes.append(f"interval: {self.interval}")
        if self.duration is not None:
            attributes.append(f"duration: {self.duration}")
        if self.cluster_size is not None:
            attributes.append(f"cluster_size: {self.cluster_size}")
        if self.tags is not None:
            attributes.append(f"tags: {', '.join(sorted(self.tags))}")
        if self.description is not None:
            attributes.append(f"description: {self.description}")
        if self.alignend is not None:
            attributes.append(f"alignend: {self.BOOL2STR[self.alignend]}")
        if self.before is not None:
            before: str = ", ".join(
                sorted(map(lambda t: " :: ".join(sorted(t)), self.before))
            )
            attributes.append(f"before: {before}")
        if self.dependencies is not None:
            after: str = ", ".join(
                sorted(map(lambda t: " :: ".join(sorted(t)), self.dependencies))
            )
            attributes.append(f"after: {after}")

        if attributes == [""]:
            attributes = []

        head = str(self._head)
        # if self.segment_string:
        #     head = f"{head} || {self.segment_string}"
        attribute_string = "\n  -- ".join(attributes)

        return f"~ {head}{attribute_string}"


class NorgItems:
    def __init__(self, items: Iterable[NorgItem] = []):
        self._items = list(items)

    @classmethod
    def from_string(cls, norg_body: str) -> "NorgItems":
        norg_body = "\n" + norg_body.strip()
        if not norg_body:
            return cls()
        item_split: re.Pattern = Regexes.item1_split
        item_strings: List[str] = re.split(item_split, norg_body)[1:]
        with open("/tmp/norg_body.norg", "w") as f:
            # f.write("\n***\n".join(items))
            f.write(norg_body)
        items = map(NorgItem.from_string, item_strings)
        with open("/tmp/norg_body.norg", "w") as f:
            # f.write("\n***\n".join(items))
            f.write(norg_body)
        with open("/tmp/norg_items.norg", "w") as f:
            # f.write('\n***********\n'.join(map(str, items)))
            f.write("\n".join(item_strings))
        for item in items:
            print(str(item))
        return cls(items)

    def __iter__(self) -> Iterator[NorgItem]:
        return iter(self._items)

    def __getitem__(self, __index: int) -> NorgItem:
        return self._items[__index]
