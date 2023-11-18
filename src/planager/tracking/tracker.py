import json
from typing import Any

from ..configuration import path_manager
from ..util import PDate
from .tracker_item import BoolTrackerItem, get_tracker_item


class Tracker:
    """
    Responsible for entry of tasks completed.
    """

    def __init__(self, tracking_dict: dict, routines_dict: dict) -> None:
        """
        Parses the activities as specified in the declaration and creates an
          instance of TrackingItem for each.
        """
        self.activities = []
        for item_dict in tracking_dict["activities"]:
            self.activities.append(get_tracker_item(item_dict))
        self.add_routines(routines_dict)
        self.activities.sort(key=lambda a: (a.order, a.name))

    def add_routines(self, routines_dict: dict[str, dict[str, Any]]) -> None:
        """
        Adds an item tracker for each item of each routine.
        """
        for routine_name, routine_dict in routines_dict.items():
            for item_dict in routine_dict["items"]:
                self.activities.append(
                    BoolTrackerItem.from_routine_item_dict(item_dict, routine_name)
                )

    def record(self) -> None:
        self.prompt_interactively()
        self.write()

    def prompt_interactively(self) -> None:
        for activity in self.activities:
            activity.prompt_interactively()

    def write(self) -> None:
        """
        Records the entire metrics tracked for the day. TODO: make non-destructive for when tracking
          is done multiple times a day.
        """
        log_dict = {activity.name: activity.as_log_dict() for activity in self.activities}
        tracking_path = path_manager.tracking_dir / f"{PDate.today()}.json"
        with open(tracking_path, "w", encoding="utf-8") as f:
            json.dump(log_dict, f, ensure_ascii=False, indent=4)
