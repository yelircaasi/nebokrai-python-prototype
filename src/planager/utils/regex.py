import re
from dataclasses import dataclass


@dataclass
class Regexes:
    date: re.Pattern = re.compile("(\d{2,4})[^\d](\d\d?)[^\d](\d\d?)")
    first_line: re.Pattern = re.compile("^\s*(.*)\s*")
    nondigit: re.Pattern = re.compile("[^\d]")
    time_bar_text: re.Pattern = re.compile("(\d\d:\d\d) *\| *([^\n]+)")
    section_split: re.Pattern = re.compile("\n+\s*\*\s+")  # \s+")
    subsection_split: re.Pattern = re.compile("\n+\s*\*\*\s+")
    asterix_split: re.Pattern = re.compile("\n+\s*\*")
    # attributes_doubledash: re.Pattern = ...
    # attributes_singledash: re.Pattern = ...
    item_split: re.Pattern = re.compile("\n\s*[~-]+\s+")
    item1_split: re.Pattern = re.compile("\n\s*[~-]\s+")
    item2_split: re.Pattern = re.compile("\n\s*[~-]{2}\s+")
    # entry: re.Pattern = ...
    entry_split_old: re.Pattern = re.compile("\n(?=\*\* \d\d:\d\d \| )")
    entry_old: re.Pattern = re.compile(
        "\*\* (\d\d:\d\d) \| ([^\n]+)\n\n"
        "  - priority: +(\d+)\n"
        "  - ismovable: +(\w+)\n"
        "  - notes: +(.+?)\n"
        "  - normaltime: +(\d+)\n"
        "  - idealtime: +(\d+)\n"
        "  - mintime: +(\d+)\n"
        "  - maxtime: +(\d+)\n"
        "  - alignend: +(\w+)\n",
        re.DOTALL,
    )
    header_and_body: re.Pattern = re.compile(
        "@document.meta\n(.+)\n@end\n+(.*)", re.DOTALL
    )
    # number_dot_split: re.Pattern = ...
    link: re.Pattern = re.compile("\[(.*?)\]\{\:(.+?)\:\}|\{\:(.+?)\:\}\[(.+?)\]")
