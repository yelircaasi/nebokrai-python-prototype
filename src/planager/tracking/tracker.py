import json

from ..configuration import path_manager
from ..util import PDate
from .tracker_item import TrackerItem, get_tracker_item


class Tracker:
    """
    Responsible for entry of tasks completed.
    """

    def __init__(self, tracking_dict: dict) -> None:
        """
        Parses the activities as specified in the declaration and creates an
          instance of TrackingItem for each.
        """
        self.activities = []
        for item_dict in tracking_dict["activities"]:
            self.activities.append(get_tracker_item(item_dict))
        self.activities.sort(key=lambda a: a.order)

    def record(self) -> None:
        self.prompt_interactively()
        self.write()

    def prompt_interactively(self) -> None:
        for activity in self.activities:
            activity.prompt_interactively()

    def write(self) -> None:
        log_dict = {activity.name: activity.as_log_dict() for activity in self.activities}
        tracking_path = path_manager.tracking_dir / f"{PDate.today()}.json"
        with open(tracking_path, "w", encoding="utf-8") as f:
            json.dump(log_dict, f, ensure_ascii=False, indent=4)
