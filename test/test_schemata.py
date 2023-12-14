import json
from typing import Any, Union

from jsonschema import validate

from .util import TDataPaths as tdp


def read_file_pair(basename: str) -> tuple[Union[dict, list], dict[str, Any]]:
    with open(tdp.default_data_dir / f"{basename}.json") as f:
        contents = json.load(f)
    with open(tdp.root_dir / f"schemata/{basename}-schema.json") as f:
        schema_contents = json.load(f)

    return contents, schema_contents


def test_validate_default_config() -> None:
    parsed, schema_parsed = read_file_pair("declaration/config")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "declaration/config.json is not valid."


def test_validate_default_calendar() -> None:
    parsed, schema_parsed = read_file_pair("declaration/calendar")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "declaration/calendar.json is not valid."


def test_validate_default_roadmaps() -> None:
    parsed, schema_parsed = read_file_pair("declaration/roadmaps")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "declaration/roadmaps.json is not valid."


def test_validate_default_routines() -> None:
    parsed, schema_parsed = read_file_pair("declaration/routines")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "declaration/routines.json is not valid."


def test_validate_default_tracking() -> None:
    parsed, schema_parsed = read_file_pair("declaration/tracking")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "declaration/tracking.json is not valid."


def test_validate_default_plan() -> None:
    parsed, schema_parsed = read_file_pair("derivation/plan")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "derivation/plan.json is not valid."


def test_validate_default_schedules() -> None:
    parsed, schema_parsed = read_file_pair("derivation/schedules")
    try:
        validate(instance=parsed, schema=schema_parsed)
    except:
        assert False, "derivation/schedules.json is not valid."
