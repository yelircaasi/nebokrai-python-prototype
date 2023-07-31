import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ...display import wrap_string
from ...pdatetime import PDateTime
from ...regex import Regexes

from .norg_item import NorgItem, NorgItems
from .norg_item_head import NorgItemHead


class Norg:
    def __init__(
        self,
        title: str = "",
        description: str = "",
        author: str = "",
        doc_id: str = "none",
        parent: str = "none",
        updated: PDateTime = PDateTime.now(),
        categories: str = "",
        items: NorgItems = NorgItems(),
        path: Optional[Path] = None,
    ) -> None:
        self.title = title
        self.description = description
        self.author = author
        self.doc_id = doc_id
        self.parent = parent
        self.updated = updated
        self.categories = categories
        self.items = items
        self.path = path

    @classmethod
    def from_path(cls, norg_path: Path) -> "Norg":
        """
        Reads and parses a .norg file into a Norg class.
        Norg.from_string() does most of the heavy lifting here.
        """
        with open(norg_path) as f:
            norg_str = f.read()
        norg_obj = cls.from_string(norg_str)
        norg_obj.path = norg_path
        return norg_obj

    @classmethod
    def from_string(cls, norg_str) -> "Norg":
        regx_header_and_body = Regexes.header_and_body

        result = re.search(regx_header_and_body, norg_str)
        if result:
            header, body = result.groups()
        else:
            raise ValueError("Norg document lacks valid header.")

        kwarg_dict: Dict[str, Any] = dict(
            map(lambda x: x.split(": ", 1), str(header).split("\n"))
        )
        kwarg_dict["updated"] = PDateTime.from_string(kwarg_dict["updated"])

        with open("/tmp/y.norg", "w") as f:
            f.write(norg_str)
        if body:
            with open("/tmp/x.norg", "w") as f:
                f.write(body)

        n = NorgItems.from_string(body)
        with open("/tmp/w.norg", "w") as f:
            f.write("------\n")
            f.write("\n\n".join([str(item) for item in n]))

        return cls(
            title=kwarg_dict["title"],
            description=kwarg_dict["description"],
            author=kwarg_dict["author"],
            doc_id=kwarg_dict["id"],
            parent=kwarg_dict["parent"],
            updated=kwarg_dict["updated"],
            categories=kwarg_dict["categories"],
            items=NorgItems.from_string(body),
        )

    def __str__(self) -> str:
        def make_header() -> str:
            return "\n".join(
                (
                    "@document.meta",
                    f"title: {self.title}",
                    f"description: {self.description}",
                    f"categories: {self.categories}",
                    f"id: {self.doc_id}",
                    f"parent: {self.parent}",
                    f"updated: {str(self.updated)}",
                    f"author: {self.author}",
                    "@end",
                )
            )

        def make_body() -> str:
            return "\n\n".join(map(str, self.items))

        return f"{make_header()}\n\n{make_body()}\n"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def norg_item(*args, **kwargs) -> NorgItem:
        return NorgItem(*args, **kwargs)

    @staticmethod
    def norg_item_from_string(norg_string: str) -> NorgItem:
        return NorgItem.from_string(norg_string)

    @staticmethod
    def norg_items(*args, **kwargs) -> NorgItems:
        return NorgItems(*args, **kwargs)

    @staticmethod
    def norg_item_head(*args, **kwargs) -> NorgItemHead:
        return NorgItemHead(*args, **kwargs)
