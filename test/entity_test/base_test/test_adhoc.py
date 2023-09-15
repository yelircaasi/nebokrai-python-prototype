from pathlib import Path
import pytest

from planager.entity.base.adhoc import AdHoc
from planager.entity.base.entry import Entry
from planager.entity.container.entries import Entries
from planager.util.pdatetime.pdate import PDate
from planager.util.pdatetime.ptime import PTime


class AdHocTest:
    def test_init(self):
        adhoc = AdHoc()
        exp = AdHoc()

        assert adhoc == exp

    def test_from_norg_workspace(self):
        path1 = Path()
        path2 = Path()
        path3 = Path()

        adhoc1 = AdHoc()
        adhoc2 = AdHoc()
        adhoc3 = AdHoc()

        assert AdHoc.from_norg_workspace(path1) == adhoc1
        assert AdHoc.from_norg_workspace(path2) == adhoc2
        assert AdHoc.from_norg_workspace(path3) == adhoc3

    def test_from_norg(self):
        adhoc = AdHoc()
        norg_string = ()

        assert AdHoc.from_norg(norg_string) == adhoc

    def test_from_json(self):
        adhoc = AdHoc()
        json_string = ()

        assert AdHoc.from_json(json_string) == adhoc

    def test_from_html(self):
        adhoc = AdHoc()
        html_string = ()

        assert AdHoc.from_html(html_string) == adhoc

    def test_copy(self) -> None:
        adhoc = AdHoc()
        copy = adhoc.copy()

        assert adhoc.__dict__ == copy.__dict__

    def test_to_norg(self):
        adhoc = AdHoc()
        adhoc_path = Path()
        exp = ()

        adhoc.to_norg(adhoc_path)
        with open(adhoc_path) as f:
            saved = f.read()
        assert saved == exp

    def test_to_json(self):
        adhoc = AdHoc()
        adhoc_path = Path()
        exp = ()

        adhoc.to_json(adhoc_path)
        with open(adhoc_path) as f:
            saved = f.read()
        assert saved == exp

    def test_to_html(self):
        adhoc = AdHoc()
        adhoc_path = Path()
        exp = ()

        adhoc.to_html(adhoc_path)
        with open(adhoc_path) as f:
            saved = f.read()
        assert saved == exp

    def test_to_norg_string(self):
        adhoc = AdHoc()
        exp = ()

        assert adhoc.to_norg_string() == exp

    def test_to_json_string(self):
        adhoc = AdHoc()
        exp = ()

        assert adhoc.to_json_string() == exp

    def test_to_html_string(self):
        adhoc = AdHoc()
        exp = ()

        assert adhoc.to_html_string() == exp

    def test_start_date(self):
        adhoc = AdHoc()
        start = PDate()

        assert adhoc.start_date == start

    def test_end_date(self):
        adhoc = AdHoc()
        end = PDate()

        assert adhoc.end_date == end

    def test_pretty(self):
        adhoc = AdHoc()
        exp = ()
        assert adhoc.pretty() == exp

    def test_getitem(self) -> None:
        adhoc = AdHoc()
        entries = Entries()
        date = PDate()

        assert adhoc[date] == entries

    def test_str(self) -> None:
        adhoc = AdHoc()
        exp = ()
        assert str(adhoc) == exp

    def test_repr(self) -> None:
        adhoc = AdHoc()
        exp = ()
        assert repr(adhoc) == exp
