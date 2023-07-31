import re
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple, Union

from ..src.planager.util.pdatetime import PDate
from ..src.planager.util.regex import Regexes


class NorgSection:
    def __init__(
        self,
        title: str,
        text: str,
        start: Optional[str] = None,
        end: Optional[str] = None,
        priority: Optional[int] = None,
        ismovable: bool = True,
        notes: str = "",
        normaltime: Optional[int] = None,
        idealtime: Optional[int] = None,
        mintime: Optional[int] = None,
        maxtime: Optional[int] = None,
        alignend: bool = False,
    ) -> None:
        self.title = title
        self.text = text
        self.start = start
        self.end = end
        self.priority = priority
        self.ismovable = ismovable
        self.notes = notes
        self.normaltime = normaltime
        self.idealtime = idealtime
        self.mintime = mintime
        self.maxtime = maxtime
        self.alignend = alignend

    @property
    def subsections(self) -> List[str]:
        raise NotImplementedError("No attribute 'subsections' of class 'NorgSection'.")

    @classmethod
    def from_string(cls, __str) -> "NorgSection":
        title = ""
        text = ""
        return cls(title, text)  # TODO

    @staticmethod
    def parse_preasterix_attributes(section: str) -> dict:
        if not section:
            return {}
        regx1 = Regexes.asterix_split
        regx2 = Regexes.item_split
        section = re.split(regx1, section)[0]
        return dict(
            map(lambda s: s.split(": "), map(str.strip, re.split(regx2, section)))
        )

    @staticmethod
    def parse_subsections(section: str) -> Dict[str, Any]:
        regx = Regexes.subsection_split
        try:
            title, body = section.split("\n", 1)
            subsections = re.split(regx, body)
            return {"title": title, "subsections": subsections}
        except:
            return {"title": section}

    @staticmethod
    def parse_title_and_attributes(segment: str) -> Tuple[str, dict]:
        assert isinstance(segment, str)
        try:
            title, body = segment.split("\n", 1)
            attributes = NorgSection.get_attributes(body)
            return title, attributes
        except:
            return segment, {}

    @staticmethod
    def get_attributes(segment: str) -> Dict[str, Any]:
        regx = Regexes.item_split
        try:
            segments = re.split(regx, segment)[1:]
            pairs = list(map(lambda s: s.split(": ", 1), segments))
            return dict(pairs) if pairs else {}
        except:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(segment)
        return {}

    @staticmethod
    def get_dict_from_section(section: str) -> dict:
        section_dict: Dict[str, Union[dict, str, list]] = {}
        result = re.search("\s*(^[^\n]+)\n*(.*)(\*\*.*)", section, re.DOTALL)
        if result:
            title, body, subsections_str = result.groups()
        else:
            return {}
        section_dict.update({"title": title, "body": body.strip(), "subsections": []})
        subsections = re.findall("\*\*\s+([^\n]+)\n+(.*?)", subsections_str, re.DOTALL)
        subsect_list = []
        for title, body in subsections:
            subsect_list.append({"title": title, "body": body.strip()})
        section_dict["subsections"] = subsect_list
        return section_dict


class NorgSections:
    def __init__(self, sections: Iterable[NorgSection] = []) -> None:
        self._sections = list(sections)

    @classmethod
    def from_dict(cls, __dict: dict) -> "NorgSections":
        sections = __dict.values()
        return cls(sections)

    def __iter__(self) -> Iterator[NorgSection]:
        return iter(self._sections)
