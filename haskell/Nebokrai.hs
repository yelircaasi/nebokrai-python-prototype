module Nebokrai ( go ) where

import Brick
import Path                        (Path)

import Nebokrai.IO                 (readAll, readRoadmaps, readCalendar, readNkConfig, readRoutines, readTracking,
                                    writeAll, writeRoadmaps, writeCalendar, writeNkConfig, writeRoutines, writeTracking)
import Nebokrai.Utils.DateTime     (NkDate, NkTime, parseDate, parseTime)
import Nebokrai.Entities.Task      (Task)
import Nebokrai.Entities.Roadmap   (Roadmap)
import Nebokrai.Entities.Project   (Project)
import Nebokrai.Entities.Entry     (Entry, entryFromTask)
import Nebokrai.Entities.Routine   (Routine)
import Nebokrai.Entities.Schedule  (Schedule)
import Nebokrai.Entities.Plan      (Plan, Subplan)
import Nebokrai.Entities.Calendar  (Calendar, CalendarDay)
import Nebokrai.Tracking           (Tracking, Tracker)
import Nebokrai.Config             (NkConfig)

go :: Path -> IO ()
go nkpath = do
    nkConfig, roadmaps, calendar, routines, tracking = readAll nkpath
    void $ customMain -- initialVty builder (Just timerChan) app initial
    -- see https://github.com/smallhadroncollider/taskell/blob/master/src/Taskell.hs

