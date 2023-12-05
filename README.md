# planager-py

Python prototype of a tool for planning, prioritizing, and tracking. Designed by me for me to be an
all-in-one way to stay organized and motivated.

Still unstable and in undergoing rapid development. Currently written in the Python standard
library (no other dependencies), but liable to be re-written in another better-suited (perhaps
sexier?) language. The README may describe some not-yet-implemented features, as I am giving 
['readme-driven development'](https://tom.preston-werner.com/2010/08/23/readme-driven-development.html)
a try.

## Design Philosophy

planager is informed by a set of guiding principles, a few of which will likely sound familiar to
anyone who has spent time in or around software development:

* **declarativeness**: what we want is clearly specified in one place and the program is tasked with
  implementing said specification, as opposed to the user having to manually spell out every step -
  more on this in the [detailed design notes]()
* **purity**: no side effects
  - i.e. what is planned and scheduled follows directly and deterministically from the declaration
  - purity in this context brings with it a striking number of benefits:
    * **transparent relationship** between all components of the system, from long-terms plans and
      goals down to short-term schedules and to-do lists - this hints at the possibility of
      something analogous to backpropagation, but that is not yet on the horizon
    * **attribution**, i.e. low-level details like a daily schedule have their roots in what I 
      really want in the long run and if I don't like or understand something, I can trace it back 
      to the  declaration to understand why the program planned / scheduled it that way - in other 
      words, nothing is random and everything has a discoverable cause
* **resilience**: known to nerds as "fault tolerance"
  - life happens, and the ability to adjust a plan following failures  and setbacks is essential
  - plans and goals without resilience are simply too brittle and are likely to be abandoned in 
    frustration
* **observability and traceability via logging**: the practice and paradigm of keeping detailed 
  notes on what happened and how and why is that we can look at what went wrong and, conversely, 
  what went well
  - this brings with it accountability, which it turns out is important for humans for a number of
    reasons
  - prevents self-deception
  - opens the door to (teaser alert!) cool dashboards and visualizations
* **modularity**: the system consists of smaller parts, which in turn consist of smaller parts,
  and while they interact seamlessly, each is as coherent and self-contained as possible

## Features

### Planning

In keeping with [Habit #2]() - "Begin with the end in mind" - it is beneficial to set long-term
goals, as it guides short- and medium-term action. To this end, planager specifies a hierarchy of
units:

* roadmaps consist of projects
* projects consist of tasks
* tasks are self.contained atomic units

Conversely, each task belongs to a project, which in turn belongs to a roadmap. This child-parent
relationship ensures context.

Each unit has a number of properties (more on this later). Every child unit
inherits by default from its parent. For example, unless otherwise specified in the declaration,
a task has the same priority as the project to which it belongs.

Roadmaps as well as projects can specify attributes relating to timing, such as start time, end
time, cluster size (how many tasks from the given project to group together as a single unit),
desired interval, etc. Of course, only a subset of all possible combinations are valid.
Based on the declaration provided, including configuration parameters and the calendar ('big rock'
entries such as work or ad hoc appointments, routines, and other attributes relevant to planning
and scheduling), the algorithm then assigns each task to a day. This is good
for Gantt-style visualization, for example:

{example here}

Planning in this way is also a good way to make sure that the long-term objectives are realistic
within the constraints provided. If the total duration of all tasks is simply too great, the
declaration will fail. This is desirable: early failure duringm compilation is always preferrable
to failure later during  deployment. 

This implies an iterative planning process. I declare roadmaps, projects, and tasks along with a
calendar and configuration parameters. Then planager either allocates tasks to days, or informs
me that I cannot and provides helpful information as to why the declaration was impossible to
realize. Then I fix the offending parts of the declaration and repeat the process until I have a
feasible plan.

### Scheduling

From the plan, the next step is to create a schedule. Algorithmically, this turns out to be more
involved - see [this]() for details and discussion. The general process is as follows: 

1. Entries are c
2. Entries are added to days in order of priority such that all constraints are satisfied
3. Entry times are adjusted such that they partition the available time

Constraint types include:

* blocks and categories: entries may have block or category names specified, such as "work" or
  "transit", where an entry can be scheduled within another entry, such as work-related tasks (i.e.
  tasks bearing the "work" category tag) being scheduled inside an entry with the block tag "work",
  which is a planager-specific way of saying that work-related activities are scheduled during
  work hours
* categories can be binding or non-binding, where binding categories may be scheduled _exclusively_
  inside entries with the corresponding block tag, whereas a non-binding category allows scheduling
  inside or outside such entries
* entries can be fixed or movable (i.e. fixed start, fixed end), as can start and end times
* entries have an `order` attribute between 0 and 100, where 0 means "put me as early as possible
  and 100 says "put me as late as possible". The numbers are purely relative; their absolute
  magnitude has no meaning.
* entries may have earliest/latest start/end times (4 combinations)

The scheduler acts as a sort of temporal constraint solver to find the optimal schedule satisfying
the declaration and (more immediately) the plan.

One of the major benefits of planning in this way is the built-in-by-design requirement that priorities are respected when planning. For example, routines can be declared in their own section of the declaration, referenced on relevant days in the calendar, and then included in planning and scheduling. To borrow yet another phrase from computer science, this is a sort of ahead-of-time compilation, which makes possible a high degree of optimization.

### Tracking

To understand what is working and what is not, it is important to have a clear record of what actually happened. As psychological studies have shown, memory is often unreliable and deceptive. Without data, I can easily overestimate the extent to which I have eaten healthily or the amount of time I spent actually working on projects (with my brain engaged, not just sitting in the right chair). Activity tracking is the antidote to these problems.

On the other hand, tracking is tedious, and in many forms it is quite burdensome. Any system attempting to facilitate tracking needs to mitigate this. An easy interactive CLI and a mobile interface via the Signal app (and later others) are two approaches that make tracking if not outright enjoyable, at least more pleasant and less of a chore.

### CLI

Coming soon...

### Mobile Integration via Signal

Coming soon...

### 'Maybe later' Features

* something akin to GTD (Getting Things Done)
* Taskwarrior and Timewarrior integration
* integration with Neorg
* TUI, including Gantt and calendar views and vim keybindings and color customizations
* native Android app / Linux mobile / etc
* 

## Usage

```shell
planager derive
```

## Installation

Use pipx, the silver bullet solution to installing Python CLI tools.

```shell
pipx install planager
```

## Roadmap

- [x] create roadmap :)
- [x] re-write in a functional style; 
  - [x] all algorithmically interesting methods to their own functions (except where there it makes good semantic sense to prefer methods)
  - [x] make classes handle data and how it is displayed, providing just an interface; all logic should be done in pure functions

mypy errors

- [x] src/planager/cli.py
- [x] src/planager/entity/container/schedules.py
- [x] src/planager/entity/base/schedule.py
- [x] src/planager/entity/base/plan.py
- [x] src/planager/entity/base/roadmap.py
- [x] src/planager/entity/base/calendar.py
- [x] src/planager/entity/container/projects.py
- [x] src/planager/entity/base/project.py
- [x] src/planager/entity/base/routine.py
- [x] src/planager/entity/container/tasks.py
- [x] src/planager/entity/base/entry.py
- [x] src/planager/util/serde/deserialization.py
- [x] src/planager/configuration.py
- [x] src/planager/util/__init__.py
- [x] src/planager/util/prompt/prompt.py
