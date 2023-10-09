import json

with open("/home/isaac/Learning/projects/Learning/ganttouchthis-data/projects.json") as f:
    p = json.load(f)
nl = "\n"
for d in p:
    print(
        f"{nl}* {d['name']}{nl}  ** link: {d['link']}{nl}  ** tasks: {d['tasks']}{nl}  ** start: {d['start']}{nl}  ** end: {d['end']}{nl}  ** priority: {d['priority']}{nl}  ** interval: {d['interval']}{nl}  ** cluster: {d['cluster']}{nl}  ** duration: {d['duration']}{nl}  ** tags:{f'{nl}     *** '.join([''] + d['tags'])}{nl}  ** description: {d['description']}"
    )
