import re
from typing import Any, Dict, List, Tuple, Union

from click import Path
from planager.utils.datetime_extensions import PTime

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





