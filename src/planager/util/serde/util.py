import re


def split_tag_sequence(tags: str) -> set[str]:
    return set(re.split(r", ?|,? ", tags))
