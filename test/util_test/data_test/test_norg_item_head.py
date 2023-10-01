from pathlib import Path
from typing import Tuple

import pytest

from planager.util.data.norg.norg_item_head import NorgItemHead


class NorgItemHeadTest:
    head1 = NorgItemHead.from_string("item head 1")
    head2 = NorgItemHead.from_string("  -- item head 2 ")
    head3 = NorgItemHead.from_string("\n  -- Item Head 3  \n\n")
    head4 = NorgItemHead.from_string("\n  -- ( ) Item Head 4  \n\n")
    head5 = NorgItemHead.from_string("\n  -- (x) Item Head 5  \n\n")
    head6 = NorgItemHead.from_string("\n  -- ( ) Item Head 6, with $pecial ch#rs  \n\n")
    head7 = NorgItemHead.from_string("\n  -- (x) Item Head 7 || 1-10,A1-A5  \n\n  ")
    head8 = NorgItemHead.from_string("  -- [item head 8]{:item head link 8:} ")
    head9 = NorgItemHead.from_string(
        "\n  -- (x) [Item Head 9]{:item head 9 link:} || 1-10,A1-A5  \n\n  "
    )

    exp_string1 = ""
    exp_string2 = ""
    exp_string3 = ""
    exp_string4 = ""
    exp_string5 = ""
    exp_string6 = ""
    exp_string7 = ""
    exp_string8 = ""
    exp_string9 = ""

    def test_init(self) -> None:
        head1 = NorgItemHead("")
        head2 = NorgItemHead("")

        assert head1
        assert head2

    def test_from_string(self) -> None:
        assert self.head1.path
        assert self.head8.path
        assert self.head9.path

    def test_path(self) -> None:
        assert self.head1
        assert self.head2
        assert self.head3
        assert self.head4
        assert self.head5
        assert self.head6
        assert self.head7
        assert self.head8
        assert self.head9

    def test_path_setter(self) -> None:
        head1 = NorgItemHead("")
        head2 = NorgItemHead("")

        path1 = Path("...")
        path2 = Path("...")

        head1.path = path1
        head2.path = path2

        assert head1.path == path1
        assert head2.path == path2

    def test_as_norg(self) -> None:
        assert str(self.head1) == self.exp_string1
        assert str(self.head2) == self.exp_string2
        assert str(self.head3) == self.exp_string3
        assert str(self.head4) == self.exp_string4
        assert str(self.head5) == self.exp_string5
        assert str(self.head6) == self.exp_string6
        assert str(self.head7) == self.exp_string7
        assert str(self.head8) == self.exp_string8
        assert str(self.head9) == self.exp_string9

    def test_str(self) -> None:
        assert str(self.head1) == self.exp_string1
        assert str(self.head2) == self.exp_string2
        assert str(self.head3) == self.exp_string3
        assert str(self.head4) == self.exp_string4
        assert str(self.head5) == self.exp_string5
        assert str(self.head6) == self.exp_string6
        assert str(self.head7) == self.exp_string7
        assert str(self.head8) == self.exp_string8
        assert str(self.head9) == self.exp_string9

    def test_repr(self) -> None:
        assert str(self.head1) == self.exp_string1
        assert str(self.head2) == self.exp_string2
        assert str(self.head3) == self.exp_string3
        assert str(self.head4) == self.exp_string4
        assert str(self.head5) == self.exp_string5
        assert str(self.head6) == self.exp_string6
        assert str(self.head7) == self.exp_string7
        assert str(self.head8) == self.exp_string8
        assert str(self.head9) == self.exp_string9

    def test_bool(self) -> None:
        assert self.head1
        assert self.head2
        assert self.head3
        assert self.head4
        assert self.head5
        assert self.head6
        assert self.head7
        assert self.head8
        assert self.head9
