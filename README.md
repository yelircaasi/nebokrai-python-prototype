# planager-py
Python prototype of a tool for planning, prioritizing, and tracking. Designed by me for me to be an all-in-one way to stay organized.

## Design Goals

Create a system that takes into account all obligations, goals, and values to optimally allocate time. This system should be:

* purely functional: the same inputs will always result in the same outputs, with no side-effects
* declarative: the entities.base (tasks, etc.) and settings declared provide a complete specification of my system; I say 'what' and the software tells me 'when'.
* simple and intuitive to use
* robust: when circumstances change, I can adjust the plans via the interface provided (as opposed to internal hacking) and carry on without problems
* integrated: planager provides an all-encompassing system to keep all aspects of my life in order
* simplifying: this tool should save me time and reduce my cognitive load, not become a distraction or an obstacle

## Entity Types

* roadmap: a 'master plan' for some area such as "Rust programing language" or "muscular flexibility" involving multiple steps or projects
* project: a self-contained unit of work that can be broken down into smaller parts, such as a book to read or a coding project
* task: a small, atomic unit of work, ideally one that can be completed in less than 120 minutes; can be recurring or one-time
* sequences: an alias for a list of tasks which are always to be performed together (typically sequentially), such as a morning or evening routine; handled identically to a task
* option set: a group of alternatives, from which I select one (or more); handled identically to a task

## Planning Algorithm (Vanilla):

1. Get daily time available from calendar. 
2. Then fill up each day according to priority. 
3. When a task is displaced, log the displacement ( -> work on helpful error messages).

## Scheduling Algorithm (Vanilla)

High-level description:

1. A base schedule is specified in the calendar, which contains default recurring activities.
2. From planning (typically quarterly and weekly), non-recurring "big rock" activities are added, each with a priority level that determines which takes precedence among a set of items competing for the same time. 
3. From the store of long-term roadmaps and projects and their corresponding tasks, tasks are assigned according to schedule and priority.
4. When there are conflicts or too many tasks to fit in the available time, these are to be resolved first automatically according to the settings. 

The irresoluble conflicts or overloads are then resolved manually, but only by editing the declarations, upon which the schedule is recomputed.

Low-level description of scheduling algorithm:

1. check whether the entries fit in a day
2. get the compression factor, i.e. how much, on average, the entries need to be compacted in order to fit
3. separate entries into fixed (immovable) and flex (movable)
4. add the fixed entried to the schedule
5. identify the gaps
6. fill in the gaps with the flex items TODO
7. resize between fixed points to remove small empty patches (where possible)

TODO: add `alignend` functionality (but first get it working without)

### Signal module:

dependencies:

* planager.tracking
* planager.schedule
* semaphore (Python package)

### Entry Adding

An Entry object can be added to a Schedule object from one of 5 origins:

* from Calendar (base schedules)
* from plan via explicit declaration in project file
* from plan via project expansion from roadmap file
* from AdHoc, from adhoc file
* from Routines, from routines file


### Habits / metrics to track:

all foods (with times)
time breaking fast
last time eating
bool: entirely plant-based? entirely non-processed?
food score

cold shower
daily walk (5x/week)
run (5x/week) - with recorded data
sets of pushups
sets of pullups
stretching
wisdom literature
last use of phone

number of texts sent
emails clean? (both) bookmarks clean?
journal
cleanliness & orderliness of apartment
bool: mast


30 minutes doing absolutely nothing
bool: getting lost in a good book
quality of meditation
something new I learned
which languages I used


TRACKING: manually via neorg, or via semaphore. One file per metric for easy tracking; move dates more than 30 days old to the old store (more efficient format?)


## Roadmap

[✓] rename universe to Planager

[✓] add `order` attribute to Entry, such that tasks can be ordered temporally indgependently of priority

[✓] fix attributes of routines (such as maxtime) for proper initialization

[✓] major refactoring to separate by entity types and remove plurals from module names

[✓] clean up imports to make relative wherever possible

[✓] fix all mypy errors

[✓] visualize with [pydeps](https://github.com/thebjorn/pydeps) and refactor accordingly

[✓] fix id to be string

[✓] remove ambiguity (**kwargs) in norg reading

[ ] migrate List[Entry] to Entries

[ ] move internal norg dicts to classes for better verification

[ ] create norg visualization via `__repr__`

[ ] 

[ ] add support for norg task status (for completed)

[ ] clean up and solidify norg readers and writers

[ ] add json readers and writers

[ ] add html readers and writers

[ ] write tests for each class, function, and method

[ ] write logger

[ ] add logging to entire library

[ ] get planning working as expected

[ ] get scheduling working as expected

[ ] make adhoc counterpart to plan, containing tasks (but one-off, non-derivable) -> adhoc folder containing a file for each day

[ ] calendar is direct parent of schedules, containing entries and day parameters -> calendar folder containing a file for each day

[ ] add tracking module mvp

[ ] write signal package for messaging
