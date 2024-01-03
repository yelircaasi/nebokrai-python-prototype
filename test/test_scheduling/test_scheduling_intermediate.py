from nebokrai import NebokraiEntryPoint
from nebokrai.entity.base.entry import Entry
from nebokrai.entity.base.plan import Plan
from nebokrai.entity.base.schedule import Schedule, add_from_plan_and_excess
from nebokrai.entity.container.entries import Entries
from nebokrai.util.nkdatetime.nkdate import NKDate

from ..util import TDataPaths


def test_add_from_plan_and_excess__underfull() -> None:
    schedule = Schedule(
        NKDate(),
        [
            Entry(),
            Entry(),
            Entry(),
            Entry(),
            Entry(),
            Entry(),
            Entry(),
        ],
    )
    plan = Plan()
    plan.plan_dict = {
        NKDate(): [],
        NKDate(): [],
    }
    excess = Entries()

    new_schedule_expected = Schedule()
    new_excess_expected = Entries()
    new_schedule, new_excess = add_from_plan_and_excess(schedule, plan, excess)

    assert new_schedule == new_schedule_expected
    assert new_excess == new_excess_expected


def test_add_from_plan_and_excess__full() -> None:
    ...


def test_add_from_plan_and_excess__overfull() -> None:
    ...


def test_add_from_plan_and_excess__underfull_no_excess() -> None:
    ...


def test_add_from_plan_and_excess__full_no_excess() -> None:
    ...


def test_add_from_plan_and_excess__overfull_no_excess() -> None:
    ...


def test_add_from_plan_and_excess__underfull_no_plan() -> None:
    ...


def test_add_from_plan_and_excess__full_no_plan() -> None:
    ...


def test_add_from_plan_and_excess__overfull_no_plan() -> None:
    ...
