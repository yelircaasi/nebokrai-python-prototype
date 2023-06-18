from pathlib import Path

import planager as p

ws = Path("/root/Learning/planager-data")
u = p.Universe.from_norg_workspace(ws)
print(u.adhoc)
print(u.routines)
print(u.roadmaps)
print(u.roadmaps[1])
print(u.roadmaps[2])
print(u.roadmaps[0])
print(u.roadmaps[0].projects[0])
print(u.roadmaps[0].projects[0]._tasks)
print(u.roadmaps[0].projects[0][1])
print(u.roadmaps[8].projects[1][1])
print(u.roadmaps[8].projects[1])
print(u[(8, 1)]._tasks)
"""
print(u[1])
print(u.roadmaps[(1, 1)])
print(u[(1, 1)])
print(u.roadmaps[1].projects[1])
print(u.roadmaps[1].projects[1].tasks)

print(u[(1, 1, 1)])
print(u.roadmaps[1].projects[1].tasks)
"""
