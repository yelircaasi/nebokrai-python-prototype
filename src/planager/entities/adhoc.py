""" EXAMPLE DOCUMENT:
@document.meta
title: Schedule for 2023-05-27
authors: [yelircaasi]
categories: 
version: 0.1
@end

.toc

* Items

** Pay the bill to ZDF
   - due: 2023-06-14-18:00
   - duration: 10
   - priority: 100

** Get the system setup
   - start: none
   - due: 2023-06-15
   - priority: 70

"""

from pathlib import Path
from typing import Any, Union

#from planager.config import config
from planager.utils.datetime_extensions import now
from planager.utils.data.norg.norg_utils import norg_utils as norg


class AdHoc:
    def __init__(self, title: str) -> None:
        self.title = title
        #self.author = config.author

    def __getitem__(self, __name: str) -> Any:
        schedule = ...
        return schedule
    
    def __setitem__(self, __name: str, __value: Any) -> None:
        ...

    def __getattr__(self, __name: str) -> Any:
        schedule = ...
        return schedule
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        ...
    
    @classmethod
    def from_norg_workspace(cls, workspace_root: Path) -> "AdHoc":
        adhoc = cls()
        return adhoc
    
    @classmethod
    def from_norg(cls, fp_or_str: Union[Path, str]) -> "AdHoc":
        ...

    @classmethod
    def from_json(cls, fp_or_str: Union[Path, str]) -> "AdHoc":
        ...

    @classmethod
    def from_html(cls, fp_or_str: Union[Path, str]) -> "AdHoc":
        ...

    def to_norg(self, fp: Path) -> None:
        with open(fp, 'w') as f:
            f.write(self.to_norg_str())

    def to_json(self, fp: Path) -> None:
        with open(fp, 'w') as f:
            f.write(self.to_json_str())

    def to_html(self, fp: Path) -> None:
        with open(fp, 'w') as f:
            f.write(self.to_html_str())

    def to_norg_str(self) -> str:
        header = norg.make_header(
            title=self.title,
            #author=self.author,
            updated=now(),
        )



    def to_json_str(self) -> str:
        ...

    def to_html_str(self) -> str:
        ...