import re
from typing import Any, List, Union
from planager.utils.datetime_extensions import PTime

from planager.utils.linewrap import wrap_string

BOOL2STR = {True: "true", False: "false"}
STR2BOOL = {"true": True, "false": False}

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


def make_norg_notes(
        notes: str
    ) -> str:
    notes = wrap_string(notes, width=120, trailing_spaces=0)
    return f"* Notes\n\n{notes}\n"


def get_norg_entries(norg_str):
    regx = re.compile("\n(?=\*\* \d\d:\d\d \| )")
    return re.split(regx, norg_str.split("* Notes")[0])[1:]


def parse_norg_header():
    ...


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


def parse_norg_notes(): 
    ...


def parse_norg_schedule():
    ...


def write_norg_schedule():
    ...


