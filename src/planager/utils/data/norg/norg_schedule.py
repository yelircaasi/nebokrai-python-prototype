import re
from pathlib import Path

#from planager import entities
from planager.utils.data.norg.norg_utils import norg_utils as norg


def read_schedule_as_list(filepath: Path) -> list:
    regx = re.compile("(\d\d:\d\d) *\| *([^\n]+)")
    doc = norg.get_dict_from_path(filepath)
    _schedule = doc["sections"]["1"]["subsections"]
    schedule = []
    for entry in _schedule:
        time, name = re.search(regx, entry["title"]).groups()
        attributes = map(norg.get_kv, re.split("\s*- ", entry["body"].strip()))
        schedule.append({"time": time, "name": name, **attributes})
    return schedule


def write_schedule(schedule: dict, filepath: Path) -> None:
    header = norg.make_header(
        title=schedule["title"])
    schedule_str = schedule["schedule"]
    
    with open(filepath, 'w') as f:
        f.write(f"{header}\n\n{schedule}")