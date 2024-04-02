-- libraries: Aeon, brick, iris / structured-cli
-- https://input-output-hk.github.io/haskell.nix/index.html
-- https://hackage.haskell.org/package/base-4.19.1.0/docs/System-Console-GetOpt.html
-- https://github.com/haskell/aeson
-- https://hackage.haskell.org/package/aeson-schema
-- https://github.com/chshersh/iris
-- https://github.com/simonmichael/shelltestrunner
-- https://github.com/jtdaugherty/brick
-- https://github.com/ndmitchell/cmdargs
-- https://github.com/docopt/docopt.hs
-- https://github.com/pcapriotti/optparse-applicative
-- https://github.com/Gabriella439/optparse-generic
-- https://github.com/soenkehahn/getopt-generics
-- https://www.stephanschiffels.de/posts/2021-03-24-Haskell-CLI
-- https://github.com/jgm/pandoc
-- https://github.com/simonmichael/hledger
-- https://github.com/jecxjo/todo.hs
-- https://github.com/matterhorn-chat/matterhorn
-- https://github.com/psibi/tldr-hs
-- https://github.com/cachix/cachix
-- https://github.com/gelisam/hawk
-- https://github.com/judah/haskeline
-- https://github.com/passy/givegif/blob/master/app/Main.hs
-- https://github.com/soywod/unfog
-- https://github.com/maralorn/haskell-taskwarrior
-- https://github.com/ad-si/TaskLite
--
-- https://docs.dhall-lang.org/tutorials/Language-Tour.html
-- https://github.com/dhall-lang/dhall-haskell
--
-- https://fluffynukeit.com/series/haskell-nixos/
-- https://discourse.nixos.org/t/super-simple-haskell-development-with-nix/14287/3
-- https://nixos.wiki/wiki/Haskell
-- https://dimitarg.github.io/nixos-haskell/
-- https://myme.no/posts/2022-01-16-nixos-the-ultimate-dev-environment.html
-- https://nixos.asia/en/nixify-haskell
-- https://discourse.nixos.org/t/nix-haskell-development-2020/6170/16
-- https://discourse.nixos.org/t/developping-haskell-on-nixos-with-haskell-language-server-and-reflex-platform/11072
-- https://nixos.asia/en/dev
-- https://github.com/malteneuss/haskell-nixos/
--
-- read: Haskell Programming from First Principles, Effective Haskell, Haskell in Depth, 
--   Haskell Tutorial and Cookbook, Learn You A Haskell for Great Good, Practical Haskell, 
--   Haskell - The Craft of Functional Programming, The Haskell Road to Logic, Naths, and Programming,
--   Seven More Languages in Seven Weeks, Quick Functional Programming, Functional Programming for Dummies,
--   Learning Functional Programming
--
--   Type-Driven Development with Idris
--   Verified Functional Programming with Agda

Nebokrai.readAll :: DataPath -> (NkConfig, Roadmaps, Calendar, Routines, ActivityTracking)
  Nebokrai.readRoadmaps   :: Path -> Roadmaps
  Nebokrai.readCalendar   :: Path -> Calendar
  Nebokrai.readNkConfig   :: Path -> NkConfig
  Nebokrai.readRoutines   :: Path -> Routines
  Nebokrai.readTracking   :: Path -> Tracking
  Nebokrai.parseRoadmaps  :: Path -> RoadmapsRecord
  Nebokrai.parseCalendar  :: Path -> CalendarRecord
  Nebokrai.parseNkConfig  :: Path -> NkConfigRecord
  Nebokrai.parseRoutines  :: Path -> RoutinesRecord
  Nebokrai.parseTracking  :: Path -> TrackingRecord
  Nebokrai.createRoadmaps :: RoadmapsRecord -> Roadmaps
  Nebokrai.createCalendar :: CalendarRecord -> Calendar
  Nebokrai.createNkConfig :: NkConfigRecord -> NkConfig
  Nebokrai.createRoutines :: RoutinesRecord -> Routines
  Nebokrai.createTracking :: TrackingRecord -> Tracking

           readRoadmaps RoadmapsPath = createRoadmaps (parseRoadmaps RoadmapsPath)
           readCalendar CalendarPath = createCalendar (parseCalendar CalendarPath)
           readNkConfig NkConfigPath = createNkConfig (parseNkConfig NkConfigPath)
           readRoutines RoutinesPath = createRoutines (parseRoutines RoutinesPath)
           readTracking TrackingPath = createTracking (parseTracking TrackingPath)

