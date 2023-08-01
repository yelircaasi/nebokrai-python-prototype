import pytest

from planager.entity.base.entry import Entry, Empty, FIRST_ENTRY, LAST_ENTRY
from planager.util.pdatetime import PTime


class EntryTest:
    entry1 = Entry()
    entry2 = Entry()
    entry3 = Entry()
    entry4 = Entry()
    entry5 = Entry()
    entry6 = Entry()
    entry7 = Entry()

    exp_string1 = "\n".join(
        "",
        "",
        "",
        "",
    )
    exp_string2 = "\n".join(
        "",
        "",
        "",
        "",
    )
    exp_string3 = "\n".join(
        "",
        "",
        "",
        "",
    )
    exp_string4 = "\n".join(
        "",
        "",
        "",
        "",
    )
    exp_string5 = "\n".join(
        "",
        "",
        "",
        "",
    )
    exp_string6 = "\n".join(
        "",
        "",
        "",
        "",
    )
    exp_string7 = "\n".join(
        "",
        "",
        "",
        "",
    )

    def test_init(self) -> None:
        assert self.entry1
        assert self.entry2
        assert self.entry3
        assert self.entry4
        assert self.entry5
        assert self.entry6
        assert self.entry7

    def test_copy(self) -> None:
        copy1 = self.entry1.copy()
        assert self.entry1 == copy1
        assert self.entry1.__dict__ == copy1.__dict__
        assert id(self.entry1) != id(copy1)

    def test_duration(self) -> None:
        assert self.entry1.duration
        assert self.entry2.duration
        assert self.entry3.duration
        assert self.entry4.duration
        assert self.entry5.duration
        assert self.entry6.duration
        assert self.entry7.duration

    def test_spansize(self) -> None:
        assert self.entry1.spansize()
        assert self.entry2.spansize()
        assert self.entry3.spansize()
        assert self.entry4.spansize()
        assert self.entry5.spansize()
        assert self.entry6.spansize()
        assert self.entry7.spansize()

    def test_timespan(self) -> None:
        assert self.entry1.timepspan()
        assert self.entry2.timepspan()
        assert self.entry3.timepspan()
        assert self.entry4.timepspan()
        assert self.entry5.timepspan()
        assert self.entry6.timepspan()
        assert self.entry7.timepspan()

    def test_to_norg(self) -> None:
        assert self.entry1.to_norg()
        assert self.entry2.to_norg()
        assert self.entry3.to_norg()
        assert self.entry4.to_norg()
        assert self.entry5.to_norg()
        assert self.entry6.to_norg()
        assert self.entry7.to_norg()

    def test_to_json(self) -> None:
        assert True

    def test_to_html(self) -> None:
        assert True

    def test_eq(self) -> None:
        assert self.entry1 == Entry()
        assert self.entry2 == Entry()
        assert self.entry3 == Entry()
        assert self.entry4 == Entry()
        assert self.entry5 == Entry()
        assert self.entry6 == Entry()
        assert self.entry7 == Entry()

    def test_hasmass(self) -> None:
        assert self.entry1.hasmass()
        assert self.entry2.hasmass()
        assert self.entry3.hasmass()
        assert self.entry4.hasmass()
        assert self.entry5.hasmass()
        assert self.entry6.hasmass()
        assert self.entry7.hasmass()

    def test_isbefore(self) -> None:
        assert self.entry1.isbefore()
        assert self.entry2.isbefore()
        assert self.entry3.isbefore()
        assert self.entry4.isbefore()
        assert self.entry5.isbefore()
        assert self.entry6.isbefore()
        assert self.entry7.isbefore()

    def test_isafter(self) -> None:
        assert self.entry1.isafter()
        assert self.entry2.isafter()
        assert self.entry3.isafter()
        assert self.entry4.isafter()
        assert self.entry5.isafter()
        assert self.entry6.isafter()
        assert self.entry7.isafter()

    def test_isbefore_by_start(self) -> None:
        assert self.entry1.isbefore_by_start()
        assert self.entry2.isbefore_by_start()
        assert self.entry3.isbefore_by_start()
        assert self.entry4.isbefore_by_start()
        assert self.entry5.isbefore_by_start()
        assert self.entry6.isbefore_by_start()
        assert self.entry7.isbefore_by_start()

    def test_isafter_by_start(self) -> None:
        assert self.entry1.isafter_by_start()
        assert self.entry2.isafter_by_start()
        assert self.entry3.isafter_by_start()
        assert self.entry4.isafter_by_start()
        assert self.entry5.isafter_by_start()
        assert self.entry6.isafter_by_start()
        assert self.entry7.isafter_by_start()

    def test_overlaps(self) -> None:
        assert self.entry1.overlaps()
        assert self.entry2.overlaps()
        assert self.entry3.overlaps()
        assert self.entry4.overlaps()
        assert self.entry5.overlaps()
        assert self.entry6.overlaps()
        assert self.entry7.overlaps()

    def test_overlaps_first(self) -> None:
        assert self.entry1.overlaps_first()
        assert self.entry2.overlaps_first()
        assert self.entry3.overlaps_first()
        assert self.entry4.overlaps_first()
        assert self.entry5.overlaps_first()
        assert self.entry6.overlaps_first()
        assert self.entry7.overlaps_first()

    def test_surrounds(self) -> None:
        assert self.entry1.surrounds()
        assert self.entry2.surrounds()
        assert self.entry3.surrounds()
        assert self.entry4.surrounds()
        assert self.entry5.surrounds()
        assert self.entry6.surrounds()
        assert self.entry7.surrounds()

    def test_surrounded_by(self) -> None:
        assert self.entry1.surrounded_by()
        assert self.entry2.surrounded_by()
        assert self.entry3.surrounded_by()
        assert self.entry4.surrounded_by()
        assert self.entry5.surrounded_by()
        assert self.entry6.surrounded_by()
        assert self.entry7.surrounded_by()

    def test_shares_start_shorter(self) -> None:
        assert self.entry1.shares_start_shorter()
        assert self.entry2.shares_start_shorter()
        assert self.entry3.shares_start_shorter()
        assert self.entry4.shares_start_shorter()
        assert self.entry5.shares_start_shorter()
        assert self.entry6.shares_start_shorter()
        assert self.entry7.shares_start_shorter()

    def test_shares_start_longer(self) -> None:
        assert self.entry1.shares_start_longer()
        assert self.entry2.shares_start_longer()
        assert self.entry3.shares_start_longer()
        assert self.entry4.shares_start_longer()
        assert self.entry5.shares_start_longer()
        assert self.entry6.shares_start_longer()
        assert self.entry7.shares_start_longer()

    def test_shares_end_shorter(self) -> None:
        assert self.entry1.shares_end_shorter()
        assert self.entry2.shares_end_shorter()
        assert self.entry3.shares_end_shorter()
        assert self.entry4.shares_end_shorter()
        assert self.entry5.shares_end_shorter()
        assert self.entry6.shares_end_shorter()
        assert self.entry7.shares_end_shorter()

    def test_shares_end_longer(self) -> None:
        assert self.entry1.shares_end_longer()
        assert self.entry2.shares_end_longer()
        assert self.entry3.shares_end_longer()
        assert self.entry4.shares_end_longer()
        assert self.entry5.shares_end_longer()
        assert self.entry6.shares_end_longer()
        assert self.entry7.shares_end_longer()

    def test_iscovered(self) -> None:
        assert self.entry1.iscovered()
        assert self.entry2.iscovered()
        assert self.entry3.iscovered()
        assert self.entry4.iscovered()
        assert self.entry5.iscovered()
        assert self.entry6.iscovered()
        assert self.entry7.iscovered()

    def test_trumps(self) -> None:
        assert self.entry1.trumps()
        assert self.entry2.trumps()
        assert self.entry3.trumps()
        assert self.entry4.trumps()
        assert self.entry5.trumps()
        assert self.entry6.trumps()
        assert self.entry7.trumps()

    def test_temporal_relationship(self) -> None:
        assert self.entry1.temporal_relationship()
        assert self.entry2.temporal_relationship()
        assert self.entry3.temporal_relationship()
        assert self.entry4.temporal_relationship()
        assert self.entry5.temporal_relationship()
        assert self.entry6.temporal_relationship()
        assert self.entry7.temporal_relationship()

    def test_pretty(self) -> None:
        assert self.entry1.pretty() == ...
        assert self.entry2.pretty() == ...
        assert self.entry3.pretty() == ...
        assert self.entry4.pretty() == ...
        assert self.entry5.pretty() == ...
        assert self.entry6.pretty() == ...
        assert self.entry7.pretty() == ...

    def test_str(self) -> None:
        assert str(self.entry1) == ...
        assert str(self.entry2) == ...
        assert str(self.entry3) == ...
        assert str(self.entry4) == ...
        assert str(self.entry5) == ...
        assert str(self.entry6) == ...
        assert str(self.entry7) == ...

    def test_repr(self) -> None:
        assert repr(self.entry1) == ...
        assert repr(self.entry2) == ...
        assert repr(self.entry3) == ...
        assert repr(self.entry4) == ...
        assert repr(self.entry5) == ...
        assert repr(self.entry6) == ...
        assert repr(self.entry7) == ...

    def test_fits(self) -> None:
        assert self.entry1.fits()
        assert self.entry2.fits()
        assert self.entry3.fits()
        assert self.entry4.fits()
        assert self.entry5.fits()
        assert self.entry6.fits()
        assert self.entry7.fits()


class EmptyTest:
    empty = Empty()

    def test_init(self) -> None:
        assert True


def test_FIRST_ENTRY() -> None:
    assert FIRST_ENTRY.start == PTime(0, 0)
    assert FIRST_ENTRY.end == PTime(0, 0)
    assert FIRST_ENTRY.priority < 0
    assert not FIRST_ENTRY.ismovable
    assert not FIRST_ENTRY.hasmass()


def test_LAST_ENTRY() -> None:
    assert LAST_ENTRY.start == PTime(24, 0)
    assert LAST_ENTRY.end == PTime(24, 0)
    assert LAST_ENTRY.priority < 0
    assert not LAST_ENTRY.ismovable
    assert not LAST_ENTRY.hasmass()
