import json

from ..configuration import path_manager
from ..util import PDate
from ..util.prompt.prompt_functions import prompt_natural_sequence
from ..util.serde.custom_dict_types import (
    ActivityDictRaw,
    DayLogDictRaw,
    RoutineDictRaw,
)
from .tracker_item import TrackerItem


class Tracker:
    """
    Responsible for entry of tasks completed.
    """

    def __init__(self, tracking_dict: dict, routines_dict: dict) -> None:
        """
        Parses the activities as specified in the declaration and creates an
          instance of TrackingItem for each.
        """
        self.activities: list[TrackerItem] = []
        for item_dict in tracking_dict["activities"]:
            self.activities.append(TrackerItem(item_dict))
        self.add_routines(routines_dict)
        self.activities.sort(key=lambda a: (a.order, a.name))

    def add_routines(self, routines_dict: dict[str, RoutineDictRaw]) -> None:
        """
        Adds an item tracker for each item of each routine.
        """
        for routine_name, routine_dict in routines_dict.items():
            # print(routine_dict)
            base_order = routine_dict.get("default_order") or 40.0
            for i, item_dict in enumerate(routine_dict["items"]):
                self.activities.append(
                    TrackerItem.from_routine_item_dict(
                        item_dict, routine_name, order=base_order + i / 100
                    )
                )

    def record(self) -> None:
        self.prompt_interactively()
        self.write()

    def prompt_interactively(self) -> None:
        """
        Elicit user input for all activities, according to their declared data type and prompt.
        """
        print("The following tracking items are available:")
        print("\n".join(map(lambda ia: f"  {ia[0]:>2}) {ia[1].name}", enumerate(self.activities))))
        indices = prompt_natural_sequence(
            "Please enter a number or list of numbers (seprated by commas, spaces, or both), "
            + "or leave empty for all items."
        )
        if not indices:
            for activity in self.activities:
                activity.prompt_interactively()
        else:
            for index in indices:
                self.activities[index].prompt_interactively()

    def write(self) -> None:
        """
        Records the entire metrics tracked for the day. TODO: make non-destructive for when tracking
          is done multiple times a day.
        """
        log_dict: DayLogDictRaw = {}
        for activity in self.activities:
            activity_serialized: ActivityDictRaw = activity.serialize()
            log_dict.update({activity.name: activity_serialized})
        tracking_path = path_manager.tracking_dir / f"{PDate.today()}.json"
        with open(tracking_path, "w", encoding="utf-8") as f:
            json.dump(log_dict, f, ensure_ascii=False, indent=4)
