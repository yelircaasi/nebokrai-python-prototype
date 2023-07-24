import re
from dataclasses import dataclass


@dataclass
class Regexes:
    first_line: re.Pattern = re.compile(r"^\s*(.*)\s*")
    item_title: re.Pattern = re.compile(r"[^\s~-].+")
    time_bar_text: re.Pattern = re.compile(r"(\d\d:\d\d) *\| *([^\n]+)")
    section_split: re.Pattern = re.compile(r"\n+\s*\*\s+")  # \s+")
    subsection_split: re.Pattern = re.compile(r"\n+\s*\*\*\s+")
    asterix_split: re.Pattern = re.compile(r"\n+\s*\*")
    item_split: re.Pattern = re.compile(r"\n\s*[~-]+ +")
    item1_split: re.Pattern = re.compile(r"\n+[~-] +")
    item2_split: re.Pattern = re.compile(r"\n*\s*[~-]{2}\s+")
    entry_split_old: re.Pattern = re.compile(r"\n(?=\*\* \d\d:\d\d \| )")
    header_and_body: re.Pattern = re.compile(
        r"@document.meta\n(.+)\n@end\n*(\n.*)", re.DOTALL
    )
    link_namefirst: re.Pattern = re.compile(r"\[(.*?)\]\{\:(.+?)\:\}")
    link_namelast: re.Pattern = re.compile(r"\{\:(.+?)\:\}\[(.+?)\]")
    attribute_pair: re.Pattern = re.compile(r"\n?\s*[-~]{1,2} (\w+): ([^\n]*)")
    name_and_segments: re.Pattern = re.compile(r"(.+?)\s+\|\|\s+([^\n]+)\s+")
