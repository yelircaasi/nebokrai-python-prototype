from pathlib import Path

import pytest

from planager.entity import Schedule
from planager.entity.base.entry import Entry
from planager.entity.container.entries import Entries
from planager.util.pdatetime.pdate import PDate
from planager.util.pdatetime.ptime import PTime


class ScheduleTest:
    # [ ]
    sched1 = Schedule(
        PDate(0, 0, 0),
        Entries((
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
        ))
    )
    # [ ]
    sched2 = Schedule(
        PDate(0, 0, 0),
        Entries((
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
            Entry(name="", start=PTime(0, 0)),
        ))
    )
    # [ ]
    sched3 = Schedule(PDate(0, 0, 0))
    # [ ]
    exp_string1 = (
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃ Thursday, August 3rd, 2023                                                   ┃\n"
        "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
        "┃ 05:00-05:20 │ Entry 4                                                        ┃\n"
        "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
        "┃ priority:     0                                                              ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    )
    # [ ]
    exp_string2 = "\n" "\n" "\n" "\n"
    # [ ]
    exp_string3 = "\n" "\n" "\n" "\n"
    # [ ]
    norg_string1 = "\n" "\n" "\n" "\n"
    # [ ]
    norg_string2 = "\n" "\n" "\n" "\n"
    # [ ]
    norg_string3 = "\n" "\n" "\n" "\n"
    # [ ]
    json_string1 = "\n" "\n" "\n" "\n"
    # [ ]
    json_string2 = "\n" "\n" "\n" "\n"
    # [ ]
    json_string3 = "\n" "\n" "\n" "\n"
    # [ ]
    html_string1 = "\n" "\n" "\n" "\n"
    # [ ]
    html_string2 = "\n" "\n" "\n" "\n"
    # [ ]
    html_string3 = "\n" "\n" "\n" "\n"

    # [ ]
    def test_init(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1.date == PDate(0, 0, 0)
        assert self.sched2.date == PDate(0, 0, 0)
        assert self.sched3.date is None

    # [ ]
    def test_copy(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1.copy().__dict__ == self.sched1.__dict__
        assert self.sched2.copy().__dict__ == self.sched2.__dict__
        assert self.sched3.copy().__dict__ == self.sched3.__dict__

    # [ ]
    def test_make_default_day(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        dd = Schedule.make_default_day()
        assert dd == Schedule()

    # [ ]
    def test_from_norg(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()
        # [ ]
        assert self.sched1 == Schedule.from_norg(path1)
        assert self.sched2 == Schedule.from_norg(path2)
        assert self.sched3 == Schedule.from_norg(path3)

    # [ ]
    def test_from_json(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()
        # [ ]
        assert self.sched1 == Schedule.from_json(path1)
        assert self.sched2 == Schedule.from_json(path2)
        assert self.sched3 == Schedule.from_json(path3)

    # [ ]
    def test_from_html(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()
        # [ ]
        assert self.sched1 == Schedule.from_html(path1)
        assert self.sched2 == Schedule.from_html(path2)
        assert self.sched3 == Schedule.from_html(path3)

    # [ ]
    def test_to_norg(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        p = Path()

        self.sched1.to_norg(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.norg_string1

        self.sched2.to_norg(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.norg_string2

        self.sched3.to_norg(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.norg_string3

    # [ ]
    def test_to_json(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        p = Path()

        self.sched1.to_json(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.json_string1

        self.sched2.to_json(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.json_string2

        self.sched3.to_json(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.json_string3

    # [ ]
    def test_as_html(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        p = Path()

        self.sched1.to_html(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.html_string1

        self.sched2.to_html(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.html_string2

        self.sched3.to_html(p)
        with open(p, "r") as f:
            s = f.read()
        assert s == self.html_string3

    # [ ]
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

        self.sched1.to_norg(path1)
        self.sched2.to_norg(path2)
        self.sched3.to_norg(path3)
        
        with open(path1) as f:
            assert self.norg_string1 == f.read()
        with open(path2) as f:
            assert self.norg_string2 == f.read()
        with open(path3) as f:
            assert self.norg_string3 == f.read()
    # [ ]
    def test_as_json(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        path1 = Path("")
        path2 = Path("")
        path3 = Path("")

        self.sched1.to_json(path1)
        self.sched2.to_json(path2)
        self.sched3.to_json(path3)
        
        with open(path1) as f:
            assert self.norg_string1 == f.read()
        with open(path2) as f:
            assert self.norg_string2 == f.read()
        with open(path3) as f:
            assert self.norg_string3 == f.read()
    # [ ]
    def test_to_html(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        path1 = Path("")
        path2 = Path("")
        path3 = Path("")

        self.sched1.to_html(path1)
        self.sched2.to_html(path2)
        self.sched3.to_html(path3)
        
        with open(path1) as f:
            assert self.norg_string1 == f.read()
        with open(path2) as f:
            assert self.norg_string2 == f.read()
        with open(path3) as f:
            assert self.norg_string3 == f.read()

    # [ ]
    def test_add(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        sched4 = self.sched1.copy()
        sched5 = self.sched2.copy()
        sched6 = self.sched3.copy()

        sched4.add()
        sched5.add()
        sched6.add()

        assert ... in sched4
        assert ... in sched5
        assert ... in sched6

    # [ ]
    def test_remove(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        sched4 = self.sched1.copy()
        sched5 = self.sched2.copy()
        sched6 = self.sched3.copy()

        sched4.remove()
        sched5.remove()
        sched6.remove()

        assert ... in sched4
        assert ... in sched5
        assert ... in sched6

    # [ ]
    def test_names(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1 == [PTime(), PTime(), PTime()]
        assert self.sched2 == [PTime(), PTime(), PTime()]
        assert self.sched3 == [PTime(), PTime(), PTime()]

    # [ ]
    def test_starts(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1
        assert self.sched2
        assert self.sched3

    # [ ]
    def test_starts_strings(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1
        assert self.sched2
        assert self.sched3

    # [ ]
    def test_add_routines(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1
        assert self.sched2
        assert self.sched3

    # [ ]
    def test_add_from_plan(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1
        assert self.sched2
        assert self.sched3

    # [ ]
    def test_add_adhoc(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1
        assert self.sched2
        assert self.sched3

    # [ ]
    def test_can_be_added(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert self.sched1.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert self.sched1.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert self.sched1.can_be_added(Entry(name="", start=PTime(0, 0)))

        assert self.sched2.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert self.sched2.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert self.sched2.can_be_added(Entry(name="", start=PTime(0, 0)))

        assert self.sched3.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert self.sched3.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert self.sched3.can_be_added(Entry(name="", start=PTime(0, 0)))

        assert not self.sched1.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert not self.sched1.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert not self.sched1.can_be_added(Entry(name="", start=PTime(0, 0)))

        assert not self.sched2.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert not self.sched2.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert not self.sched2.can_be_added(Entry(name="", start=PTime(0, 0)))

        assert not self.sched3.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert not self.sched3.can_be_added(Entry(name="", start=PTime(0, 0)))
        assert not self.sched3.can_be_added(Entry(name="", start=PTime(0, 0)))

    # [ ]
    def test_allocate_in_time(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert True

    # [ ]
    def test_prio_weighting_function(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        weighter1 = self.sched1.prio_weighting_function
        assert self.sched1.prio_weighting_function(0) == weighter1(0) == ...
        assert self.sched1.prio_weighting_function(10) == weighter1(10) == ...
        assert self.sched1.prio_weighting_function(30) == weighter1(30) == ...
        assert self.sched1.prio_weighting_function(70) == weighter1(70) == ...
        assert self.sched1.prio_weighting_function(100) == weighter1(100) == ...

        weighter2 = self.sched2.prio_weighting_function
        assert self.sched2.prio_weighting_function(10) == weighter2(10) == ...
        assert self.sched2.prio_weighting_function(30) == weighter2(30) == ...
        assert self.sched2.prio_weighting_function(50) == weighter2(50) == ...
        assert self.sched2.prio_weighting_function(77) == weighter2(77) == ...
        assert self.sched2.prio_weighting_function(100) == weighter2(100) == ...

        weighter3 = self.sched1.prio_weighting_function
        assert self.sched3.prio_weighting_function(5) == weighter3(5) == ...
        assert self.sched3.prio_weighting_function(10) == weighter3(10) == ...
        assert self.sched3.prio_weighting_function(30) == weighter3(30) == ...
        assert self.sched3.prio_weighting_function(70) == weighter3(70) == ...
        assert self.sched3.prio_weighting_function(90) == weighter3(90) == ...

    # [ ]
    def test_is_valid(
        self,
    ) -> None:  # rewrite to make initializing an invalid schedule impossible
        """
        Cases:
        1) 
        2) 
        3) 
        """
        invalid1 = Schedule()
        invalid2 = Schedule()

        assert self.sched1.is_valid()
        assert self.sched2.is_valid()
        assert self.sched3.is_valid()

        assert not invalid1.is_valid()
        assert not invalid2.is_valid()

    def test_str(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert str(self.sched1) == self.exp_string1
        assert str(self.sched2) == self.exp_string2
        assert str(self.sched3) == self.exp_string3

    def test_repr(self) -> None:
        """
        Cases:
        1) 
        2) 
        3) 
        """
        assert repr(self.sched1) == self.exp_string1
        assert repr(self.sched2) == self.exp_string2
        assert repr(self.sched3) == self.exp_string3
