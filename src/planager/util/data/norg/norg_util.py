import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ...display.linewrap import wrap_string
from ...pdatetime import ZERODATETIME, PDateTime, PTime
from ...regex import Regexes

BOOL2STR = {True: "true", False: "false"}
STR2BOOL = {"true": True, "false": False}


def split_document(fp: Path) -> List[str]:
    regx = Regexes.section_split
    with open(fp) as f:
        return re.split(regx, f.read())


def make_header(**kwargs) -> str:
    inner = "\n".join(
        map(": ".join, map(lambda kv: (kv[0], str(kv[1])), kwargs.items()))
    )
    return f"@document.meta\n{inner}\n@end"


def get_kv(attr_str: str) -> List[List[str]]:
    return [re.split(" *: *", s.strip(), 1) for s in re.split("\n\s*", attr_str)]


def get_list_from_header(header: str) -> List[Dict[str, str]]:
    header_info = []
    for k, v in re.findall("([^:\n]+): ([^\n]*)\n", header):
        header_info.append({"key": k, "value": v})
    return header_info


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


def get_dict_from_path(fp: Path) -> Dict:
    doc: Dict[str, Any] = {"header": {}, "sections": {}}
    header, *sections = split_document(fp)
    doc.update({"header": get_list_from_header(header)})
    for i, section in enumerate(sections):
        doc["sections"].update({str(i + 1), get_dict_from_section(section)})
    return doc


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


def parse_norg_header():
    ...


def parse_norg_notes():
    ...


def make_norg_entry(
    name: str,
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


def make_norg_header(
    title: str,
    author: str = "yelircaasi",
    categories: List[str] = [],
    version: Union[float, str] = "0.1",
) -> str:
    return "\n".join(
        (
            "@document.meta",
            f"title: {title}",
            f"authors: [{author}]",
            f"categories: {', '.join(categories)}",
            f"version: {str(version)}",
            "@end",
            "",
            ".toc",
            "",
            "* Schedule",
            "",
        )
    )


def make_norg_notes(notes: str) -> str:
    notes = wrap_string(notes, width=120, trailing_spaces=0)
    return f"* Notes\n\n{notes}\n"


def get_norg_entries(norg_str):
    regx = Regexes.entry_split_old
    return re.split(regx, norg_str.split("* Notes")[0])[1:]


class Norg:
    def __init__(
        self,
        title: str = "",
        description: str = "",
        author: str = "",
        id: int = -1,
        parent: int = -1,
        updated: PDateTime = ZERODATETIME,
        categories: str = "",
        sections: dict = {},
        items: List[str] = [],
        path: Optional[Path] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.author = author
        self.id = id
        self.parent = parent
        self.updated = updated
        self.categories = categories
        self.sections = sections
        self.items = items
        self.path = path

    @classmethod
    def from_path(cls, norg_path: Path) -> "Norg":
        with open(norg_path) as f:
            norg_str = f.read()
        norg_obj = cls.from_string(norg_str)
        norg_obj.path = norg_path
        return norg_obj

    @classmethod
    def from_string(cls, norg_str) -> "Norg":
        kwarg_dict = cls.parse_norg_str(norg_str)

        return cls(**kwarg_dict)

    @staticmethod
    def parse_norg_str(norg: str) -> Dict[str, Any]:
        regx_header_and_body = Regexes.header_and_body
        regx_sections = Regexes.section_split
        regx_items = Regexes.item1_split

        result = re.search(regx_header_and_body, norg)
        if result:
            header, body = result.groups() if result else ("", "")
        else:
            return {}
        body = "\n" + body
        lines = str(header).split("\n")

        kwarg_dict: Dict[str, Any] = dict(map(lambda x: x.split(": ", 1), lines))

        kwarg_dict["id"] = int(kwarg_dict["id"])
        kwarg_dict["parent"] = int(kwarg_dict["parent"])
        kwarg_dict["updated"] = PDateTime.from_string(kwarg_dict["updated"])

        def parse_section(section_str: str) -> Optional[Dict[str, Any]]:
            regx_subsections = Regexes.subsection_split
            section_dict = {
                "title": "",
                "text": "",
                "attributes": {},
                "subsections": [],
            }
            res = re.search("\*?([^\n]+)", section_str)
            if not res:
                return None
            section_dict["title"] = res.groups()[0].strip()
            res = re.search("\n(.*?)\n?[\*]+ ", section_str)
            section_dict["text"] = "" if not res else res.groups()[0].strip()
            regx = Regexes.attribute_pair
            section_dict["attributes"] = dict(re.findall(regx, section_str))
            section_dict["subsections"] = list(
                map(str.strip, re.split(regx_subsections, section_str)[1:])
            )
            return section_dict

        sections = re.split(regx_sections, body)
        kwarg_dict.update(
            {"sections": list(map(parse_section, filter(bool, sections)))}
        )
        kwarg_dict.update({"items": re.split(regx_items, sections[0])[1:]})

        return kwarg_dict

    @staticmethod
    def parse_link(s: str) -> Tuple[str, str]:
        regx_link = Regexes.link
        search = re.search(regx_link, s)
        if not search:
            return ("", "")
        else:
            groups = search.groups() if search else []
            link = [result for result in groups if str(result).startswith("$/")][0]
            loc = groups.index(link)
            text = groups[(loc - 1) if (loc % 2) else (loc + 1)]
            return (text, link)

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

    @staticmethod
    def parse_title_and_attributes(segment: str) -> Tuple[str, dict]:
        assert isinstance(segment, str)
        try:
            title, body = segment.split("\n", 1)
            attributes = Norg.get_attributes(body)
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

    def __str__(self) -> str:
        return f""

    def __repr__(self) -> str:
        return self.__str__()


# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/projects/notes_reading_projects/b.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/roadmaps.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/adhoc.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/calendar.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/.norg"))
