import re
from dataclasses import dataclass


@dataclass
class Regexes:
    """
    Collection of regexes used throughout nebokrai.
    """

    item_split: re.Pattern = re.compile(r"\s+[~-]+\s*")
    item1_split: re.Pattern = re.compile(r"\s+[~-] +")
    header_and_body: re.Pattern = re.compile(r"@document.meta\n(.+)\n@end\n*(\n.*)", re.DOTALL)
    link_namefirst: re.Pattern = re.compile(r"\[(.+?)\]\{\:(.+?)\:\}")
    attribute_pair: re.Pattern = re.compile(r"\n?\s*[-~]{1,2} (\w+)\s*: ([^\n]+[^\s]) *")
    name_and_segments: re.Pattern = re.compile(r"([^~\-\s].*?)\s+\|\|\s+([^\n]+?)\s*")