Nebokrai.derive :: Calendar -> Roadmaps -> (Plan, Schedule)

  Nebokrai.derivePlan                         :: Calendar -> Roadmaps -> Plan
    Nebokrai.makeSubplan                      :: Project  -> Subplan  -> Project
    Nebokrai.Planning.addSubplanToPlan        :: Subplan  -> Plan     -> Plan
    Nebokrai.Planning.addTaskToDay            :: DayTasks -> Task     -> (DayTasks, [Task])
    Nebokrai.Planning.addTasksToDay           :: DayTasks -> [Task]   -> (DayTasks, [Task])
    Nebokrai.Planning.calculateTimeTotal      :: [Task]   -> Int
    Nebokrai.Planning.calculateTimeCollapsed  :: [Task]   -> Int
    Nebokrai.Planning.splitValidAndExcess     :: [Task]   -> AvailableTimeByBlock -> (DayTasks, [Task])
    Nebokrai.Planning.getAvailableTimeByBlock :: NkDay    -> DayTasks -> AvailableTimeByBlock
    Nebokrai.Planning.sortOnPriority          :: [Task]   -> [Tasks]
    Nebokrai.Planning.showPlanVerbose         :: Plan     -> Text
    Nebokrai.Planning.showPlanConcise         :: Plan     -> Text
    Nebokrai.Planning.showPlanDebug           :: Plan     -> Text
    Nebokrai.Planning.logDiffs                :: Plan     -> PlanDiffLog -- tracks difference between desired and actual scheduling

    
  Nebokrai.deriveSchedule                       :: Calendar    -> Plan     -> Schedule
    Nebokrai.Scheduling.scheduleDay             :: CalendarDay -> DayTasks -> (DaySchedule, [Task])
    Nebokrai.Scheduling.taskToEntry             :: Task        -> Entry
    Nebokrai.Scheduling.addTask                 :: DaySchedule -> Task     -> (DaySchedule, [Entry])
    Nebokrai.Scheduling.addEntry                :: DaySchedule -> Entry    -> (DaySchedule, [Entry])
    Nebokrai.Scheduling.addTasks                :: DaySchedule -> [Task]   -> (DaySchedule, [Entry])
    Nebokrai.Scheduling.addEntries              :: DaySchedule -> [Entry]  -> (DaySchedule, [Entry])
    Nebokrai.Scheduling.sortEntries             :: [Entry]     -> [Entry]
    Nebokrai.Scheduling.getAvailableTimeByBlock :: DaySchedule -> AvailableTimeByBlock
    Nebokrai.Scheduling.addEntryFixed           :: DaySchedule -> Entry -> DaySchedule
    Nebokrai.Scheduling.addEntryFlex            :: DaySchedule -> Entry -> DaySchedule
    Nebokrai.Scheduling.showScheduleVerbose     :: Schedule    -> Text
    Nebokrai.Scheduling.showScheduleConcise     :: Schedule    -> Text
    Nebokrai.Scheduling.showScheduleDebug       :: Schedule    -> Text
    Nebokrai.Scheduling.showDayScheduleVerbose  :: DaySchedule -> Text
    Nebokrai.Scheduling.showDayScheduleConcise  :: DaySchedule -> Text
    Nebokrai.Scheduling.showDayScheduleDebug    :: DaySchedule -> Text
    Nebokrai.Scheduling.logDiffs                :: Schedule    -> ScheduleDiffLog -- tracks difference between desired and actual scheduling
  
Nebokrai.trackActivity :: [ActivityTracker] -> IO () -> ActivityLog -- need to see how to handle IO
  -----------------------------------------------
import qualified Data.Map as Map

-- entities
type Plan = Map.Map NkDate Entry 
    -- deriving (Show, Read, Equals)

type Schedule { Entries :: [Entry],
} deriving (Show, Read, Equals)

type Task { Priority: Int
} deriving (Show, Read, Equals)

type Entry {

} deriving (Show, Read, Equals)

type Routine {

} deriving (Show, Read, Equals)

type Calendar Map.Map NkDate CalendarDay

type CalendarDay { Date :: NkDate
                 , Start :: NkTime
                 , End :: NkTime
                 , Entries :: [Entry]
                 , Routines :: [Routine]
} deriving (Show, Read, Equals)

type Project {

} deriving (Show, Read, Equals)

type Roadmap {

} deriving (Show, Read, Equals)

-- ?
type NkDate { Year :: Int
       , Month :: Int
       , Day :: Int
} deriving (Equals, Show, Read)

-- ?
type NkTime { Hour :: Int
            , Minute :: Int
} deriving (Equals, Show, Read)

type PromptConfig {}

type TrackingPrompt :: IO ()

-- Readers and Writers
Reader.readCalendar
Reader.readCalendarDay
Reader.readEntry
Reader.readPlan
Reader.readProject
Reader.readRoadmap
Reader.readRoutine
Reader.readSchedule
Reader.readTask
Reader.readPromptConfig

-- planning functions
derivePlan :: Calendar -> [Subplan] -> Plan

combineSubplans :: [Subplan] -> Plan

addPlanToCalendar :: Calendar -> Plan -> Plan

adjustPlan :: Plan -> Plan

rolloverTasks :: AvailableTime -> [Task] -> [Task] 
-- = mapAccumL ...; (use splitAt)

getTotalCollapsedTime :: [Task] -> Int

popLowestPriority :: AvailableTime -> [Task] -> Tuple([Task], [Task])

-- scheduling functions
deriveSchedule :: Calendar -> Plan -> Schedule

resolveSchedule :: Schedule -> [Tasks] -> Schedule







