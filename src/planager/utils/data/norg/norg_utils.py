import re
from typing import Any, Dict, List, Optional, Tuple, Union

from pathlib import Path
from planager.utils.datetime_extensions import PDateTime, PTime, ZERODATETIME

from planager.utils.linewrap import wrap_string

BOOL2STR = {True: "true", False: "false"}
STR2BOOL = {"true": True, "false": False}


def split_document(fp: Path) -> Tuple:
    regx = re.compile("\s*\n+\s*\*\s+")
    with open(fp) as f:
        return re.split(regx, f.read())


def make_header(**kwargs) -> str:
    inner = "\n".join(map(": ".join, map(lambda kv: (kv[0], str(kv[1])), kwargs.items())))
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
    title, body, subsections_str = re.search("\s*(^[^\n]+)\n*(.*)(\*\*.*)", section, re.DOTALL).groups()
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
    regx = re.compile(
        "\*\* (\d\d:\d\d) \| ([^\n]+)\n\n"
        "  - priority: +(\d+)\n"
        "  - ismovable: +(\w+)\n"
        "  - notes: +(.+?)\n"
        "  - normaltime: +(\d+)\n"
        "  - idealtime: +(\d+)\n"
        "  - mintime: +(\d+)\n"
        "  - maxtime: +(\d+)\n"
        "  - alignend: +(\w+)\n",
        re.DOTALL
    )
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
    kwdict["notes"] = re.sub("\s+", ' ', kwdict["notes"]).strip()
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
        version: Union[float, str] = "0.1"
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


def make_norg_notes(
        notes: str
    ) -> str:
    notes = wrap_string(notes, width=120, trailing_spaces=0)
    return f"* Notes\n\n{notes}\n"


def get_norg_entries(norg_str):
    regx = re.compile("\n(?=\*\* \d\d:\d\d \| )")
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
        regx_header = re.compile("@document.meta\n(.+)\n@end\n+\s*\n*(.*)", re.DOTALL)
        regx_sections = re.compile("\n\* ", re.DOTALL)
        regx_items = re.compile("\n\d{1,3}\. +|\n\s*- +")
        
        header, body = re.search(regx_header, norg).groups()
        lines = header.split("\n")
        
        kwarg_dict = dict(map(lambda x: x.split(": ", 1), lines))
        print(kwarg_dict)
        kwarg_dict["id"] = int(kwarg_dict["id"])
        kwarg_dict["parent"] = int(kwarg_dict["parent"])
        kwarg_dict["updated"] = PDateTime.from_string(kwarg_dict["updated"])
        
        def parse_section(section_str: str) -> Dict[str, Any]:
            regx_subsections = re.compile("\n\s*\*\* ", re.DOTALL)
            section_str = section_str.strip()
            section_dict = {"title": "", "text": "", "subsections": []}
            section_dict["title"] = re.search("([^\n]+)", section_str).groups()[0]
            section_dict["text"] = re.search("\n(.*?)\n?\*+ ", section_str).groups()[0].strip()
            section_dict["subsections"] = list(map(str.strip, re.split(regx_subsections, section_str)))
            return section_dict

        sections = re.split(regx_sections, body)
        kwarg_dict.update({"sections": list(map(parse_section, sections[1:]))})
        print(sections[0])
        kwarg_dict.update({"items": list(map(str.strip, re.split(regx_items, sections[0])[1:]))})

        return kwarg_dict
    
    @staticmethod
    def parse_link(s: str) -> str:
        regx_link = re.compile("\[(.+?)\]\{(.+?)\}|\{(.+?}\]\[(.+?)\]", re.DOTALL)
        search = re.search(regx_link, s)
        if not search:
            return ""
        return search.groups()[0]
    
    @staticmethod
    def parse_preasterix_attributes(section: str) -> dict:
        regx1 = re.compile("\n+\s*\*+ ")
        regx2 = re.compile("\n")
        section = re.split(regx1, section)[0]
        attributes = list(map(str.strip, re.split(regx2, section)))
        return attributes
    
    @staticmethod
    def parse_subsections(section: str) -> List[dict]:
        regx = re.compile("\n+\s*\*\*+ ")
        try:
            title, body = section.split("\n", 1)
            subsections = re.split(regx)
            return {"title": title, "subsections": subsections}
        except:
            return {"title": section}
    
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
