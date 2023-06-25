from pathlib import Path

import planager

ws = Path.expanduser(Path("~/Learning/planager-data"))
p = planager.Planager.from_norg_workspace(ws)
print(p.adhoc)
print(p.routines)
print(p.roadmaps)
print(p.plan.start_date)
print(p.plan.end_date)
print()
with open("/tmp/repr.txt", "w") as f:
    f.write(str(p))
# print(u)
# print(u.roadmaps[1])
# print(u.roadmaps[2])
# print(u.roadmaps[0])
# print(u.roadmaps[0]._projects[0])
# print(u.roadmaps[0]._projects[0]._tasks)
# print(u.roadmaps[0]._projects[0][1])
# print(u.roadmaps[8]._projects[1][1])
# print(u.roadmaps[8]._projects[1])
"""
print(u[8][1]._tasks)
print(u[1])
print(u.roadmaps[(1, 1)])
print(u[(1, 1)])
print(u.roadmaps[1].projects[1])
print(u.roadmaps[1].projects[1].tasks)

print(u[(1, 1, 1)])
print(u.roadmaps[1].projects[1].tasks)
"""
