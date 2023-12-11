import json
import re
from pathlib import Path
from typing import Protocol

from .nkdatetime import NKDate


class PathManagerType(Protocol):
    declaration_dir: Path
    backup_dir: Path


def shift_declaration_ndays(path_manager: PathManagerType, ndays: int) -> None:
    """
    Moves all dates (surrounded by double quotes) under roadmaps back by 'ndays' days. Moves
      forward, naturally, if 'ndays' is negative.
    """
    if not ndays:
        return
    with open(path_manager.declaration_dir, encoding="utf-8") as f:
        declaration_dict = json.load(f)
    with open(path_manager.backup_dir / "declaration/tmp.json", "w", encoding="utf-8") as f:
        json.dump(declaration_dict, f, ensure_ascii=False, indent=4)
    roadmaps_dict = declaration_dict["roadmaps"]
    roadmaps_string = json.dumps(roadmaps_dict, ensure_ascii=False)

    all_dates = list(
        map(NKDate.from_string, re.findall(r"(?<=\")\d{4}-\d\d-\d\d(?=\")", roadmaps_string))
    )
    min_date, max_date = min(all_dates), max(all_dates)
    print(min_date, max_date)
    date_range = max_date.range(min_date) if ndays > 0 else min_date.range(max_date)
    for date in date_range:
        roadmaps_string = roadmaps_string.replace(str(date), str(date + ndays))
    declaration_dict["roadmaps"] = json.loads(roadmaps_string)

    with open(path_manager.declaration_dir, "w", encoding="utf-8") as f:
        json.dump(declaration_dict, f, ensure_ascii=False, indent=4)
