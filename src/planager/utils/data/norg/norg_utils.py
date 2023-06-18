import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from planager.utils.datetime_extensions import ZERODATETIME, PDateTime, PTime
from planager.utils.linewrap import wrap_string
from planager.utils.regex import Regexes

BOOL2STR = {True: "true", False: "false"}
STR2BOOL = {"true": True, "false": False}


def split_document(fp: Path) -> Tuple:
    regx = Regexes.section_split
    with open(fp) as f:
        return re.split(regx, f.read())


def make_header(**kwargs) -> str:
    inner = "\n".join(
        map(": ".join, map(lambda kv: (kv[0], str(kv[1])), kwargs.items()))
    )
    return f"@document.meta\n{inner}\n@end"


def get_kv(s: str) -> Tuple[str, str]:
    return re.split(" *: *", s.strip(), 1)


def get_list_from_header(header: str) -> dict:
    header_info = []
    for k, v in re.findall("([^:\n]+): ([^\n]*)\n", header):
        header_info.append({"key": k, "value": v})
    return header_info


def get_dict_from_section(section: str) -> dict:
    section_dict = {}
    title, body, subsections_str = re.search(
        "\s*(^[^\n]+)\n*(.*)(\*\*.*)", section, re.DOTALL
    ).groups()
    section_dict.update({"title": title, "body": body.strip(), "subsections": []})
    subsections = re.findall("\*\*\s+([^\n]+)\n+(.*?)", subsections_str, re.DOTALL)
    for title, body in subsections:
        section_dict["subsections"].append({"title": title, "body": body.strip()})
    return section_dict


def get_dict_from_path(fp: Path) -> Dict:
    doc = {"header": {}, "sections": {}}
    header, *sections = split_document(fp)
    doc.update({"header": get_list_from_header(header)})
    for i, section in enumerate(sections):
        doc["sections"].update({str(i + 1), get_dict_from_section(section)})
    return doc


def parse_norg_entry(entry: str):
    regx = Regexes.entry_old
    groups = re.search(regx, entry).groups()
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
        self.__dict__.update(**locals())

    @classmethod
    def from_path(cls, norg_path: Path) -> "Norg":
        # print(50 * '=')
        # print(norg_path)
        # print(50 * '=')
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

        search = re.search(regx_header_and_body, norg)
        if not search:
            print(100 * "&")
            print(norg)
            print(search)
            print(regx_header_and_body)
        header, body = search.groups()
        body = "\n" + body
        # print(body)
        lines = header.split("\n")

        # print(lines)
        kwarg_dict = dict(map(lambda x: x.split(": ", 1), lines))
        # print(kwarg_dict)
        kwarg_dict["id"] = int(kwarg_dict["id"])
        kwarg_dict["parent"] = int(kwarg_dict["parent"])
        kwarg_dict["updated"] = PDateTime.from_string(kwarg_dict["updated"])

        def parse_section(section_str: str) -> Optional[Dict[str, Any]]:
            regx_subsections = Regexes.subsection_split
            # section_str = section_str.strip()
            section_dict = {"title": "", "text": "", "subsections": []}
            res = re.search("\*?([^\n]+)", section_str)
            if not res:
                return None
            section_dict["title"] = res.groups()[0].strip()
            res = re.search("\n(.*?)\n?\*+ ", section_str)
            section_dict["text"] = "" if not res else res.groups()[0].strip()
            section_dict["subsections"] = list(
                map(str.strip, re.split(regx_subsections, section_str)[1:])
            )
            return section_dict

        sections = re.split(regx_sections, body)
        kwarg_dict.update(
            {"sections": list(map(parse_section, filter(bool, sections)))}
        )
        # print(sections[0])
        kwarg_dict.update({"items": re.split(regx_items, sections[0])[1:]})

        return kwarg_dict

    @staticmethod
    def parse_link(s: str) -> str:
        regx_link = Regexes.link
        search = re.search(regx_link, s)
        if not search:
            return ("", "")
        s = search.groups()
        # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # print(s)
        link = [result for result in s if str(result).startswith("$/")][0]
        loc = s.index(link)
        text = s[(loc - 1) if (loc % 2) else (loc + 1)]
        return (text, link)

    @staticmethod
    def parse_preasterix_attributes(section: str) -> dict:
        if not section:
            return {}
        regx1 = Regexes.asterix_split
        regx2 = Regexes.item_split
        section = re.split(regx1, section)[0]
        # print(100 * "%")
        # print(section)
        return dict(
            map(lambda s: s.split(": "), map(str.strip, re.split(regx2, section)))
        )

    @staticmethod
    def parse_subsections(section: str) -> List[dict]:
        print(f"{section=}")
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
            return None
        regx1 = Regexes.first_line
        regx2 = Regexes.item_split
        title = re.search(regx1, item).groups()[0]
        attributes = dict(map(lambda s: s.split(": ", 1), re.split(regx2, item)[1:]))
        return {"title": title, "attributes": attributes}

    @staticmethod
    def parse_title_and_attributes(segment: str) -> Tuple[str, dict]:
        assert isinstance(segment, str)
        try:
            title, body = segment.split("\n", 1)
            attributes = Norg.get_attributes(body)
            # print(f"{title=}")
            # print(f"{attributes=}")
            return title, attributes
        except:
            return segment, {}

    @staticmethod
    def get_attributes(segment: str) -> Dict[str, Any]:
        regx = Regexes.item_split
        try:
            segments = re.split(regx, segment)[1:]
            # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            # print(segments)
            pairs = list(map(lambda s: s.split(": ", 1), segments))
            # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            # print(pairs)
            return dict(pairs) if pairs else {}
        except:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(segment)

    def __str__(self) -> str:
        return f""

    def __repr__(self) -> str:
        return self.__str__()


# class DocType(Enum):
#     ROADMAP = 1
#     PROJECT = 2


def parse_norg_str(norg_str: str) -> Norg:
    norg = {}

    return norg


def parse_norg_path(file: Path) -> Norg:
    with open(file) as f:
        norg_str = f.read()
    return parse_norg_str(norg_str)


# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/projects/notes_reading_projects/b.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/roadmaps.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/adhoc.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/calendar.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/.norg"))
