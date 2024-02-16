from nebokrai import NebokraiEntryPoint
from nebokrai.entity.base.entry import Entry
from nebokrai.entity.base.plan import Plan
from nebokrai.entity.base.schedule import (
    Schedule,
    add_from_plan_and_excess,
    add_to_blocks,
    assert_plan_and_date,
    entries_from_plan_and_excess,
    zip_flex_and_fixed,
)
from nebokrai.entity.container.entries import Entries
from nebokrai.util.nkdatetime.nkdate import NKDate

from ..util import TDataPaths


def test_entries_from_plan_and_excess() -> None:
    plan = Plan()
    excess = Entries()
    date = NKDate()
    entries_expected = Entries()
    entries = entries_from_plan_and_excess(plan, excess, date)

    assert entries == entries_expected


def test_add_to_blocks() -> None:
    schedule = Schedule()
    entries = Entries()
    new_schedule_expected = Schedule()
    new_entries_expected = Entries()
    new_schedule, new_entries = add_to_blocks(schedule, entries)

    assert new_schedule == new_schedule_expected
    assert new_entries == new_entries_expected


def test_zip_flex_and_fixed() -> None:
    flex_entries = []
    fixed_entries = []
    new_entries_expected = Entries()
    new_entries = zip_flex_and_fixed(flex_entries, fixed_entries)

    assert new_entries == new_entries_expected


def test_assert_plan_and_date() -> None:
    plan = Plan()
    date = NKDate()
    assert assert_plan_and_date(plan, date)

    plan = Plan()
    date = NKDate()
    assert not assert_plan_and_date(plan, date)

    plan = Plan()
    date = NKDate()
    assert not assert_plan_and_date(plan, date)

    plan = Plan()
    date = NKDate()
    assert not assert_plan_and_date(plan, date)


def test_Schedule_can_be_added() -> None:
    schedule = Schedule()
    entry = Entry()

    assert schedule.can_be_added(entry)

    schedule = Schedule()
    entry = Entry()

    assert not schedule.can_be_added(entry)


def test_Schedule_empty_time() -> None:
    schedule = Schedule()
    empty_time_expected = ...

    assert schedule.empty_time == empty_time_expected


def test_Schedule_total_available() -> None:
    schedule = Schedule()
    total_available_expected = ...

    assert schedule.total_available == total_available_expected


def test_Schedule_available_dict() -> None:
    schedule = Schedule()
    available_dict_expected = {}

    assert schedule.available_dict == available_dict_expected


def test_Schedule_get_flex_entries_and_fixed_clusters() -> None:
    schedule = Schedule()
    entries = Entries()
    flex_expected = Entries()
    fixed_expected = Entries()
    flex, fixed = schedule.get_flex_entries_and_fixed_clusters(entries)

    assert flex == flex_expected
    assert fixed == fixed_expected


def test_Schedule_is_valid() -> None:
    schedule = Schedule()
    assert schedule.is_valid

    schedule = Schedule()
    assert not schedule.is_valid


def test_Schedule_summary() -> None:
    schedule = Schedule()
    summary_expected = ""

    assert schedule.summary == summary_expected


def test_() -> None:
    assert True


#     schedule = Schedule()


# def test_() -> None:
#     schedule = Schedule()


# def test_() -> None:
#     schedule = Schedule()
