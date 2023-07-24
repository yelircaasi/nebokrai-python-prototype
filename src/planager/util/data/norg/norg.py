import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ...display import wrap_string
from ...pdatetime import PDateTime
from ...regex import Regexes

from .norg_item import NorgItem, NorgItems
from .norg_link import NorgLink


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

        # def parse_section(section_str: str) -> Optional[Dict[str, Any]]:
        #     regx_subsections = Regexes.subsection_split
        #     section_dict = {
        #         "title": "",
        #         "text": "",
        #         "attributes": {},
        #         "subsections": [],
        #     }
        #     res = re.search("\*?([^\n]+)", section_str)
        #     if not res:
        #         return None
        #     section_dict["title"] = res.groups()[0].strip()
        #     res = re.search("\n(.*?)\n?[\*]+ ", section_str)
        #     section_dict["text"] = "" if not res else res.groups()[0].strip()
        #     regx = Regexes.attribute_pair
        #     section_dict["attributes"] = dict(re.findall(regx, section_str))
        #     section_dict["subsections"] = list(
        #         map(str.strip, re.split(regx_subsections, section_str)[1:])
        #     )
        #     return section_dict

        # sections = re.split(regx_items, body)
        # kwarg_dict.update(
        #     {"sections": list(map(parse_section, filter(bool, sections)))}
        # )
        # kwarg_dict.update({"items": re.split(regx_items, sections[0])[1:]})

        with open("/tmp/y.norg", "w") as f:
            # f.write("\n***\n".join(items))
            f.write(norg_str)
        if body:
            with open("/tmp/x.norg", "w") as f:
                f.write(body)

        print(100 * "7")
        n = NorgItems.from_string(body)
        with open("/tmp/w.norg", "w") as f:
            f.write("------")
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

    # @staticmethod
    # def parse_link(s: str) -> Tuple[str, str]:
    #     regx_link = Regexes.link
    #     search = re.search(regx_link, s)
    #     if not search:
    #         return ("", "")
    #     else:
    #         groups = search.groups() if search else []
    #         link = [result for result in groups if str(result).startswith("$/")][0]
    #         loc = groups.index(link)
    #         text = groups[(loc - 1) if (loc % 2) else (loc + 1)]
    #         return (text, link)

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
    def norg_link(*args, **kwargs) -> NorgLink:
        return NorgLink(*args, **kwargs)

    # @staticmethod
    # def split_document(fp: Path) -> List[str]:
    #     regx = Regexes.section_split
    #     with open(fp) as f:
    #         return re.split(regx, f.read())

    # @staticmethod
    # def get_kv(attr_str: str) -> List[List[str]]:
    #     return [re.split(" *: *", s.strip(), 1) for s in re.split("\n\s*", attr_str)]

    # @staticmethod
    # def get_dict_from_path(fp: Path) -> Dict:
    #     doc: Dict[str, Any] = {"header": {}, "sections": {}}
    #     header, *sections = Norg.split_document(fp)
    #     doc.update({"header": NorgHeader.get_list_from_header(header)})
    #     for i, section in enumerate(sections):
    #         doc["sections"].update({str(i + 1), NorgSection.get_dict_from_section(section)})
    #     return doc

    # @staticmethod
    # def make_norg_notes(notes: str) -> str:
    #     notes = wrap_string(notes, width=120, trailing_spaces=0)
    #     return f"* Notes\n\n{notes}\n"

    # @staticmethod
    # def get_norg_entries(norg_str):
    #     regx = Regexes.entry_split_old
    #     return re.split(regx, norg_str.split("* Notes")[0])[1:]


# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/projects/notes_reading_projects/b.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/roadmaps.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/adhoc.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/calendar.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/.norg"))
# n = Norg.from_path(Path("/home/isaac/Learning/planager-data/.norg"))
