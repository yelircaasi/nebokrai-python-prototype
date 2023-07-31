from pathlib import Path
from typing import Set, Tuple

import pytest

from planager.util import PDate, PDateTime, PTime
from planager.util.data.norg.norg import Norg
from planager.util.data.norg.norg_item import NorgItem, NorgItems


title = "Test Title"
description = "Test Description"
author = "Test Author"
doc_id = "Test Doc ID"
parent = "Test Parent"
updated = PDateTime.now()
categories = ""
item_a_name = "Item A"
item_b_name = "Item B"

item_a_status = " "
priority_a = 50
notes_a = "Notes on Item A"
after_a_set: Set[Tuple[str, ...]] = {("Q",)}
after_a_str = "Q"

item_b_status = "x"
item_b_segment_string = "1-10,B"
item_b_link = "Item B Link"
parent_b_str = "A :: B :: C"
parent_b_tuple: Tuple[str, ...] = ("A", "B", "C")
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
before_b_str = "A :: B :: C, D :: E :: F, G :: H :: I"
before_b_set: Set[Tuple[str, ...]] = {("A", "B", "C"), ("D", "E", "F"), ("G", "H", "I")}
after_b_str = "V :: W"
after_b_set: Set[Tuple[str, ...]] = {("V", "W")}

norg_string1 = f"""@document.meta
title: {title}
description: {description}
categories: {categories}
id: {doc_id}
parent: {parent}
updated: {str(updated)}
author: {author}
@end

~ ({item_a_status}) {item_a_name}
  -- priority: {priority_a}
  -- notes: {notes_a}
  -- after: {after_a_str}

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
norg_string2 = """

"""
norg_string3 = """

"""
norg_string4 = """

"""
norg_string5 = """

"""
norg_string6 = """

"""
norg_string7 = """

"""

path1 = Path(__file__).parent.parent.parent / "data" / "norg1.norg"
with open(path1, 'w') as f:
    f.write(norg_string1)


class NorgTest:
    def test_init(self) -> None:
        items = NorgItems(
            [
                NorgItem(
                    item_a_name, priority=priority_a, notes=notes_a, after=after_a_set
                ),
                NorgItem(
                    name=item_b_name,
                    link=item_b_link,
                    status=item_b_status,
                    ismovable=ismovable_b_bool,
                    maxtime=maxtime_b,
                    before=before_b_set,
                ),
            ]
        )

        norg1 = Norg(
            title=title,
            description=description,
            author=author,
            doc_id=doc_id,
            parent=parent,
            updated=updated,
            categories=categories,
            items=items,
        )

        assert norg1.title == title
        assert norg1.description == description
        assert norg1.author == author
        assert norg1.doc_id == doc_id
        assert norg1.parent == parent
        assert norg1.updated == updated
        assert norg1.categories == categories

        item_a = norg1.items[0]
        item_b = norg1.items[1]

        assert item_a.name == item_a_name
        assert item_a.status == item_a_status
        assert item_a.priority == priority_a
        assert item_a.notes == notes_a
        assert item_a.dependencies == after_a_set

        assert item_b.name == item_b_name
        assert item_b.status == item_b_status
        assert item_b.link == item_b_link
        assert item_b.ismovable == ismovable_b_bool
        assert item_b.maxtime == maxtime_b
        assert item_b.before == before_b_set
'''
    def test_from_path(self) -> None:
        norg1 = Norg.from_path(path1)

        assert norg1.title == title
        assert norg1.description == description
        assert norg1.author == author
        assert norg1.doc_id == doc_id
        assert norg1.parent == parent
        assert norg1.updated == updated
        assert norg1.categories == categories

        item_a = norg1.items[0]
        item_b = norg1.items[1]

        assert item_a.name == item_a_name
        assert item_a.status == item_a_status
        assert item_a.priority == priority_a
        assert item_a.notes == notes_a
        assert item_a.dependencies == after_a_set

        assert item_b.name == item_b_name
        assert item_b.status == item_b_status
        assert item_b.link == item_b_link
        assert item_b.parent == parent_b_tuple
        assert item_b.start_date == start_b_date
        assert item_b.end_time == end_b_time
        assert item_b.priority == priority_b
        assert item_b.ismovable == ismovable_b_bool
        assert item_b.notes == notes_b
        assert item_b.normaltime == normaltime_b
        assert item_b.idealtime == idealtime_b
        assert item_b.mintime == mintime_b
        assert item_b.maxtime == maxtime_b
        assert item_b.interval == interval_b
        assert item_b.duration == duration_b
        assert item_b.cluster_size == cluster_size_b
        assert item_b.tags == tags_b_set
        assert item_b.description == description_b
        assert item_b.alignend == alignend_b_bool
        assert item_b.before == before_b_set
        assert item_b.dependencies == after_b_set

    def test_from_string(self) -> None:
        norg1 = Norg.from_string(norg_string1)

        assert norg1.title == title
        assert norg1.description == description
        assert norg1.author == author
        assert norg1.doc_id == doc_id
        assert norg1.parent == parent
        assert norg1.updated == updated
        assert norg1.categories == categories

        item_a = norg1.items[0]
        item_b = norg1.items[1]

        assert item_a.name == item_a_name
        assert item_a.status == item_a_status
        assert item_a.priority == priority_a
        assert item_a.notes == notes_a
        assert item_a.dependencies == after_a_set

        assert item_b.name == item_b_name
        assert item_b.status == item_b_status
        assert item_b.link == item_b_link
        assert item_b.parent == parent_b_tuple
        assert item_b.start_date == start_b_date
        assert item_b.end_time == end_b_time
        assert item_b.priority == priority_b
        assert item_b.ismovable == ismovable_b_bool
        assert item_b.notes == notes_b
        assert item_b.normaltime == normaltime_b
        assert item_b.idealtime == idealtime_b
        assert item_b.mintime == mintime_b
        assert item_b.maxtime == maxtime_b
        assert item_b.interval == interval_b
        assert item_b.duration == duration_b
        assert item_b.cluster_size == cluster_size_b
        assert item_b.tags == tags_b_set
        assert item_b.description == description_b
        assert item_b.alignend == alignend_b_bool
        assert item_b.before == before_b_set
        assert item_b.dependencies == after_b_set

    def test_str(self) -> None:
        norg1 = Norg.from_string(norg_string1)

        assert norg_string1 == str(norg1)

    def test_norg_item(self) -> None:
        assert True

    def test_norg_item_from_string(self) -> None:
        assert True

    def test_norg_item_head(self) -> None:
        assert True

'''
