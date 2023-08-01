from pathlib import Path

import pytest

from planager.entity import Schedule


class ScheduleTest:
    sched1 = Schedule()
    sched2 = Schedule()
    sched3 = Schedule()

    exp_string1 = '\n'.join(
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

    norg_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    norg_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    norg_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    
    json_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    json_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    json_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    
    html_string1 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    html_string2 = '\n'.join(
        "",
        "",
        "",
        "",
    )
    html_string3 = '\n'.join(
        "",
        "",
        "",
        "",
    )

    def test_init(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_copy(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_make_default_day(self) -> None:
        dd = Schedule.make_default_day()
        assert dd == Schedule()

    def test_from_norg(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        assert self.sched1 == Schedule.from_norg(path1)
        assert self.sched2 == Schedule.from_norg(path2)
        assert self.sched3 == Schedule.from_norg(path3)

    def test_from_json(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        assert self.sched1 == Schedule.from_json(path1)
        assert self.sched2 == Schedule.from_json(path2)
        assert self.sched3 == Schedule.from_json(path3)

    def test_from_html(self) -> None:
        path1 = Path()
        path2 = Path()
        path3 = Path()

        assert self.sched1 == Schedule.from_html(path1)
        assert self.sched2 == Schedule.from_html(path2)
        assert self.sched3 == Schedule.from_html(path3)

    def test_ensure_bookends(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_to_norg(self) -> None:
        p = Path()
        
        self.sched1.to_norg(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.norg_string1

        self.sched2.to_norg(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.norg_string2

        self.sched3.to_norg(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.norg_string3

    def test_to_json(self) -> None:
        p = Path()
        
        self.sched1.to_json(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.json_string1

        self.sched2.to_json(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.json_string2

        self.sched3.to_json(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.json_string3

    def test_as_html(self) -> None:
        p = Path()
        
        self.sched1.to_html(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.html_string1

        self.sched2.to_html(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.html_string2

        self.sched3.to_html(p)
        with open(p, 'r') as f:
            s = f.read()
        assert s == self.html_string3

    def test_as_norg(self) -> None:
        assert self.sched1.to_norg() == self.norg_string1
        assert self.sched2.to_norg() == self.norg_string2
        assert self.sched3.to_norg() == self.norg_string3

    def test_as_json(self) -> None:
        assert self.sched1.to_json() == self.json_string1
        assert self.sched2.to_json() == self.json_string2
        assert self.sched3.to_json() == self.json_string3

    def test_to_html(self) -> None:
        assert self.sched1.to_html() == self.html_string1
        assert self.sched2.to_html() == self.html_string2
        assert self.sched3.to_html() == self.html_string3

    def test_add(self) -> None:
        sched4 = self.sched1.copy()
        sched5 = self.sched2.copy()
        sched6 = self.sched3.copy()

        sched4.add()
        sched5.add() 
        sched6.add()

        assert ... in sched4
        assert ... in sched5
        assert ... in sched6

    def test_remove(self) -> None:
        sched4 = self.sched1.copy()
        sched5 = self.sched2.copy()
        sched6 = self.sched3.copy()

        sched4.remove()
        sched5.remove()
        sched6.remove()

        assert ... in sched4
        assert ... in sched5
        assert ... in sched6

    def test_ispartitioned(self) -> None:
        assert self.sched1.ispartitioned()
        assert self.sched2.ispartitioned()
        assert self.sched3.ispartitioned()

    def test_names(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_starts(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_starts_strings(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_add_routines(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_add_from_plan(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_add_adhoc(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_get_inds_of_relevant_blocks(self) -> None:
        assert self.sched1
        assert self.sched2
        assert self.sched3

    def test_add_to_block_by_index(self) -> None:
        sched4 = self.sched1.copy()
        sched5 = self.sched2.copy()
        sched6 = self.sched3.copy()

        sched4.add_to_block_by_index()
        sched5.add_to_block_by_index()
        sched6.add_to_block_by_index()

    def test_can_be_added(self) -> None:
        assert True

    def test_get_overlaps(self) -> None:
        assert True

    def test_overlaps_are_movable(self) -> None:
        assert True

    def test_allocate_in_time(self) -> None:
        assert True

    def test_add_over_block(self) -> None:
        assert Schedule.add_over_block() == ...
        assert Schedule.add_over_block() == ...
        assert Schedule.add_over_block() == ...

    def test_get_fixed_and_flex(self) -> None:
        assert Schedule.get_fixed_and_flex() == ...
        assert Schedule.get_fixed_and_flex() == ...
        assert Schedule.get_fixed_and_flex() == ...

    def test_entry_list_fits(self) -> None:
        assert Schedule.entry_list_fits() == ...
        assert Schedule.entry_list_fits() == ...
        assert Schedule.entry_list_fits() == ...

    def test_get_gaps(self) -> None:
        assert Schedule.get_gaps() == ...
        assert Schedule.get_gaps() == ...
        assert Schedule.get_gaps() == ...

    def test_get_fixed_groups(self) -> None:
        assert self.sched1.get_fized_groups() == []
        assert self.sched2.get_fized_groups() == []
        assert self.sched3.get_fized_groups() == []

    def test_fill_gaps(self) -> None:
        entries1 = self.sched1.schedule.copy()
        entries2 = self.sched2.schedule.copy()
        entries3 = self.sched3.schedule.copy()

        assert self.sched1.fill_gaps(...) == ...
        assert self.sched2.fill_gaps(...) == ...
        assert self.sched3.fill_gaps(...) == ...

    def test_smooth_between_fixed(self) -> None:
        entries1 = self.sched1.schedule.copy()
        entries2 = self.sched2.schedule.copy()
        entries3 = self.sched3.schedule.copy()

        assert self.sched1.smooth_between_fixed(...) == ...
        assert self.sched2.smooth_between_fixed(...) == ...
        assert self.sched3.smooth_between_fixed(...) == ...

    def test_smooth_entries(self) -> None:
        entries1 = self.sched1.schedule.copy()
        entries2 = self.sched2.schedule.copy()
        entries3 = self.sched3.schedule.copy()

        assert self.sched1.smooth_entries(...) == ...
        assert self.sched2.smooth_entries(...) == ...
        assert self.sched3.smooth_entries(...) == ...

    def test_time_weight_from_prio(self) -> None:
        assert self.sched1.time_weight_from_prio(...) == ...
        assert self.sched2.time_weight_from_prio(...) == ...
        assert self.sched3.time_weight_from_prio(...) == ...

    def test_is_valid(self) -> None:
        assert self.sched1.is_valid()
        assert self.sched2.is_valid()
        assert self.sched3.is_valid()

    def test_str(self) -> None:
        assert str(self.sched1) == self.exp_string1
        assert str(self.sched2) == self.exp_string2
        assert str(self.sched3) == self.exp_string3

    def test_repr(self) -> None:
        assert repr(self.sched1) == self.exp_string1
        assert repr(self.sched2) == self.exp_string2
        assert repr(self.sched3) == self.exp_string3
