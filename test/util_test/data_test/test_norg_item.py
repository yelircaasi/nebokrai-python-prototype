from pathlib import Path
from typing import Tuple

import pytest

from planager.util import PDate, PDateTime, PTime
from planager.util.data.norg.norg import Norg
from planager.util.data.norg.norg_item import NorgItem, NorgItems


item_a_name = "Item A"
item_b_name = "Item B"

item_a_status = " "
priority_a = 50
notes_a = "Notes on Item A"
after_a_set: set[tuple[str, ...]] = {("Q",)}
after_a_str = "Q"

item_b_status = "x"
item_b_segment_string = "1-10,B"
item_b_link = "Item B Link"
parent_b_str = "A <> B <> C"
parent_b_tuple: tuple[str, ...] = ("A", "B", "C")
start_b_str = "2023-08-14"
start_b_date = PDate(2023, 8, 14)
end_b_str = "09:20"
end_b_time = PTime(9, 20)
priority_b = 80
ismovable_b_str = "false"
ismovable_b_bool = False
notes_b = "Notes on Item B"
normaltime_b = 50
idealtime_b = 60
mintime_b = 20
maxtime_b = 120
interval_b = 4
duration_b = 45
cluster_size_b = 3
tags_b_str = "X, Y, Z"
tags_b_set = {"X", "Y", "Z"}
description_b = "Description of Item B"
alignend_b_str = "false"
alignend_b_bool = False
before_b_str = "A <> B <> C, D <> E <> F, G <> H <> I"
before_b_set: set[tuple[str, ...]] = {("A", "B", "C"), ("D", "E", "F"), ("G", "H", "I")}
after_b_str = "V <> W"
after_b_set: set[tuple[str, ...]] = {("V", "W")}

item_a_string = f"""

~ ({item_a_status}) {item_a_name}
  -- priority: {priority_a}
  -- notes: {notes_a}
  -- after: {after_a_str}

  """

item_b_string = f"""

~ ({item_b_status}) [{item_b_name}]{{:{item_b_link}:}} || {item_b_segment_string}
  -- parent: {parent_b_str}
  -- start: {start_b_str}
  -- end: {end_b_str}
  -- priority: {priority_b}
  -- ismovable: {ismovable_b_str}
  -- notes: {notes_b}
  -- normaltime: {normaltime_b}
  -- idealtime: {idealtime_b}
  -- mintime: {mintime_b}
  -- maxtime: {maxtime_b}
  -- interval: {interval_b}
  -- duration: {duration_b}
  -- cluster_size: {cluster_size_b}
  -- tags: {tags_b_str}
  -- description: {description_b}
  -- alignend: {alignend_b_str}
  -- before: {before_b_str}
  -- after: {after_b_str}

"""


