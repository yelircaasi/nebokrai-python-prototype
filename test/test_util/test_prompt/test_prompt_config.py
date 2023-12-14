from nebokrai.util.prompt import PromptConfig
from nebokrai.util.serde.custom_dict_types import (
    ComponentsDictParsed,
    SubitemDictParsed,
)


def test_from_components_dict_simple() -> None:
    components_dict: ComponentsDictParsed = {}


def test_from_components_dict_complex() -> None:
    components_dict: ComponentsDictParsed = {}


def test_from_subitem_dict_simple() -> None:
    subitem_dict: SubitemDictParsed = {
        "name": "",
        "dtype": "text",
    }


def test_from_subitem_dict_complex() -> None:
    subitem_dict: SubitemDictParsed = {
        "name": "",
        "dtype": "text",
    }
