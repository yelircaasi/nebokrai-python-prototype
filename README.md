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

### Project and Task Dependency Logic

* use only `.after` attribute; `.before` superfluous
* add `.tmpdate` (or maybe `.placeholder_date`) attribute to tasks for sorting; default NullDate to allow for easy complex comparisons
* 2-pass approach for planning: first regular planning to assign tmpdate, then adjust for dependencies
* use special sorting (`__gt__ , __lt__, __ge__, __le__`) that first looks at `.after`, then at `.tmpdate`

### Blocking Logic

* blocks like 'work' that other smaller, more specific tasks can be scheduled on top of
* Blocks come from Calendar, AdHoc, Routines
* Potentially also from regular (roadmap-originating) tasks
* used to 'collapse' durations together for planning and scheduling

### Task 'Stacking'

* combining tasks that can be done simultaneously, such as listening to a podcast on the way home
* also allows 'time collapsing' during planning, scheduling with require something new and custom

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

* [✓] rename universe to Planager

* [✓] add `order` attribute to Entry, such that tasks can be ordered temporally indgependently of priority

* [✓] fix attributes of routines (such as maxtime) for proper initialization

* [✓] major refactoring to separate by entity types and remove plurals from module names

* [✓] clean up imports to make relative wherever possible

* [✓] fix all mypy errors

