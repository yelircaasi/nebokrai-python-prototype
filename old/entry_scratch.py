from pathlib import Path

import pytest

from planager.entity.base.entry import FIRST_ENTRY, LAST_ENTRY, Empty, Entry
from planager.util.pdatetime import PTime

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
    mintime=20,
    alignend=False,
    order=50,
)
entry_430_630 = Entry(  # 'elif start and end' -> normaltime 120
    "Entry 3",
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
    mintime=105,
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
    maxtime=420,
    order=45,
)
entry_0_030 = Entry("random name", PTime(0))  # 'else'

exp_string_0_5 = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 00:00-05:00 │ First Entry                                                    ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ notes:        notes on entry 1                                               ┃\n"
    "┃ priority:     70                                                             ┃\n"
    "┃ time:         270  (240-360, ideal: 330)                                     ┃\n"
    "┃ blocks:       block 1, block 2, block 3, block 4                             ┃\n"
    "┃ categories:   category 1, category 2, category 3, wildcard                   ┃\n"
    "┃ alignend:     true                                                           ┃\n"
    "┃ order:        80                                                             ┃"
)
exp_string_430_5 = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 04:30-05:00 │ Entry 2                                                        ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ priority:     95                                                             ┃\n"
    "┃ time:         30  (20-60, ideal: 40)                                         ┃"
)
exp_string_430_630 = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 04:30-06:30 │ Entry 3                                                        ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ notes:        long placeholder notes here that take space; long placeholder  ┃\n"
    "┃                 notes here that take space; long placeholder notes here      ┃\n"
    "┃                 that take space; long placeholder notes here that take       ┃\n"
    "┃                 space; long placeholder notes here that take space;          ┃\n"
    "┃ priority:     0                                                              ┃\n"
    "┃ time:         120  (60-240, ideal: 180)                                      ┃\n"
    "┃ blocks:       block 1, block 2                                               ┃\n"
    "┃ categories:   category 1, category 2, wildcard                               ┃"
)
exp_string_5_520 = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 05:00-05:20 │ Entry the fourth                                               ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ notes:        just some placeholder text, !@#$#@%#^$just some placeholder    ┃\n"
    "┃                 text, !@#$#@%#^$just some placeholder text, !@#$#@%#^$       ┃\n"
    "┃ priority:     0                                                              ┃\n"
    "┃ time:         20  (10-40, ideal: 30)                                         ┃\n"
    "┃ categories:   category 3, wildcard                                           ┃\n"
    "┃ ismovable:    false                                                          ┃\n"
    "┃ alignend:     true                                                           ┃"
)
exp_string_7_1030_a = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 07:00-10:30 │ Entry 5                                                        ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ notes:        some basic notes                                               ┃\n"
    "┃ time:         210  (105-420, ideal: 315)                                     ┃\n"
    "┃ order:        20                                                             ┃"
)
exp_string_7_1030_b = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 07:00-10:30 │ Entry 6                                                        ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ priority:     30                                                             ┃\n"
    "┃ time:         210  (105-420, ideal: 315)                                     ┃\n"
    "┃ blocks:       block1, block2, block3, block4                                 ┃\n"
    "┃ ismovable:    false                                                          ┃\n"
    "┃ order:        45                                                             ┃"
)
exp_string_0_030 = (
    "┣━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫\n"
    "┃ 00:00-00:30 │ random name                                                    ┃\n"
    "┠─────────────┴────────────────────────────────────────────────────────────────┨\n"
    "┃ time:         30  (15-60, ideal: 45)                                         ┃"
)


print(entry_0_5)
print(exp_string_0_5)
print(entry_0_5 == exp_string_0_5)
print()
print(entry_430_5)
print(exp_string_430_5)
print(entry_430_5 == exp_string_430_5)
print()
print(entry_430_630)
print(exp_string_430_630)
print(entry_430_630 == exp_string_430_630)
print()
print(entry_5_520)
print(exp_string_5_520)
print(entry_5_520 == exp_string_5_520)
print()
print(entry_7_1030_a)
print(exp_string_7_1030_a)
print(entry_7_1030_a == exp_string_7_1030_a)
print()
print(entry_7_1030_b)
print(exp_string_7_1030_b)
print(entry_7_1030_b == exp_string_7_1030_b)
print()
print(entry_0_030)
print(exp_string_0_030)
print(entry_0_030 == exp_string_0_030)
