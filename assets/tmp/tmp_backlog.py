import json
with open("/home/isaac/Learning/ganttouchthis-data/backlog.json") as f:
  p = [v for k, v in json.load(f)["_default"].items()]
nl = "\n"
def pp(d):
  return f"{2 * nl}* {d['name']}{nl}  ** link: {d['link']}{nl}  ** tasks: {d['tasks']}{nl}  ** priority: {d['priority']}{nl}  ** cluster: {d['cluster']}{nl}  ** duration: {d['duration']}{nl}  ** tags:{f'{nl}     *** '.join([''] + d['tags'])}{nl}  ** description: {d['description']}"
import itertools
tags = set(itertools.chain.from_iterable([d["tags"] for d in p]))
occs = {tag: len(list(filter(lambda d: tag in d["tags"], p))) for tag in tags}
freq = set([k for k, v in occs.items() if v > 13])
other = list(filter(lambda d: freq.intersection(d["tags"]) == set(), p))

for name in freq:
  for d in list(filter(lambda d: name in d["tags"], p)):
    with open(f"backlog_{name.lower()}.norg", 'a') as f:
      f.write(pp(d))
    p.remove(d)

for d in other:
    with open(f"backlog_other.norg", 'a') as f:
      f.write(pp(d))
