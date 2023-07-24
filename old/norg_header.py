import re
from typing import Dict, List, Union

"""
from .pdatetime import PDateTime


class NorgHeader:
    def __init__(self) -> None:
        ...

    @classmethod
    def from_dict(cls, __dict: dict) -> "NorgHeader":
        ...
        return cls()

    @staticmethod
    def as_string(
        title: str,
        doc_id: str,
        parent: str,
        updated: str = PDateTime.now_str(),
        author: str = "yelircaasi",
        description: str = "",
        categories: Union[str, list] = "",
    ) -> str:
        # inner = "\n".join(
        #     map(": ".join, map(lambda kv: (kv[0], str(kv[1])), kwargs.items()))
        # )
        categories = (
            ", ".join(categories) if isinstance(categories, list) else categories
        )
        kv_pairs = [
            f"title: {title}",
            f"id: {doc_id}",
            f"parent: {parent}",
            f"updated: {updated}",
            f"author: {author}",
            f"description: {description}",
            f"categories: {categories}",
        ]
        inner = "\n".join(filter(bool, kv_pairs))
        return f"@document.meta\n{inner}\n@end"

    @staticmethod
    def get_list_from_header(header: str) -> List[Dict[str, str]]:
        header_info = []
        for k, v in re.findall("([^:\n]+): ([^\n]*)\n", header):
            header_info.append({"key": k, "value": v})
        return header_info

    @staticmethod
    def make_norg_header(
        title: str,
        author: str = "yelircaasi",
        categories: List[str] = [],
        version: Union[float, str] = "0.1",
    ) -> str:
        return "\n".join(
            (
                "@document.meta",
                f"title: {title}",
                f"authors: [{author}]",
                f"categories: {', '.join(categories)}",
                f"version: {str(version)}",
                "@end",
                "",
                ".toc",
                "",
                "* Schedule",
                "",
            )
        )
"""
