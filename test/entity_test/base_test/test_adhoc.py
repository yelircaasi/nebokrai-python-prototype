from pathlib import Path
import pytest

from planager.entity.base.adhoc import AdHoc
from planager.entity.base.entry import Entry
from planager.entity.container.entries import Entries
from planager.util.pdatetime.pdate import PDate
from planager.util.pdatetime.ptime import PTime


class AdHocTest:
    adhoc1 = AdHoc()
    adhoc2 = AdHoc()
    adhoc3 = AdHoc()

    exp_string1 = "\n" "\n" "\n" "\n"
    exp_string2 = "\n" "\n" "\n" "\n"
    exp_string3 = "\n" "\n" "\n" "\n"

    exp_norg_string1 = "\n" "\n" "\n" "\n"
    exp_norg_string2 = "\n" "\n" "\n" "\n"
    exp_norg_string3 = "\n" "\n" "\n" "\n"

    exp_json_string1 = "\n" "\n" "\n" "\n"
    exp_json_string2 = "\n" "\n" "\n" "\n"
    exp_json_string3 = "\n" "\n" "\n" "\n"

    exp_html_string1 = "\n" "\n" "\n" "\n"
    exp_html_string2 = "\n" "\n" "\n" "\n"
    exp_html_string3 = "\n" "\n" "\n" "\n"

    def test_init(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1
        assert self.adhoc2
        assert self.adhoc3

    def test_from_norg_workspace(self):
        """
        Cases:
        1)
        2)
        3)
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        assert AdHoc.from_norg_workspace(path1) == self.adhoc1
        assert AdHoc.from_norg_workspace(path2) == self.adhoc2
        assert AdHoc.from_norg_workspace(path3) == self.adhoc3

    def test_from_norg(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert AdHoc.from_norg(self.exp_norg_string1) == self.adhoc1
        assert AdHoc.from_norg(self.exp_norg_string2) == self.adhoc2
        assert AdHoc.from_norg(self.exp_norg_string3) == self.adhoc3

    def test_from_json(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert AdHoc.from_json(self.exp_json_string1) == self.adhoc1
        assert AdHoc.from_json(self.exp_json_string2) == self.adhoc2
        assert AdHoc.from_json(self.exp_json_string3) == self.adhoc3

    def test_from_html(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert AdHoc.from_html(self.exp_html_string1) == self.adhoc1
        assert AdHoc.from_html(self.exp_html_string2) == self.adhoc2
        assert AdHoc.from_html(self.exp_html_string3) == self.adhoc3

    def test_copy(self) -> None:
        assert self.adhoc1 == AdHoc(Entries([Entry("", PTime(0, 0))]))
        assert self.adhoc2 == AdHoc(Entries([Entry("", PTime(0, 0))]))
        assert self.adhoc3 == AdHoc(Entries([Entry("", PTime(0, 0))]))

    def test_to_norg(self):
        """
        Cases:
        1)
        2)
        3)
        """
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
        """
        Cases:
        1)
        2)
        3)
        """
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
        """
        Cases:
        1)
        2)
        3)
        """
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
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1.to_norg_string() == self.exp_norg_string1
        assert self.adhoc2.to_norg_string() == self.exp_norg_string2
        assert self.adhoc3.to_norg_string() == self.exp_norg_string3

    def test_to_json_string(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1.to_json_string() == self.exp_json_string1
        assert self.adhoc2.to_json_string() == self.exp_json_string2
        assert self.adhoc3.to_json_string() == self.exp_json_string3

    def test_to_html_string(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1.to_html_string() == self.exp_html_string1
        assert self.adhoc2.to_html_string() == self.exp_html_string2
        assert self.adhoc3.to_html_string() == self.exp_html_string3

    def test_start_date(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1.start_date == PTime(0, 0)
        assert self.adhoc2.start_date == PTime(0, 0)
        assert self.adhoc3.start_date == PTime(0, 0)

    def test_end_date(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1.end_date == PTime(0, 0)
        assert self.adhoc2.end_date == PTime(0, 0)
        assert self.adhoc3.end_date == PTime(0, 0)

    def test_pretty(self):
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1.pretty() == self.exp_string1
        assert self.adhoc2.pretty() == self.exp_string2
        assert self.adhoc3.pretty() == self.exp_string3

    def test_getitem(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert self.adhoc1[PDate(0, 0, 0)] == Entries([])
        assert self.adhoc2[PDate(0, 0, 0)] == Entries([])
        assert self.adhoc3[PDate(0, 0, 0)] == Entries([])

    def test_str(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert str(self.adhoc1) == self.exp_string1
        assert str(self.adhoc2) == self.exp_string2
        assert str(self.adhoc3) == self.exp_string3

    def test_repr(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        assert repr(self.adhoc1) == self.exp_string1
        assert repr(self.adhoc2) == self.exp_string2
        assert repr(self.adhoc3) == self.exp_string3
