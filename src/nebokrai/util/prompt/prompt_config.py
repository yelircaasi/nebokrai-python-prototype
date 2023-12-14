from typing import Optional

from ..elementary_types import PromptTypeName, prompt_type_mapping
from ..serde.custom_dict_types import (
    ActivityDictParsed,
    ComponentsDictParsed,
    SubitemDictParsed,
)
from .type_conversion import ConversionFuncType, conversion_func_dict


class PromptConfig:
    """
    Container object to hold the information needed to run a specific type of prompt.
    """

    def __init__(
        self,
        prompt_type: PromptTypeName = None,
        quit_string: str = ":q",
        prompt_message: Optional[str] = None,
        invalid_input_message: Optional[str] = None,
        sequence_item_config: Optional["PromptConfig"] = None,
        components: Optional[dict[str, "PromptConfig"]] = None,
    ) -> None:
        self.prompt_type: PromptTypeName = prompt_type
        self.conversion_func: ConversionFuncType = conversion_func_dict.get(
            prompt_type, lambda x: x
        )
        self.quit_string: str = quit_string
        self.prompt_message: str = prompt_message or (
            f"Please give an input corresponding to '{prompt_type}'"
            f", parsable as {prompt_type_mapping[prompt_type]}"
            f" ('{quit_string}' to quit):  "
        )
        self.invalid_input_message: str = invalid_input_message or "Invalid input."
        self.sequence_item_config: Optional["PromptConfig"] = sequence_item_config
        self.components: Optional[dict[str, "PromptConfig"]] = components

    @classmethod
    def from_activity_dict(cls, activity_dict: ActivityDictParsed) -> "PromptConfig":
        """
        Create an instance of PromptConfig from the information supplied in declaration.json,
          via the parsed activity dict.
        """
        prompt_type = activity_dict["dtype"]
        sequence_item_config = cls.config_from_subitem_dict(activity_dict["subitem"])
        components = cls.config_from_components_dict(activity_dict["components"])

        return PromptConfig(
            prompt_type=prompt_type,
            quit_string=activity_dict["quit_string"],
            prompt_message=activity_dict["prompt"],
            invalid_input_message=activity_dict["error_prompt"],
            sequence_item_config=sequence_item_config,
            components=components,
        )

    @staticmethod
    def config_from_subitem_dict(subitem_dict: SubitemDictParsed) -> Optional["PromptConfig"]:
        """
        Read in parsed subitem dict as its own PromptConfig object.
        """
        print(subitem_dict)  # TODO
        return PromptConfig()

    @staticmethod
    def config_from_components_dict(
        components_dict: ComponentsDictParsed,
    ) -> Optional[dict[str, "PromptConfig"]]:
        """
        Read in parsed components dict as its own dict of PromptConfig object.
        """
        print(components_dict)  # TODO
        return {"": PromptConfig()}
