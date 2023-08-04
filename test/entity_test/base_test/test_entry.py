from pathlib import Path
import pytest

from planager.entity.base.entry import Entry, Empty, FIRST_ENTRY, LAST_ENTRY
from planager.util.pdatetime import PTime


class EntryTest:
    # []
    entry_0_5 = Entry(
        "First Entry",
        start=PTime(0),
        end=PTime(5),
        priority=70,
        ismovable=True,
        blocks={"block 1", "block 2", "block 3", "block 4"},
        categories={"category 1", "category 2", "category 3"},
        notes="notes on entry 1",
        normaltime=270,
        idealtime=330,
        mintime=240,
        maxtime=360,
        alignend=True,
        order=80,
    )
    entry_430_5 = Entry(  # 'if normaltime'
        "Entry 2",
        start=PTime(4, 30),
        end=None,  # 5:00
        priority=95,
        normaltime=30,
        idealtime=40,
        mintime=50,
        alignend=False,
        order=50,
    )
    entry_430_630 = Entry(  # 'elif start and end' -> normaltime 120
        "Entry3",
        start=PTime(4, 30),
        end=PTime(6, 30),
        priority=0,
        blocks={"block 1", "block 2"},
        categories={"category 1", "category 2"},
        notes=5 * "long placeholder notes here that take space; ",
        alignend=False,
    )
    entry_5_520 = Entry(  # 'elif idealtime'
        "Entry the fourth",
        start=PTime(5),
        end=PTime(5, 20),
        priority=0,
        ismovable=False,
        categories={"category 3"},
        notes=3 * "just some placeholder text, !@#$#@%#^$, "[:-2],
        alignend=True,
    )
    entry_7_1030_a = Entry(  # 'elif mintime'
        "Entry 5",
        start=PTime(7),
        end=PTime(10, 30),
        ismovable=True,
        notes="some basic notes",
        mintime=120,
        alignend=False,
        order=20,
    )
    entry_7_1030_b = Entry(  # 'elif maxtime'
        "Entry 6",
        start=PTime(7),
        end=PTime(10, 30),
        priority=30,
        ismovable=False,
        blocks={"block1", "block2", "block3", "block4"},
        maxtime=360,
        order=45,
    )
    entry_0_030 = Entry("random name", PTime(0))  # 'else'
    # []
    exp_string1 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 00:00-05:00 │ First Entry                                                    ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ priority:     70                                                             ┃\n"
        "┃ blocks:       block 1, block 2, block 3, block 4                             ┃\n"
        "┃ categories:   category 1, category 2, category 3                             ┃\n"
        "┃ notes:        notes on entry 1                                               ┃\n"
        "┃ normaltime:   270                                                            ┃\n"
        "┃ idealtime:    330                                                            ┃\n"
        "┃ mintime:      240                                                            ┃\n"
        "┃ maxtime:      360                                                            ┃\n"
        "┃ alignend:     true                                                           ┃\n"
        "┃ order:        80                                                             ┃\n"
    )
    exp_string2 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 04:30-05:00 │ Entry 2                                                        ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ priority:     95                                                             ┃\n"
        "┃ idealtime:    40                                                             ┃\n"
        "┃ mintime:      50                                                             ┃\n"
        "┃ maxtime:      60                                                             ┃\n"
    )
    exp_string3 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 04:30-06:30 │ Entry 3                                                        ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ priority:     0                                                              ┃\n"
        "┃ blocks:       block 1, block 2                                               ┃\n"
        "┃ categories:   category 1, category 2                                         ┃\n"
        "┃ notes:        long placeholder notes here that take lots of space; long      ┃\n"
        "┃                 placeholder notes here that take space; long placeholder     ┃\n"
        "┃                 notes here that take space; long placeholder notes here      ┃\n"
        "┃                 that take space; long placeholder notes here that take       ┃\n"
        "┃                 space;                                                       ┃\n"
    )
    exp_string4 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 05:00-05:20 │ Entry 4                                                        ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ priority:     0                                                              ┃\n"
        "┃ categories:   category 3                                                     ┃\n"
        "┃ notes:        just some placeholder text, !@#$#@%#^$, just some placeholder  ┃\n"
        "┃                 text, !@#$#@%#^$, just some placeholder text, !@#$#@%#^$     ┃\n"
        "┃ alignend:     true                                                           ┃\n"
    )
    exp_string5 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 07:00-10:30 │ Entry 5                                                        ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ notes:        some basic notes                                               ┃\n"
        "┃ mintime:      120                                                            ┃\n"
        "┃ order:        20                                                             ┃\n"
    )
    exp_string6 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 07:00-10:30 │ Entry 6                                                        ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ priority:     30                                                             ┃\n"
        "┃ ismovable:    false                                                          ┃\n"
        "┃ blocks:       block 1, block 2, block 3, block 4                             ┃\n"
        "┃ maxtime:      360                                                            ┃\n"
        "┃ order:        45                                                             ┃\n"
    )
    exp_string7 = (
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 00:00-00:30 │ random name                                                    ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    )

    # []
    def test_init(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.name == "First Entry"
        assert self.entry_0_5.start == PTime(0)
        assert self.entry_0_5.end == PTime(5)
        assert self.entry_0_5.priority == 70
        assert self.entry_0_5.ismovable == True
        assert self.entry_0_5.blocks == {"block 1", "block 2", "block 3", "block 4"}
        assert self.entry_0_5.categories == {"category 1", "category 2", "category 3"}
        assert self.entry_0_5.notes == "notes on entry 1"
        assert self.entry_0_5.normaltime == 270
        assert self.entry_0_5.idealtime == 330
        assert self.entry_0_5.mintime == 240
        assert self.entry_0_5.maxtime == 360
        assert self.entry_0_5.alignend == True
        assert self.entry_0_5.order == 80

        assert self.entry_430_5.name == "Entry 2"
        assert self.entry_430_5.start == PTime(4, 30)
        assert self.entry_430_5.end == PTime(5)
        assert self.entry_430_5.priority == 95
        assert self.entry_430_5.ismovable == True
        assert self.entry_430_5.blocks == set()
        assert self.entry_430_5.categories == set()
        assert self.entry_430_5.notes == ""
        assert self.entry_430_5.normaltime == 30
        assert self.entry_430_5.idealtime == 35
        assert self.entry_430_5.mintime == 20
        assert self.entry_430_5.maxtime == 40
        assert self.entry_430_5.alignend == False
        assert self.entry_430_5.order == 50

        assert self.entry_430_630.name == "Entry 3"
        assert self.entry_430_630.start == PTime(4, 30)
        assert self.entry_430_630.end == PTime(6, 30)
        assert self.entry_430_630.priority == 0
        assert self.entry_430_630.ismovable == True
        assert self.entry_430_630.blocks == {"block 1", "block 2"}
        assert self.entry_430_630.categories == {"category 1", "category 2"}
        assert (
            self.entry_430_630.notes
            == 5 * "long placeholder notes here that take lots of space; "
        )
        assert self.entry_430_630.normaltime == 120
        assert self.entry_430_630.idealtime == 180
        assert self.entry_430_630.mintime == 60
        assert self.entry_430_630.maxtime == 240
        assert self.entry_430_630.alignend == False
        assert self.entry_430_630.order == 50

        assert self.entry_5_520.name == "Entry the fourth"
        assert self.entry_5_520.start == PTime(5)
        assert self.entry_5_520.end == PTime(5, 20)
        assert self.entry_5_520.priority == 0
        assert self.entry_5_520.ismovable == False
        assert self.entry_5_520.blocks == {"category 3"}
        assert self.entry_5_520.categories == set()
        assert self.entry_5_520.notes == 3 * "just some placeholder text, !@#$#@%#^$, "
        assert self.entry_5_520.normaltime == 20
        assert self.entry_5_520.idealtime == 30
        assert self.entry_5_520.mintime == 10
        assert self.entry_5_520.maxtime == 40
        assert self.entry_5_520.alignend == True
        assert self.entry_5_520.order == 50

        assert self.entry_7_1030_a.name == "Entry 5"
        assert self.entry_7_1030_a.start == PTime(7)
        assert self.entry_7_1030_a.end == PTime(10, 30)
        assert self.entry_7_1030_a.priority == 10
        assert self.entry_7_1030_a.ismovable == True
        assert self.entry_7_1030_a.blocks == set()
        assert self.entry_7_1030_a.categories == set()
        assert self.entry_7_1030_a.notes == "some basic notes"
        assert self.entry_7_1030_a.normaltime == 210
        assert self.entry_7_1030_a.idealtime == 315
        assert self.entry_7_1030_a.mintime == 105
        assert self.entry_7_1030_a.maxtime == 420
        assert self.entry_7_1030_a.alignend == False
        assert self.entry_7_1030_a.order == 20

        assert self.entry_7_1030_b.name == "Entry 6"
        assert self.entry_7_1030_b.start == PTime(7)
        assert self.entry_7_1030_b.end == PTime(10, 30)
        assert self.entry_7_1030_b.priority == 30
        assert self.entry_7_1030_b.ismovable == False
        assert self.entry_7_1030_b.blocks == {"block1", "block2", "block3", "block4"}
        assert self.entry_7_1030_b.categories == set()
        assert self.entry_7_1030_b.notes == ""
        assert self.entry_7_1030_b.normaltime == 210
        assert self.entry_7_1030_b.idealtime == 315
        assert self.entry_7_1030_b.mintime == 105
        assert self.entry_7_1030_b.maxtime == 420
        assert self.entry_7_1030_b.alignend == False
        assert self.entry_7_1030_b.order == 45

        assert self.entry_0_030.name == "random name"
        assert self.entry_0_030.start == PTime()
        assert self.entry_0_030.end == PTime(0, 30)
        assert self.entry_0_030.priority == 10
        assert self.entry_0_030.ismovable == False
        assert self.entry_0_030.blocks == set()
        assert self.entry_0_030.categories == set()
        assert self.entry_0_030.notes == ""
        assert self.entry_0_030.normaltime == 30
        assert self.entry_0_030.idealtime == 45
        assert self.entry_0_030.mintime == 15
        assert self.entry_0_030.maxtime == 60
        assert self.entry_0_030.alignend == False
        assert self.entry_0_030.order == 50

    def test_copy(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        copy1 = self.entry_0_5.copy()
        assert self.entry_0_5 == copy1
        assert self.entry_0_5.__dict__ == copy1.__dict__
        assert id(self.entry_0_5) != id(copy1)

    def test_duration(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.duration == 300
        assert self.entry_430_5.duration == 30
        assert self.entry_430_630.duration == 120
        assert self.entry_5_520.duration == 20
        assert self.entry_7_1030_a.duration == 210
        assert self.entry_7_1030_b.duration == 210
        assert self.entry_0_030.duration == 30

    def test_timespan(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.timespan == (PTime(0), PTime(5))
        assert self.entry_430_5.timespan == (PTime(4, 30), PTime(5))
        assert self.entry_430_630.timespan == (PTime(4, 30), PTime(6, 30))
        assert self.entry_5_520.timespan == (PTime(5), PTime(5, 20))
        assert self.entry_7_1030_a.timespan == (PTime(7), PTime(10, 30))
        assert self.entry_7_1030_b.timespan == (PTime(7), PTime(10, 30))
        assert self.entry_0_030.timespan == (PTime(0), PTime(0, 30))

    def test_as_norg(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        path1 = Path("")
        path2 = Path("")
        path3 = Path("")
        path4 = Path("")
        path5 = Path("")
        path6 = Path("")
        path7 = Path("")

        assert self.entry_0_5.as_norg(path1) == (
            "~ 00:00-05:00 | First Entry\n"
            "  -- priority:   70\n"
            "  -- blocks:     block 1, block 2, block 3, block 4\n"
            "  -- categories: category 1, category 2, category 3\n"
            "  -- notes:      notes on entry 1\n"
            "  -- normaltime: 30\n"
            "  -- idealtime:  35\n"
            "  -- mintime:    20\n"
            "  -- maxtime:    40\n"
            "  -- alignend:   true\n"
            "  -- order:      80"
        )
        assert self.entry_430_5.as_norg(path2) == (
            "~ 04:30-05:00 | Entry 2\n"
            "  -- priority:   95\n"
            "  -- idealtime:  35\n"
            "  -- mintime:    20\n"
            "  -- maxtime:    40"
        )
        assert self.entry_430_630.as_norg(path3) == (
            "~ 04:30-06:30 | Entry 3\n"
            "  -- priority:   0\n"
            "  -- blocks:     block 1, block 2\n"
            "  -- categories: category 1, category 2\n"
            "  -- notes:      TODO\n"
        )
        assert self.entry_5_520.as_norg(path4) == (
            "~ 05:00-05:20 | Entry 4\n\n"
            "  -- priority:   0\n\n"
            "  -- categories: category 3\n\n"
            "  -- notes:      just some placeholder text, !@#$#@%#^$, just some"
            "                   placeholder text, !@#$#@%#^$, just some"
            "                   placeholder text, !@#$#@%#^$"
            "  -- alignend:   true"
        )
        assert self.entry_7_1030_a.as_norg(path5) == (
            "~ 07:00-10:30 | Entry 5\n"
            "  -- notes:      some basic notes\n"
            "  -- mintime:    120"
            "  -- order:      20"
        )
        assert self.entry_7_1030_b.as_norg(path6) == (
            "~ 07:00-10:30 | Entry 6\n"
            "  -- priority:   30\n"
            "  -- ismovable:  false\n"
            "  -- blocks:     block 1, block 2, block 3, block 4\n"
            "  -- maxtime:    360\n"
            "  -- order:      45"
        )
        assert self.entry_0_030.as_norg(path7) == "~ 00:00-00:30 | random name"

    # []
    def test_as_json(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert True

    # []
    def test_as_html(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert True

    def test_hasmass(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.hasmass()
        assert self.entry_430_5.hasmass()
        assert not self.entry_430_630.hasmass()
        assert not self.entry_5_520.hasmass()
        assert self.entry_7_1030_a.hasmass()
        assert self.entry_7_1030_b.hasmass()
        assert self.entry_0_030.hasmass()

    def test_isbefore(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.isbefore(self.entry_5_520)
        assert self.entry_430_5.isbefore(self.entry_5_520)
        assert self.entry_430_630.isbefore(self.entry_7_1030_a)
        assert self.entry_5_520.isbefore(self.entry_7_1030_a)
        assert not self.entry_7_1030_a.isbefore(self.entry_0_030)
        assert not self.entry_7_1030_b.isbefore(self.entry_0_5)
        assert not self.entry_0_030.isbefore(self.entry_430_5)

    def test_isafter(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert not self.entry_0_5.isafter(self.entry_0_030)
        assert not self.entry_430_5.isafter(self.entry_0_5)
        assert self.entry_430_630.isafter(self.entry_430_5)
        assert self.entry_7_1030_b.isafter(self.entry_430_630)
        assert not self.entry_7_1030_b.isafter(self.entry_7_1030_a)
        assert not self.entry_0_030.isafter(self.entry_7_1030_b)

    def test_isbefore_by_start(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.isbefore_by_start(self.entry_430_5)
        assert not self.entry_430_5.isbefore_by_start(self.entry_430_630)
        assert self.entry_430_630.isbefore_by_start(self.entry_5_520)
        assert self.entry_5_520.isbefore_by_start(self.entry_430_5)
        assert not self.entry_7_1030_a.isbefore_by_start(self.entry_7_1030_b)
        assert not self.entry_7_1030_b.isbefore_by_start(self.entry_0_030)
        assert not self.entry_0_030.isbefore_by_start(self.entry_0_5)

    def test_isafter_by_start(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert not self.entry_0_5.isafter_by_start(self.entry_0_030)
        assert self.entry_430_5.isafter_by_start(self.entry_0_5)
        assert not self.entry_430_630.isafter_by_start(self.entry_430_5)
        assert self.entry_5_520.isafter_by_start(self.entry_430_630)
        assert self.entry_7_1030_a.isafter_by_start(self.entry_5_520)
        assert not self.entry_7_1030_b.isafter_by_start(self.entry_7_1030_a)
        assert not self.entry_0_030.isafter_by_start(self.entry_7_1030_b)

    def test_overlaps(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.overlaps(self.entry_430_5)
        assert self.entry_0_5.overlaps(self.entry_430_630)
        assert self.entry_0_5.overlaps(self.entry_0_030)
        assert self.entry_7_1030_a.overlaps(self.entry_7_1030_b)
        assert self.entry_430_5.overlaps(self.entry_0_5)
        assert self.entry_430_630.overlaps(self.entry_0_5)
        assert self.entry_5_520.overlaps(self.entry_0_5)
        assert self.entry_7_1030_a.overlaps(self.entry_7_1030_a)

    def test_overlaps_first(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_030.overlaps_first(self.entry_0_5)
        assert self.entry_0_5.overlaps_first(self.entry_430_5)
        assert self.entry_0_5.overlaps_first(self.entry_430_630)
        assert self.entry_430_5.overlaps_first(self.entry_430_630)
        assert not self.entry_7_1030_a.overlaps_first(self.entry_7_1030_b)
        assert not self.entry_7_1030_b.overlaps_first(self.entry_7_1030_a)

    def test_overlaps_second(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.overlaps_second(self.entry_0_030)
        assert self.entry_430_5.overlaps_second(self.entry_0_5)
        assert self.entry_430_630.overlaps_second(self.entry_0_5)
        assert self.entry_430_630.overlaps_second(self.entry_430_5)
        assert not self.entry_7_1030_a.overlaps_second(self.entry_7_1030_b)
        assert not self.entry_7_1030_b.overlaps_second(self.entry_7_1030_a)

    def test_surrounds(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_430_630.surrounds(self.entry_430_5)
        assert self.entry_430_630.surrounds(self.entry_5_520)
        assert self.entry_0_5.surrounds(self.entry_430_5)
        assert self.entry_0_5.surrounds(self.entry_0_030)

        assert not self.entry_430_5.surrounds(self.entry_430_630)
        assert not self.entry_430_5.surrounds(self.entry_0_5)
        assert not self.entry_7_1030_a.surrounds(self.entry_5_520)
        assert not self.entry_0_030.surrounds(self.entry_0_5)

    def test_surrounded_by(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_430_630.surrounded_by(self.entry_430_5)
        assert self.entry_430_5.surrounded_by(self.entry_0_5)
        assert self.entry_0_030.surrounded_by(self.entry_0_5)
        assert self.entry_430_5.surrounded_by(self.entry_430_630)
        assert self.entry_5_520.surrounded_by(self.entry_430_630)

        assert self.entry_430_5.surrounded_by(self.entry_430_630)
        assert self.entry_0_5.surrounded_by(self.entry_430_5)
        assert self.entry_0_5.surrounded_by(self.entry_0_030)
        assert self.entry_430_630.surrounded_by(self.entry_430_5)
        assert self.entry_430_630.surrounded_by(self.entry_5_520)
        assert self.entry_430_5.surrounded_by(self.entry_7_1030_b)
        assert self.entry_7_1030_b.surrounded_by(self.entry_430_5)

    def test_shares_start_shorter(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_030.shares_start_shorter(self.entry_0_5)
        assert self.entry_430_5.shares_start_shorter(self.entry_430_630)
        assert not self.entry_430_630.shares_start_shorter(self.entry_5_520)
        assert not self.entry_5_520.shares_start_shorter(self.entry_7_1030_a)
        assert not self.entry_7_1030_a.shares_start_shorter(self.entry_7_1030_b)
        assert not self.entry_0_5.shares_start_shorter(self.entry_0_030)

    def test_shares_start_longer(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_430_630.shares_start_longer(self.entry_430_5)
        assert not self.entry_430_5.shares_start_longer(self.entry_430_630)
        assert not self.entry_7_1030_a.shares_end_shorter(self.entry_7_1030_b)

    def test_shares_end_shorter(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_430_5.shares_end_shorter(self.entry_0_5)
        assert not self.entry_0_5.shares_end_shorter(self.entry_430_5)
        assert not self.entry_7_1030_a.shares_end_shorter(self.entry_7_1030_b)

    def test_shares_end_longer(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.shares_end_longer(self.entry_430_5)
        assert not self.entry_430_5.shares_end_longer(self.entry_430_630)
        assert not self.entry_7_1030_a.shares_end_longer(self.entry_7_1030_b)

    def test_covers(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.covers(self.entry_0_030)
        assert self.entry_0_5.covers(self.entry_430_5)
        assert self.entry_7_1030_b.covers(self.entry_430_5)
        assert self.entry_430_630.covers(self.entry_7_1030_a)
        assert self.entry_7_1030_a.covers(self.entry_7_1030_b)
        assert self.entry_430_630.covers(self.entry_5_520)

        assert self.entry_5_520.covers(self.entry_7_1030_b)
        assert self.entry_7_1030_b.covers(self.entry_5_520)
        assert self.entry_0_030.covers(self.entry_0_5)
        assert self.entry_430_5.covers(self.entry_0_5)
        assert self.entry_430_5.covers(self.entry_430_630)

    def test_iscovered(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_030.iscovered(self.entry_0_5)
        assert self.entry_430_5.iscovered(self.entry_0_5)
        assert self.entry_430_5.iscovered(self.entry_430_630)
        assert self.entry_7_1030_a.iscovered(self.entry_7_1030_b)
        assert self.entry_7_1030_b.iscovered(self.entry_7_1030_a)
        assert self.entry_5_520.iscovered(self.entry_430_630)

        assert not self.entry_7_1030_b.iscovered(self.entry_5_520)
        assert not self.entry_5_520.iscovered(self.entry_7_1030_b)
        assert not self.entry_0_5.iscovered(self.entry_0_030)
        assert not self.entry_0_5.iscovered(self.entry_430_5)
        assert not self.entry_430_630.iscovered(self.entry_430_5)

    def test_trumps(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert not self.entry_0_5.trumps(self.entry_430_5)
        assert not self.entry_430_5.trumps(self.entry_0_5)

        assert not self.entry_7_1030_b.trumps(self.entry_5_520)
        assert not self.entry_5_520.trumps(self.entry_7_1030_b)

        assert not self.entry_430_630.trumps(self.entry_5_520)

    def test_fits_in(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert not self.entry_0_5.fits_in(self.entry_430_5)
        assert self.entry_430_5.fits_in(self.entry_0_5)

        assert not self.entry_5_520.fits_in(self.entry_7_1030_a)
        assert self.entry_7_1030_a.fits_in(self.entry_5_520)

    def test_accommodates(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert not self.entry_430_5.accommodates(self.entry_0_5)
        assert self.entry_0_5.accommodates(self.entry_430_5)

        assert not self.entry_7_1030_a.accommodates(self.entry_5_520)
        assert self.entry_5_520.accommodates(self.entry_7_1030_a)

    def test_pretty(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.entry_0_5.pretty() == self.exp_string1
        assert self.entry_430_5.pretty() == self.exp_string2
        assert self.entry_430_630.pretty() == self.exp_string3
        assert self.entry_5_520.pretty() == self.exp_string4
        assert self.entry_7_1030_a.pretty() == self.exp_string5
        assert self.entry_7_1030_b.pretty() == self.exp_string6
        assert self.entry_0_030.pretty() == self.exp_string7

    def test_eq(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        dup1 = Entry(
            "First Entry",
            start=PTime(0),
            end=PTime(5),
            priority=70,
            ismovable=True,
            blocks={"block 1", "block 2", "block 3", "block 4"},
            categories={"category 1", "category 2", "category 3"},
            notes="notes on entry 1",
            normaltime=270,
            idealtime=330,
            mintime=240,
            maxtime=360,
            alignend=True,
            order=80,
        )
        dup2 = Entry(
            "Entry 2",
            start=PTime(4, 30),
            end=None,  # 5:00
            priority=95,
            normaltime=30,
            idealtime=40,
            mintime=50,
            alignend=False,
            order=50,
        )
        dup3 = Entry(
            "Entry3",
            start=PTime(4, 30),
            end=PTime(6, 30),
            priority=0,
            blocks={"block 1", "block 2"},
            categories={"category 1", "category 2"},
            notes=5 * "long placeholder notes here that take space; ",
            alignend=False,
        )

        assert self.entry_0_5 == self.entry_0_5
        assert self.entry_430_5 == self.entry_430_5
        assert self.entry_430_630 == self.entry_430_630
        assert self.entry_5_520 == self.entry_5_520.copy()
        assert self.entry_7_1030_a == self.entry_7_1030_a.copy()
        assert self.entry_7_1030_b == self.entry_7_1030_b.copy()
        assert self.entry_0_030 == Entry("random name")

        assert self.entry_0_5 == dup1
        assert self.entry_430_5 == dup2
        assert self.entry_430_630 == dup3

        assert self.entry_7_1030_a != self.entry_0_5
        assert self.entry_7_1030_b != self.entry_430_5
        assert self.entry_0_030 != self.entry_430_630

    def test_str(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert str(self.entry_0_5) == self.exp_string1
        assert str(self.entry_430_5) == self.exp_string2
        assert str(self.entry_430_630) == self.exp_string3
        assert str(self.entry_5_520) == self.exp_string4
        assert str(self.entry_7_1030_a) == self.exp_string5
        assert str(self.entry_7_1030_b) == self.exp_string6
        assert str(self.entry_0_030) == self.exp_string7

    def test_repr(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert repr(self.entry_0_5) == self.exp_string1
        assert repr(self.entry_430_5) == self.exp_string2
        assert repr(self.entry_430_630) == self.exp_string3
        assert repr(self.entry_5_520) == self.exp_string4
        assert repr(self.entry_7_1030_a) == self.exp_string5
        assert repr(self.entry_7_1030_b) == self.exp_string6
        assert repr(self.entry_0_030) == self.exp_string7


class EmptyTest:
    empty = Empty(start=PTime(5), end=PTime(7, 30))

    def test_init(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.empty.start == PTime(5)
        assert self.empty.end == PTime(7, 30)
        assert self.empty.ismovable == False
        assert self.empty.priority == -1.0
        assert self.empty.mintime == 0


def test_FIRST_ENTRY() -> None:
    """
    Cases:
    1) 
    2) 
    3) 
    """
    assert FIRST_ENTRY.start == PTime(0, 0)
    assert FIRST_ENTRY.end == PTime(0, 0)
    assert FIRST_ENTRY.priority < 0
    assert not FIRST_ENTRY.ismovable
    assert not FIRST_ENTRY.hasmass()


def test_LAST_ENTRY() -> None:
    """
    Cases:
    1) 
    2) 
    3) 
    """
    assert LAST_ENTRY.start == PTime(24, 0)
    assert LAST_ENTRY.end == PTime(24, 0)
    assert LAST_ENTRY.priority < 0
    assert not LAST_ENTRY.ismovable
    assert not LAST_ENTRY.hasmass()
