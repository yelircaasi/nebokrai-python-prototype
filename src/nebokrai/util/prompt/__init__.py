import re
from dataclasses import dataclass
from typing import Any, Callable, Iterable, NamedTuple, Optional

from ..elementary_types import Natural, PromptTypeName, TrackingActivityResponseType
from ..nkdatetime import NKTime
from ..serde.custom_dict_types import (
    PromptDispatcherType,
    TimedDistance,
    TimedDistanceWithElevation,
)
from .prompt_config import PromptConfig

__all__ = ["PromptConfig", "prompt_any", "prompt_configs"]


def prompt_atomic(prompt_config: "PromptConfig") -> Optional[TrackingActivityResponseType]:
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


def prompt_composite(prompt_config: PromptConfig) -> dict[str, TrackingActivityResponseType]:
    """
    Run the input prompt corresponding to types with subfields.
    """
    assert prompt_config.components is not None
    ret: dict[str, TrackingActivityResponseType] = {}
    for k, kconfig in prompt_config.components.items():
        parsed_response: TrackingActivityResponseType = prompt_any(kconfig)
        ret.update({k: parsed_response})
    return ret


def prompt_sequence(prompt_config: "PromptConfig") -> list[TrackingActivityResponseType]:
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


def prompt_any(prompt_config: PromptConfig) -> TrackingActivityResponseType:
    """
    Run whichever type of prompt is appropriate for the configuration supplied.
    """
    assert not (
        prompt_config.sequence_item_config and prompt_config.components
    ), "At most one of 'sequence_item_config' and 'components' can be defined for an activity item."
    if prompt_config.sequence_item_config:
        return prompt_sequence(prompt_config)
    if prompt_config.components:
        return prompt_composite(prompt_config)
    return prompt_atomic(prompt_config)
