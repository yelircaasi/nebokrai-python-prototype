import re

import pytest

from planager.util.regex import Regexes


class RegexesTest:
    def test_item_split(self) -> None:
        s1 = "\n\n-- hey \n\n-- new_item: item value\n\n"
        s2 = "some text\n-- item 1\n    item 1 text\n\n-- item 2"

        exp1 = ["", "hey", "new_item: item value\n\n"]
        exp2 = ["some text", "item 1\n    item 1 text", "item 2"]

        assert re.split(Regexes.item_split, s1) == exp1
        assert re.split(Regexes.item_split, s2) == exp2

    def test_item1_split(self) -> None:
        s1 = "\n\n- hey \n\n- new_item: item value\n\n"
        s2 = "some text\n~ item 1\n    item 1 text\n\n~ item 2"

        exp1 = ["", "hey", "new_item: item value\n\n"]
        exp2 = ["some text", "item 1\n    item 1 text", "item 2"]

        assert re.split(Regexes.item1_split, s1) == exp1
        assert re.split(Regexes.item1_split, s2) == exp2

    def test_header_and_body(self) -> None:
        s1 = "@document.meta\ntitle: title\n@end\n\nbody here\nanother line"

        exp1 = ("title: title", "\nbody here\nanother line")

        rs = re.search(Regexes.header_and_body, s1)
        assert rs and (rs.groups() == exp1)

    def test_link_namefirst(self) -> None:
        s1 = "[name]{:link:}"
        s2 = "[name with spaces]{:link with spaces:}"
        s3 = "[Name with sp@ces and $pecial c#ars _ ]{:Link with sp@ces and $pecial c#ars _ :}"

        exp1 = ("name", "link")
        exp2 = ("name with spaces", "link with spaces")
        exp3 = (
            "Name with sp@ces and $pecial c#ars _ ",
            "Link with sp@ces and $pecial c#ars _ ",
        )

        rs = re.search(Regexes.link_namefirst, s1)
        assert rs and (rs.groups() == exp1)
        rs = re.search(Regexes.link_namefirst, s2)
        assert rs and (rs.groups() == exp2)
        rs = re.search(Regexes.link_namefirst, s3)
        assert rs and (rs.groups() == exp3)

    def test_attribute_pair(self) -> None:
        s1 = "   -- att_name: att_val  "
        s2 = "-- att_name: att_val"
        s3 = " \n  -- att_name : att_val with spaces  \n more text"

        exp1 = ("att_name", "att_val")
        exp3 = ("att_name", "att_val with spaces")

        rs = re.search(Regexes.attribute_pair, s1)
        assert rs and (rs.groups() == exp1)
        rs = re.search(Regexes.attribute_pair, s2)
        assert rs and (rs.groups() == exp1)
        rs = re.search(Regexes.attribute_pair, s3)
        assert rs and (rs.groups() == exp3)

    def test_name_and_segments(self) -> None:
        s1 = "  name here  ||  1-10, A   \n\n"
        s2 = "\n  #Name || segment1, segment 2, segment3   "
        s3 = "\n  #Name || segment1, segment 2, segment3 \n\n  "

        assert re.search(Regexes.name_and_segments, s1)
        assert re.search(Regexes.name_and_segments, s2)
        assert re.search(Regexes.name_and_segments, s3)