* [✓] visualize with [pydeps](https://github.com/thebjorn/pydeps) and refactor accordingly

* [✓] fix id to be string

* [✓] remove ambiguity (**kwargs) in norg reading

* [✓] migrate List[Entry] to Entries

* [✓] move internal norg dicts to classes for better verification

* [✓] create norg visualization via `__repr__`

* [✓] add support for norg task status (for completed)

* [✓] add blocking logic

* [✓] add basic dependency logic for projects and tasks, integrated in planning

* [ ] refactor Entries.smooth_entries (30)

* [ ] add functionality for a cluster of Tasks to be merged into a single Entity (Tasks class? Entity class method?) (& update test skeletons)

* [ ] add first_line_offset kwarg to str repr functions for norg printing (30)

* [ ] write tests for each class, function, and method (see checklist)
      
      [] Entry
         [✓] write       (60)
         [] get passing  (180)
      [] Entries
         [] write        (90)
         [] get passing  (60)
      [] Task
         [] write        (180)
         [] get passing  (60)
      [] Tasks
         [] write        (90)
         [] get passing  (30)
      [] Project
         [] write        (90)
         [] get passing  ()
      [] Projects
         [] write        (60)
         [] get passing  (30)
      [] Schedule
         [] write        (240)
         [] get passing  (240)
      [] Schedules
         [] write        (30)
         [] get passing  (30)
      [] Plan
         [] write        (180)
         [] get passing  (60)
      [] Roadmap
         [] write        (60)
         [] get passing  (60)
      [] Roadmaps
         [] write        (60)
         [] get passing  (60)
      [] AdHoc (without json and html for now)
         [] write        (60)
         [] get passing  (30)
      [] Calendar
         [] write        (60)
         [] get passing  (30)
      [] Routine
         [] write        (90)
         [] get passing  (30)
      [] Routines
         [] write        ()
         [] get passing  ()

* [ ] add basic dependency logic for entries, integrated in scheduling (& update tests)

* [ ] refine dependency logic for projects and tasks, integrated in planning (& update tests)

* [ ] refine dependency logic for entries, integrated in scheduling (& update tests)

* [ ] add task stacking logic (& update tests)

* [ ] clean up and solidify norg readers and writers (& update tests)

* [ ] add json readers and writers (& update tests)

* [ ] add html readers and writers (& update tests)

* [ ] write logger (& update tests)

* [ ] add logging to entire library (& update tests)

* [ ] get planning working as expected (& update tests)

* [ ] get scheduling working as expected (& update tests)

* [ ] make adhoc counterpart to plan, containing tasks (but one-off, non-derivable) -> adhoc folder containing a file for each day (& update tests)

* [ ] calendar is direct parent of schedules, containing entries and day parameters -> calendar folder containing a file for each day (& update tests)

* [ ] add tracking module mvp (& update tests)

* [ ] write signal package for messaging (& update tests)

* [ ] refine tracking module (& update tests)


## Checklist

*  [ ] planager.util
*     [ ] planager.util.data
*         [✓] planager.util.data.__init__
*             [✓] written
*             [-] tests written
*             [✓] tests passed
*         [ ] planager.util.data.norg
*             [✓] planager.util.data.norg.norg.Norg
*                 [✓] written
*                 [✓] tests written
*                 [ ] tests passed
*             [ ] planager.util.data.norg.norg_item.NorgItem
*                 [✓] written
*                 [ ] tests written
*                 [ ] tests passed
*             [ ] planager.util.data.norg.norg_item.NorgItems
*                 [✓] written
*                 [ ] tests written
*                 [ ] tests passed
*             [ ] planager.util.data.norg.norg_header.NorgHeader
*                 [ ] written
*                 [ ] tests written
*                 [ ] tests passed
*         [ ] planager.util.data.html.html.HTML
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.util.data.json.json.JSON
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*     [✓] planager.util.display
*         [✓] planager.util.repr.wrap_as_list
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*         [✓] planager.util.display.repr.wrap_string
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*         [✓] planager.util.display.repr.tabularize
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*     [✓] planager.util.pdatetime
*         [✓] planager.util.pdatetime.pdate.PDate
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*         [✓] planager.util.pdatetime.pdatetime.PDateTime
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*         [✓] planager.util.pdatetime.ptime.PTime
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*     [✓] planager.util.misc
*         [✓] planager.util.misc.round5
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*         [✓] planager.util.misc.expand_task_segments
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*     [✓] planager.util.regex
*         [✓] planager.util.regex.Regexes
*             [✓] planager.util.regex.Regexes.item_split
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*             [✓] planager.util.regex.Regexes.item1_split
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*             [✓] planager.util.regex.Regexes.item1_split
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*             [✓] planager.util.regex.Regexes.item2_split
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*             [✓] planager.util.regex.Regexes.header_and_body
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*             [✓] planager.util.regex.Regexes.link
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*             [✓] planager.util.regex.Regexes.attribute_pair
*                 [✓] written
*                 [✓] tests written
*                 [✓] tests passed
*     [✓] planager.util.type
*         [✓] planager.util.type.ClusterType
*             [✓] written
*             [✓] tests written
*             [✓] tests passed
*     [ ] planager.util.path_manager
*         [ ] planager.util.path_manager.PathManager
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
* [ ] planager.entity
*     [ ] planager.entity.base
*         [ ] planager.entity.base.__init__
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.adhoc.AdHoc
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.calendar.Calendar
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.entry.Entry
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.plan.Plan
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.project.Project
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.roadmap.Roadmap
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.routine.Routine
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.schedule.Schedule
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
*         [ ] planager.entity.base.task.Task
*             [ ] written
*             [ ] tests written
*             [ ] tests passed
* [ ] planager.container
*     [ ] planager.container.__init__
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.container.entries.Entries
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.container.projects.Projects
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.container.roadmaps.Roadmaps
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.container.routines.Routines
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.container.schedules.Schedules
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.container.tasks.Tasks
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
* [ ] planager.patch
*     [ ] planager.patch.__init__
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.patch.plan_patch.PlanPatch
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.patch.plan_patch.PlanPatches
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.patch.schedule_patch.SchedulePatch
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.patch.schedule_patch.SchedulePatches
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.patch.task_patch.TaskPatch
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.patch.task_patch.TaskPatches
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
* [ ] planager.operator
*     [ ] planager.__init__.__all__
*         [ ] written
*         [ ] tests written
*         [ ] tests passed    
*     [ ] planager.patch.task_patch.TaskPatch
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.operator.planner
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.operator.scheduler
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.operator.patcher.__init__
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.operator.patcher.PlanPatcher
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.operator.patcher.SchedulePatcher
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
*     [ ] planager.operator.patcher.TaskPatcher
*         [ ] written
*         [ ] tests written
*         [ ] tests passed
* [ ] planager.tracking
*     [ ] planager.tracking.__init__
*         [ ] written
*         [ ] tests written
*         [ ] tests passed

## Adjustment Types (old)

```python
class AdjustmentType(Enum):
    AUTO = 0  # methods figure it out, based on priority and properties
    CLIP = 1  # higher-priority entry takes precedence and lower-priority activity makes way
    SHIFT = 2  #
    COMPRESS = 3  #
    COMPROMISE = 4  #
    DISPLACE = 5  #
```