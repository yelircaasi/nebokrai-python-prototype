from calendar import Calendar
from pathlib import Path

import pytest

from planager.entity import Schedule
from planager.entity.base.adhoc import AdHoc
from planager.entity.base.entry import Entry
from planager.entity.base.plan import Plan
from planager.entity.container.entries import Entries
from planager.entity.container.routines import Routines
from planager.entity.container.tasks import Tasks
from planager.util.pdatetime.pdate import PDate
from planager.util.pdatetime.ptime import PTime


class ScheduleTest:
    # # [ ]
    # sched1 = Schedule(
    #     PDate(0, 0, 0),
    #     Entries(
    #         (
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #         )
    #     ),
    # )
    # # [ ]
    # sched2 = Schedule(
    #     PDate(0, 0, 0),
    #     Entries(
    #         (
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #             Entry(name="", start=PTime(0, 0)),
    #         )
    #     ),
    # )
    # # [ ]
    # sched3 = Schedule(PDate(0, 0, 0))
    # # [ ]
    # exp_string1 = (
    #     "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    #     "┃ Thursday, August 3rd, 2023                                                   ┃\n"
    #     "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    #     "┃ 05:00-05:20 │ Entry 4                                                        ┃\n"
    #     "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    #     "┃ priority:     0                                                              ┃\n"
    #     "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    # )
    # # [ ]
    # exp_string2 = "\n" "\n" "\n" "\n"
    # # [ ]
    # exp_string3 = "\n" "\n" "\n" "\n"
    # # [ ]
    # norg_string1 = "\n" "\n" "\n" "\n"
    # # [ ]
    # norg_string2 = "\n" "\n" "\n" "\n"
    # # [ ]
    # norg_string3 = "\n" "\n" "\n" "\n"
    # # [ ]
    # json_string1 = "\n" "\n" "\n" "\n"
    # # [ ]
    # json_string2 = "\n" "\n" "\n" "\n"
    # # [ ]
    # json_string3 = "\n" "\n" "\n" "\n"
    # # [ ]
    # html_string1 = "\n" "\n" "\n" "\n"
    # # [ ]
    # html_string2 = "\n" "\n" "\n" "\n"
    # # [ ]
    # html_string3 = "\n" "\n" "\n" "\n"

    # # [ ]
    # def test_init(self) -> None:
    #     """
    #     Cases:
    #     1)
    #     2)
    #     3)
    #     """
    #     assert self.sched1.date == PDate(0, 0, 0)
    #     assert self.sched2.date == PDate(0, 0, 0)
    #     assert self.sched3.date is None

    # # [ ]
    # def test_copy(self) -> None:
    #     """
    #     Cases:
    #     1)
    #     2)
    #     3)
    #     """
    #     assert self.sched1.copy().__dict__ == self.sched1.__dict__
    #     assert self.sched2.copy().__dict__ == self.sched2.__dict__
    #     assert self.sched3.copy().__dict__ == self.sched3.__dict__

    def test_from_calendar(self) -> None:
        calendar = Calendar()
        date = PDate()
        schedule = Schedule.from_calendar(calendar, date)
        exp = Schedule()

        assert schedule == exp

    # [ ]
    def test_make_default_day(self) -> None:
        exp = Entries()
        dd = Schedule.make_default_day()
        assert dd == Schedule()

    # [ ]
    def test_from_norg(self) -> None:
        """
        Cases:
        1) minimal
        2) maximal
        3) intermediate
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        exp1 = Schedule()
        exp2 = Schedule()
        exp3 = Schedule()

        assert exp1 == Schedule.from_norg(path1)
        assert exp2 == Schedule.from_norg(path2)
        assert exp3 == Schedule.from_norg(path3)

    # [ ]
    def test_from_json(self) -> None:
        """
        Cases:
        1) minimal
        2) maximal
        3) intermediate
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        exp1 = Schedule()
        exp2 = Schedule()
        exp3 = Schedule()

        assert exp1 == Schedule.from_json(path1)
        assert exp2 == Schedule.from_json(path2)
        assert exp3 == Schedule.from_json(path3)

    # [ ]
    def test_from_html(self) -> None:
        """
        Cases:
        1) minimal
        2) maximal
        3) intermediate
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        exp1 = Schedule()
        exp2 = Schedule()
        exp3 = Schedule()

        assert exp1 == Schedule.from_html(path1)
        assert exp2 == Schedule.from_html(path2)
        assert exp3 == Schedule.from_html(path3)

    # [ ]
    def test_to_norg(self) -> None:
        """
        Cases:
        1) minimal
        2) maximal
        3) intermediate
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()

        norg_string1 = ()
        norg_string2 = ()
        norg_string3 = ()

        sched1.to_norg(path1)
        with open(path1, "r") as f:
            string1 = f.read()
        assert string1 == norg_string1

        sched2.to_norg(path2)
        with open(path2, "r") as f:
            string2 = f.read()
        assert string2 == norg_string2

        sched3.to_norg(path3)
        with open(path3, "r") as f:
            string3 = f.read()
        assert string3 == norg_string3

    # [ ]
    def test_to_json(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()

        json_string1 = ()
        json_string2 = ()
        json_string3 = ()

        sched1.to_json(path1)
        with open(path1, "r") as f:
            string1 = f.read()
        assert string1 == json_string1

        sched2.to_json(path2)
        with open(path2, "r") as f:
            string2 = f.read()
        assert string2 == json_string2

        sched3.to_json(path3)
        with open(path3, "r") as f:
            string3 = f.read()
        assert string3 == json_string3

    # [ ]
    def test_as_html(self) -> None:
        """
        Cases:
        1)
        2)
        3)
        """
        path1 = Path()
        path2 = Path()
        path3 = Path()

        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()

        html_string1 = ()
        html_string2 = ()
        html_string3 = ()

        sched1.to_html(path1)
        with open(path1, "r") as f:
            string1 = f.read()
        assert string1 == html_string1

        sched2.to_html(path2)
        with open(path2, "r") as f:
            string2 = f.read()
        assert string2 == html_string2

        sched3.to_html(path3)
        with open(path3, "r") as f:
            string3 = f.read()
        assert string3 == html_string3

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

        norg_string1 = ()
        norg_string2 = ()
        norg_string3 = ()

        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()

        sched1.to_norg(path1)
        sched2.to_norg(path2)
        sched3.to_norg(path3)

        with open(path1) as f:
            assert norg_string1 == f.read()
        with open(path2) as f:
            assert norg_string2 == f.read()
        with open(path3) as f:
            assert norg_string3 == f.read()

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

        json_string1 = ()
        json_string2 = ()
        json_string3 = ()

        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()

        sched1.to_json(path1)
        sched2.to_json(path2)
        sched3.to_json(path3)

        with open(path1) as f:
            assert json_string1 == f.read()
        with open(path2) as f:
            assert json_string2 == f.read()
        with open(path3) as f:
            assert json_string3 == f.read()

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

        html_string1 = ()
        html_string2 = ()
        html_string3 = ()

        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()

        sched1.to_html(path1)
        sched2.to_html(path2)
        sched3.to_html(path3)

        with open(path1) as f:
            assert html_string1 == f.read()
        with open(path2) as f:
            assert html_string2 == f.read()
        with open(path3) as f:
            assert html_string3 == f.read()

    # [ ]
    def test_add(self) -> None:
        """
        Cases:
        1)  add flex over empty day
        2)  add flex over empty space
        3)  add flex over empty with snap
        4)  add flex with compression
        5)  add flex over flex
        6)  add flex over fixed
        7)  add fixed over empty day
        8)  add fixed over empty space
        9)  add fixed over empty with snap
        10) add fixed with compression
        11) add fixed over flex
        12) add fixed over fixed
        """
        sched1 = Schedule()
        sched2 = Schedule()
        sched3 = Schedule()
        sched4 = Schedule()
        sched5 = Schedule()
        sched6 = Schedule()
        sched7 = Schedule()
        sched8 = Schedule()
        sched9 = Schedule()
        sched10 = Schedule()
        sched11 = Schedule()
        sched12 = Schedule()

        exp1 = Schedule()
        exp2 = Schedule()
        exp3 = Schedule()
        exp4 = Schedule()
        exp5 = Schedule()
        exp6 = Schedule()
        exp7 = Schedule()
        exp8 = Schedule()
        exp9 = Schedule()
        exp10 = Schedule()
        exp11 = Schedule()
        exp12 = Schedule()

        sched1.add(Entry())
        sched2.add(Entry())
        sched3.add(Entry())
        sched4.add(Entry())
        sched5.add(Entry())
        sched6.add(Entry())
        sched7.add(Entry())
        sched8.add(Entry())
        sched9.add(Entry())
        sched10.add(Entry())
        sched11.add(Entry())
        sched12.add(Entry())

        assert sched1 == exp1
        assert sched2 == exp2
        assert sched3 == exp3
        assert sched4 == exp4
        assert sched5 == exp5
        assert sched6 == exp6
        assert sched7 == exp7
        assert sched8 == exp8
        assert sched9 == exp9
        assert sched10 == exp10
        assert sched11 == exp11
        assert sched12 == exp12

    # [ ]
    def test_remove(self) -> None:
        """
        Cases:
        1) remove from otherwise empty
        2) remove without triggering expansion
        3) remove triggering expansion
        4) remove triggering snap
        """
        sched_empty = Schedule()
        sched_noexpand = Schedule()
        sched_expand = Schedule()
        sched_snap = Schedule()

        exp_empty = Schedule()
        exp_noexpand = Schedule()
        exp_expand = Schedule()
        exp_snap = Schedule()

        sched_empty.remove(Entry())
        sched_noexpand.remove(Entry())
        sched_expand.remove(Entry())
        sched_snap.remove(Entry())

        assert sched_empty == exp_empty
        assert sched_noexpand == exp_noexpand
        assert sched_expand == exp_expand
        assert sched_snap == exp_snap

    # [ ]
    def test_names(self) -> None:
        sched = Schedule()
        assert sched.names == ["", "", ""]

    # [ ]
    def test_starts(self) -> None:
        sched = Schedule()
        assert sched.starts == [PTime(), PTime(), PTime()]

    # [ ]
    def test_starts_strings(self) -> None:
        sched = Schedule()
        assert sched.starts_strings == ["", "", ""]

    # [ ]
    def test_add_routines(self) -> None:
        sched = Schedule()
        routines = Routines()
        exp = Schedule()

        sched.add_routines(routines)

        assert sched == exp

    # [ ]
    def test_add_from_plan(self) -> None:
        sched = Schedule()
        plan = Plan()
        tasks = Tasks()
        exp = Schedule()

        sched.add_from_plan(plan, tasks)

        assert sched == exp

    # [ ]
    def test_add_adhoc(self) -> None:
        sched = Schedule()
        adhoc = AdHoc()
        exp = Schedule()

        sched.add_adhoc(adhoc)

        assert sched == exp

    # [ ]
    def test_can_be_added(self) -> None:
        """
        Cases:
        1) addable
        2) nonaddable due to space
        3) nonaddable due to conflict of fixed
        4) addable on schedule dense with fixed entries
        5) non-addable on schedule dense with fixed entries
        """
        sched = Schedule()
        sched_fixed_tight = Schedule()

        addable = Entry()
        nonaddable_by_space = Entry()
        nonaddable_fixed = Entry()
        addable_for_fixed_tight = Entry()
        nonaddable_for_fixed_tight = Entry()

        assert sched.can_be_added(addable)
        assert not sched.can_be_added(nonaddable_by_space)
        assert not sched.can_be_added(nonaddable_fixed)
        assert sched_fixed_tight.can_be_added(addable_for_fixed_tight)
        assert not sched_fixed_tight.can_be_added(nonaddable_for_fixed_tight)

    # [ ]
    def test_prio_weighting_function(self) -> None:
        """
        Cases:
        1) default values
        2) custom values
        """
        sched_default = Schedule()
        sched_custom = Schedule(
            ...,
            weight_interval_min=0.5,
            weight_interval_max=1.5,
            prio_transform=lambda x: (x / 100) ** 2,
        )

        weighter_default = sched_default.prio_weighting_function
        weighter_custom = sched_custom.prio_weighting_function

        assert weighter_default(0) == ...
        assert weighter_default(10) == ...
        assert weighter_default(20) == ...
        assert weighter_default(33) == ...
        assert weighter_default(42) == ...
        assert weighter_default(55) == ...
        assert weighter_default(60) == ...
        assert weighter_default(69) == ...
        assert weighter_default(80) == ...
        assert weighter_default(95) == ...
        assert weighter_default(100) == ...

        assert weighter_custom(0) == ...
        assert weighter_custom(10) == ...
        assert weighter_custom(20) == ...
        assert weighter_custom(33) == ...
        assert weighter_custom(42) == ...
        assert weighter_custom(55) == ...
        assert weighter_custom(60) == ...
        assert weighter_custom(69) == ...
        assert weighter_custom(80) == ...
        assert weighter_custom(95) == ...
        assert weighter_custom(100) == ...

    # [ ]
    def test_is_valid(
        self,
    ) -> None:  # rewrite to make initializing an invalid schedule impossible
        """
        Cases:
        1) valid
        2) invalid due to gaps
        3) invalid due to overlaps
        4) invalid due to both
        """
        valid = Schedule()
        gaps = Schedule()
        overlaps = Schedule()
        both = Schedule()

        assert valid.is_valid()
        assert not gaps.is_valid()
        assert not overlaps.is_valid()
        assert not both.is_valid()

    def test_str(self) -> None:
        sched = Schedule()
        exp = "" "" ""
        assert str(sched) == exp

    def test_repr(self) -> None:
        sched = Schedule()
        exp = "" "" ""
        assert repr(sched) == exp