class NorgItemTest:
    string1 = "\n" "\n" ""
    string2 = "\n" "\n" ""
    string3 = "\n" "\n" ""
    string4 = "\n" "\n" ""
    string5 = "\n" "\n" ""

    item1 = NorgItem.from_string(string1)
    item2 = NorgItem.from_string(string2)
    item3 = NorgItem.from_string(string3)
    item4 = NorgItem.from_string(string4)
    item5 = NorgItem.from_string(string5)

    exp_item1 = NorgItem(
        head=None,
        name=None,
        path=None,
        link=None,
        status=None,
        item_id=None,
        parent=None,
        start=None,
        end=None,
        priority=None,
        ismovable=None,
        notes=None,
        normaltime=None,
        idealtime=None,
        mintime=None,
        maxtime=None,
        interval=None,
        duration=None,
        cluster_size=None,
        tags=None,
        description=None,
        alignend=None,
        before=None,
        after=None,
    )
    exp_item2 = NorgItem(
        head=None,
        name=None,
        path=None,
        link=None,
        status=None,
        item_id=None,
        parent=None,
        start=None,
        end=None,
        priority=None,
        ismovable=None,
        notes=None,
        normaltime=None,
        idealtime=None,
        mintime=None,
        maxtime=None,
        interval=None,
        duration=None,
        cluster_size=None,
        tags=None,
        description=None,
        alignend=None,
        before=None,
        after=None,
    )
    exp_item3 = NorgItem(
        head=None,
        name=None,
        path=None,
        link=None,
        status=None,
        item_id=None,
        parent=None,
        start=None,
        end=None,
        priority=None,
        ismovable=None,
        notes=None,
        normaltime=None,
        idealtime=None,
        mintime=None,
        maxtime=None,
        interval=None,
        duration=None,
        cluster_size=None,
        tags=None,
        description=None,
        alignend=None,
        before=None,
        after=None,
    )
    exp_item4 = NorgItem(
        head=None,
        name=None,
        path=None,
        link=None,
        status=None,
        item_id=None,
        parent=None,
        start=None,
        end=None,
        priority=None,
        ismovable=None,
        notes=None,
        normaltime=None,
        idealtime=None,
        mintime=None,
        maxtime=None,
        interval=None,
        duration=None,
        cluster_size=None,
        tags=None,
        description=None,
        alignend=None,
        before=None,
        after=None,
    )
    exp_item5 = NorgItem(
        head=None,
        name=None,
        path=None,
        link=None,
        status=None,
        item_id=None,
        parent=None,
        start=None,
        end=None,
        priority=None,
        ismovable=None,
        notes=None,
        normaltime=None,
        idealtime=None,
        mintime=None,
        maxtime=None,
        interval=None,
        duration=None,
        cluster_size=None,
        tags=None,
        description=None,
        alignend=None,
        before=None,
        after=None,
    )

    exp_string1 = "\n" "\n" ""
    exp_string2 = "\n" "\n" ""
    exp_string3 = "\n" "\n" ""
    exp_string4 = "\n" "\n" ""
    exp_string5 = "\n" "\n" ""

    def test_init(self) -> None:
        assert self.item1
        assert self.item2
        assert self.item3
        assert self.item4
        assert self.item5

    def test_convert_head(self) -> None:
        assert True

    def test_name(self) -> None:
        assert self.item1.name == ""
        assert self.item2.name == ""
        assert self.item3.name == ""
        assert self.item4.name == ""
        assert self.item5.name == ""

    def test_path(self) -> None:
        assert self.item1.path == Path("")
        assert self.item2.path == Path("")
        assert self.item3.path == Path("")
        assert self.item4.path == Path("")
        assert self.item5.path == Path("")

    def test_link(self) -> None:
        assert self.item1.link == ""
        assert self.item2.link == ""
        assert self.item3.link == ""
        assert self.item4.link == ""
        assert self.item5.link == ""

    def test_isdone(self) -> None:
        assert self.item1.isdone
        assert self.item2.isdone
        assert not self.item3.isdone
        assert not self.item4.isdone
        assert self.item5.isdone

    def test_status(self) -> None:
        assert self.item1.status == "x"
        assert self.item2.status == " "
        assert self.item3.status == "?"
        assert self.item4.status == "x"
        assert self.item5.status == " "

    def test_segment_string(self) -> None:
        assert self.item1.segment_string == ""
        assert self.item2.segment_string == ""
        assert self.item3.segment_string == ""
        assert self.item4.segment_string == ""
        assert self.item5.segment_string == ""

    def test_start_date(self) -> None:
        assert self.item1.start_date == PDate(0, 0, 0)
        assert self.item2.start_date == PDate(0, 0, 0)
        assert self.item3.start_date == PDate(0, 0, 0)
        assert self.item4.start_date == PDate(0, 0, 0)
        assert self.item5.start_date == PDate(0, 0, 0)

    def test_start_time(self) -> None:
        assert self.item1.start_time == PTime(0, 0)
        assert self.item2.start_time == PTime(0, 0)
        assert self.item3.start_time == PTime(0, 0)
        assert self.item4.start_time == PTime(0, 0)
        assert self.item5.start_time == PTime(0, 0)

    def test_start_string(self) -> None:
        assert self.item1.start_string == ""
        assert self.item2.start_string == ""
        assert self.item3.start_string == ""
        assert self.item4.start_string == ""
        assert self.item5.start_string == ""

    def test_end_date(self) -> None:
        assert self.item1.end_date == PDate(0, 0, 0)
        assert self.item2.end_date == PDate(0, 0, 0)
        assert self.item3.end_date == PDate(0, 0, 0)
        assert self.item4.end_date == PDate(0, 0, 0)
        assert self.item5.end_date == PDate(0, 0, 0)

    def test_end_time(self) -> None:
        assert self.item1.end_time == PTime(0, 0)
        assert self.item2.end_time == PTime(0, 0)
        assert self.item3.end_time == PTime(0, 0)
        assert self.item4.end_time == PTime(0, 0)
        assert self.item5.end_time == PTime(0, 0)

    def test_end_string(self) -> None:
        assert self.item1.end_string == ""
        assert self.item2.end_string == ""
        assert self.item3.end_string == ""
        assert self.item4.end_string == ""
        assert self.item5.end_string == ""

    def test_convert_int(self) -> None:
        assert NorgItem.convert_int("6") == 6
        assert NorgItem.convert_int("57") == 57
        assert NorgItem.convert_int("-14") == -14
        assert NorgItem.convert_int("0") == 0
        assert NorgItem.convert_int("10000") == 10000

    def test_convert_bool(self) -> None:
        assert NorgItem.convert_bool(True) == True
        assert NorgItem.convert_bool("true") == True
        assert NorgItem.convert_bool("True") == True
        assert NorgItem.convert_bool(False) == False
        assert NorgItem.convert_bool("false") == False
        assert NorgItem.convert_bool("False") == False

    def test_convert_tags(self) -> None:
        assert NorgItem.convert_tags("") == ...
        assert NorgItem.convert_tags("") == ...
        assert NorgItem.convert_tags("") == ...
        assert NorgItem.convert_tags({"", ""}) == ...
        assert NorgItem.convert_tags({""}) == ...

    def test_convert_tuple(self) -> None:
        assert NorgItem.convert_tuple("") == {""}
        assert NorgItem.convert_tuple("") == {"", ""}
        assert NorgItem.convert_tuple("") == {"", ""}
        assert NorgItem.convert_tuple(("", "")) == {""}
        assert NorgItem.convert_tuple(("", "")) == {"", ""}

    def test_convert_tupleset(self) -> None:
        assert NorgItem.convert_tupleset("") == {"", ""}
        assert NorgItem.convert_tupleset("") == {"", ""}
        assert NorgItem.convert_tupleset("") == {"", ""}
        assert NorgItem.convert_tupleset({("", "", "")}) == {""}
        assert NorgItem.convert_tupleset({("", "", ""), ("", "", "")}) == {"", ""}

    def test_str(self) -> None:
        assert str(self.item1) == self.exp_string1
        assert str(self.item2) == self.exp_string2
        assert str(self.item3) == self.exp_string3
        assert str(self.item4) == self.exp_string4
        assert str(self.item5) == self.exp_string5


class NorgItemsTest:
    string1 = "\n" "\n" ""
    string2 = "\n" "\n" ""

    items1 = NorgItems.from_string(string1)
    items2 = NorgItems.from_string(string2)

    exp_items1 = NorgItems()
    exp_items2 = NorgItems()

    def test_init(self) -> None:
        assert self.exp_items1
        assert self.exp_items2

    def test_from_string(self) -> None:
        assert self.items1
        assert self.items2

    def test_iter(self) -> None:
        assert list(self.items1)
        assert list(self.items2)

    def test_getitem(self) -> None:
        assert self.items1[0]
        assert self.items1[1]
        assert self.items2[0]
        assert self.items2[1]
