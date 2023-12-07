import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable, NamedTuple, Optional

from ..elementary_types import Natural, PromptTypeName, TrackingActivityType
from ..pdatetime import PTime
from ..serde.custom_dict_types import (
    PromptDispatcherType,
    TimedDistance,
    TimedDistanceWithElevation,
)
from .prompt_config import PromptConfig, prompt_configs

__all__ = ["PromptConfig", "prompt_any", "prompt_configs"]
# from .prompt_functions import (
#     prompt_boolean,
#     prompt_dispatcher,
#     prompt_integer,
#     prompt_integer_sequence,
#     prompt_natural,
#     prompt_natural_sequence,
#     prompt_numerical,
#     prompt_text,
#     prompt_time,
#     prompt_time_amount,
#     prompt_timed_distance,
#     prompt_timed_distance_with_elevation,
#     prompt_typed_list,
#     simple_prompt_functions,
# )

# __all__ = [
#     "prompt_boolean",
#     "prompt_integer",
#     "prompt_integer_sequence",
#     "prompt_natural",
#     "prompt_natural_sequence",
#     "prompt_numerical",
#     "prompt_text",
#     "prompt_time",
#     "prompt_time_amount",
#     "prompt_timed_distance",
#     "prompt_timed_distance_with_elevation",
#     "prompt_typed_list",
#     "simple_prompt_functions",
# ]


def prompt_single(prompt_config: "PromptConfig") -> Optional[TrackingActivityType]:
    """
    Interactively prompts for the desired type until the desired type is given or the quit string is
      given.
    """
    isvalid, quit_loop = False, False
    while not isvalid or quit_loop:
        try:
            raw = input(prompt_config.prompt_message)
            if raw == prompt_config.quit_string:
                return None
            value = prompt_config.conversion_func(raw)
            isvalid = True
        except ValueError:
            print(prompt_config.invalid_input_message)
            continue
    return value


def prompt_composite(prompt_config: PromptConfig) -> dict[str, TrackingActivityType]:
    """
    Run the input prompt corresponding to types with subfields.
    """
    assert prompt_config.components is not None
    ret: dict[str, TrackingActivityType] = {}
    for k, kconfig in prompt_config.components.items():
        parsed_response: TrackingActivityType = prompt_any(kconfig)
        # if parsed_response is None:
        #     return None
        ret.update({k: parsed_response})
    return ret


def prompt_sequence(prompt_config: "PromptConfig") -> list[TrackingActivityType]:
    """
    Interactively prompts for an item of type `item_type` until the quit_string is entered.
    """
    assert prompt_config.sequence_item_config is not None
    responses: list[Any] = []
    print(prompt_config.prompt_message)
    subprompt_config: PromptConfig = prompt_config.sequence_item_config

    quit_loop = False
    while not quit_loop:
        response = prompt_any(subprompt_config)
        if not (quit_loop := (response is None)):
            responses.append(response)

    return responses


def prompt_any(prompt_config: PromptConfig) -> TrackingActivityType:
    """
    Run whichever type of prompt is appropriate for the configuration supplied.
    """
    assert (
        not prompt_config.sequence_item_config and prompt_config.components
    ), "At most one of 'sequence_item_config' and 'components' can be defined for an activity item."
    if prompt_config.sequence_item_config:
        return prompt_sequence(prompt_config)
    if prompt_config.components:
        return prompt_composite(prompt_config)
    return prompt_single(prompt_config)
