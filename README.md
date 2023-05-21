# planager-py
Python prototype of a tool for planning, prioritizing, and tracking. Designed by me for me to be an all-in-one way to stay organized.

## Design Goals

To create a system that takes into account all obligations, goals, and values to optimally allocate time. This system should be:

* purely functional: the same inputs will always result in the same outputs, with so side-effects
* declarative: the entities (tasks, etc.) and settings I delare provide a complete specification of my system; I say 'what' and the software tells me 'when'.
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

## Overview of Vanilla Scheduling Algorithm

1. A default day is specified, which contains recurring activities and activities blocked out.
2. From plnaning (typically quarterly and weekly), non-recurring "big rock" activities are added, each with a priority level that determines which takes precedence among a set of items competing for the same time. 
3. From the store of long-term roadmaps and projects and their corresponding tasks, tasks are assigned according to schedule and priority.
4. When there are conflicts or too many tasks to fit in the available time, these are to be resolved first automatically according to the settings. 
5. The irresoluble conflicts or overloads are then resolved manually, but only by editing the declrations, upon which the schedule is recomputed.
