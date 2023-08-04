import re
from dataclasses import dataclass


@dataclass
class Regexes:
    item_split: re.Pattern = re.compile(r"\s+[~-]+\s*")
    item1_split: re.Pattern = re.compile(r"\s+[~-] +")
    header_and_body: re.Pattern = re.compile(
        r"@document.meta\n(.+)\n@end\n*(\n.*)", re.DOTALL
    )
    link_namefirst: re.Pattern = re.compile(r"\[(.+?)\]\{\:(.+?)\:\}")
    attribute_pair: re.Pattern = re.compile(
        r"\n?\s*[-~]{1,2} (\w+)\s*: ([^\n]+[^\s]) *"
    )
    name_and_segments: re.Pattern = re.compile(r"([^~\-\s].*?)\s+\|\|\s+([^\n]+?)\s*")
    # first_line: re.Pattern = re.compile(r"^\s*([^\n]+?)\s*$|^\s*([^\n]+?)\s*\n.*$")
    # item_title: re.Pattern = re.compile(r"[^\s~-][^\n]+")
    # time_bar_text: re.Pattern = re.compile(r"(\d\d:\d\d) *\| *([^\n]+)")
    # section_split: re.Pattern = re.compile(r"\n+\s*\*\s+")  # \s+")
    # subsection_split: re.Pattern = re.compile(r"\n+\s*\*\*\s+")
    # asterix_split: re.Pattern = re.compile(r"\n+\s*\*")
    # item2_split: re.Pattern = re.compile(r"\n*\s*[~-]{2}\s+")
    # link_namelast: re.Pattern = re.compile(r"\{\:(.+?)\:\}\[(.+?)\]")
