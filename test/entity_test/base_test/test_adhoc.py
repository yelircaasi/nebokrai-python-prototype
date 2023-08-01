from pathlib import Path
import pytest

from planager.entity.base.adhoc import AdHoc
from planager.entity.base.entry import Entry
from planager.util.pdatetime.pdate import PDate


class AdHocTest:
    adhoc1 = AdHoc()
    adhoc2 = AdHoc()
    adhoc3 = AdHoc()

    exp_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )

    exp_norg_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_norg_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_norg_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )

    exp_json_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_json_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_json_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )

    exp_html_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_html_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    exp_html_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )

    def test_init(self):
        assert self.adhoc1
        assert self.adhoc2
        assert self.adhoc3

    def test_from_norg_workspace(self):
        path1 = Path()
        path2 = Path()
        path3 = Path()

        assert AdHoc.from_norg_workspace(path1) == self.adhoc1
        assert AdHoc.from_norg_workspace(path2) == self.adhoc2
        assert AdHoc.from_norg_workspace(path3) == self.adhoc3

    def test_from_norg(self):
        assert AdHoc.from_norg(self.exp_norg_string1) == self.adhoc1
        assert AdHoc.from_norg(self.exp_norg_string2) == self.adhoc2
        assert AdHoc.from_norg(self.exp_norg_string3) == self.adhoc3

    def test_from_json(self):
        assert AdHoc.from_json(self.exp_json_string1) == self.adhoc1
        assert AdHoc.from_json(self.exp_json_string2) == self.adhoc2
        assert AdHoc.from_json(self.exp_json_string3) == self.adhoc3

    def test_from_html(self):
        assert AdHoc.from_html(self.exp_html_string1) == self.adhoc1
        assert AdHoc.from_html(self.exp_html_string2) == self.adhoc2
        assert AdHoc.from_html(self.exp_html_string3) == self.adhoc3

    def test_to_norg(self):
        tmp_path = Path()

        self.adhoc1.to_norg(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string1

        self.adhoc2.to_norg(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string2

        self.adhoc3.to_norg(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string3

    def test_to_json(self):
        tmp_path = Path()

        self.adhoc1.to_json(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string1

        self.adhoc2.to_json(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string2

        self.adhoc3.to_json(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string3

    def test_to_html(self):
        tmp_path = Path()

        self.adhoc1.to_html(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string1

        self.adhoc2.to_html(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string2

        self.adhoc3.to_html(tmp_path)
        with open(tmp_path) as f:
            saved = f.read()
        assert saved == self.exp_json_string3

    def test_to_norg_string(self):
        assert self.adhoc1.to_norg_string() == self.exp_norg_string1
        assert self.adhoc2.to_norg_string() == self.exp_norg_string2
        assert self.adhoc3.to_norg_string() == self.exp_norg_string3

    def test_to_json_string(self):
        assert self.adhoc1.to_json_string() == self.exp_json_string1
        assert self.adhoc2.to_json_string() == self.exp_json_string2
        assert self.adhoc3.to_json_string() == self.exp_json_string3

    def test_to_html_string(self):
        assert self.adhoc1.to_html_string() == self.exp_html_string1
        assert self.adhoc2.to_html_string() == self.exp_html_string2
        assert self.adhoc3.to_html_string() == self.exp_html_string3

    def test_start_date(self):
        assert self.adhoc1.start_date == PDate()
        assert self.adhoc2.start_date == PDate()
        assert self.adhoc3.start_date == PDate()

    def test_end_date(self):
        assert self.adhoc1.end_date == PDate()
        assert self.adhoc2.end_date == PDate()
        assert self.adhoc3.end_date == PDate()

    def test_pretty(self):
        assert self.adhoc1.pretty() == self.exp_string1
        assert self.adhoc2.pretty() == self.exp_string2
        assert self.adhoc3.pretty() == self.exp_string3

    def test_getitem(self) -> None:
        assert self.adhoc1[2] == Entry()
        assert self.adhoc2[4] == Entry()
        assert self.adhoc3[-1] == Entry()

    def test_setitem(self) -> None:
        cal1 = self.adhoc1.copy()
        cal2 = self.adhoc2.copy()
        cal3 = self.adhoc3.copy()

        date1 = PDate()
        date2 = PDate()
        date3 = PDate()

        entry1 = Entry()
        entry2 = Entry()
        entry3 = Entry()

        cal1[date1] = entry1
        cal2[date2] = entry1
        cal3[date3] = entry1

        assert cal1[date1] == entry1
        assert cal2[date2] == entry2
        assert cal3[date3] == entry3

    def test_str(self) -> None:
        assert str(self.adhoc1) == self.exp_string1
        assert str(self.adhoc2) == self.exp_string2
        assert str(self.adhoc3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.adhoc1) == self.exp_string1
        assert repr(self.adhoc2) == self.exp_string2
        assert repr(self.adhoc3) == self.exp_string3
