import re
from dataclasses import dataclass


@dataclass
class Regexes:
    first_line: re.Pattern = re.compile("^\s*(.*)\s*")
    item_title: re.Pattern = re.compile("[^\s~-].+")
    time_bar_text: re.Pattern = re.compile("(\d\d:\d\d) *\| *([^\n]+)")
    section_split: re.Pattern = re.compile("\n+\s*\*\s+")  # \s+")
    subsection_split: re.Pattern = re.compile("\n+\s*\*\*\s+")
    asterix_split: re.Pattern = re.compile("\n+\s*\*")
    item_split: re.Pattern = re.compile("\n\s*[~-]+\s+")
    item1_split: re.Pattern = re.compile("\n\s*[~-]\s+")
    item2_split: re.Pattern = re.compile("\n\s*[~-]{2}\s+")
    entry_split_old: re.Pattern = re.compile("\n(?=\*\* \d\d:\d\d \| )")
    header_and_body: re.Pattern = re.compile(
        "@document.meta\n(.+)\n@end\n+(.*)", re.DOTALL
    )
    link: re.Pattern = re.compile("\[(.*?)\]\{\:(.+?)\:\}|\{\:(.+?)\:\}\[(.+?)\]")
    attribute_pair: re.Pattern = re.compile("\n?\s*[-~]{1,2} (\w+): ([^\n]*)")
