import pytest

from planager.util.entity_ids import ProjectID, RoadmapID, TaskID


def test_ids() -> None:
    rmid = RoadmapID("rdmp")
    prid = ProjectID("rdmp", "prjct")
    tkid = TaskID("rdmp", "prjct", "tsk")

    prid_from_rmid = rmid.project_id("prjct")
    tkid_from_rmid = rmid.task_id("prjct", "tsk")
    rmid_from_prid = prid.roadmap_id
    tkid_from_prid = prid.task_id("tsk")
    rmid_from_tkid = tkid.roadmap_id
    prid_from_tkid = tkid.project_id

    assert rmid.roadmap == prid.roadmap == tkid.roadmap == "rdmp"
    assert prid.project == tkid.project == "prjct"
    assert tkid.task == "tsk"

    assert rmid == rmid_from_prid
    assert rmid == rmid_from_tkid
    assert prid == prid_from_rmid
    assert prid == prid_from_tkid
    assert tkid == tkid_from_rmid
    assert tkid == tkid_from_prid

    assert str(rmid) == "rdmp"
    assert str(prid) == "rdmp-prjct"
    assert str(tkid) == "rdmp-prjct-tsk"

    assert ProjectID.from_string("rdmp-prjct") == prid
    assert TaskID.from_string("rdmp-prjct-tsk") == tkid

    assert rmid in rmid
    assert rmid in prid
    assert prid in prid
    assert tkid in tkid
    assert prid in rmid
    assert rmid in tkid
    assert tkid in rmid
    assert prid in tkid
    assert tkid in prid

    assert RoadmapID("other") not in rmid
    assert RoadmapID("other") not in prid
    assert RoadmapID("other") not in tkid

    assert ProjectID("other", "prjct") not in rmid
    assert ProjectID("rdmp", "other") in rmid

    assert ProjectID("rdmp", "other") not in prid
    assert ProjectID("other", "prjct") not in prid

    assert ProjectID("rdmp", "other") not in tkid
    assert ProjectID("other", "prjct") not in tkid

    assert TaskID("other", "prjct", "tsk") not in rmid
    assert TaskID("rdmp", "other", "tsk") in rmid
    assert TaskID("rdmp", "prjct", "other") in rmid
    assert TaskID("rdmp", "other", "other") in rmid

    assert TaskID("other", "prjct", "tsk") not in rmid
    assert TaskID("rdmp", "other", "tsk") in rmid
    assert TaskID("rdmp", "prjct", "other") in rmid
    assert TaskID("rdmp", "other", "other") in rmid

    assert TaskID("other", "prjct", "tsk") not in tkid
    assert TaskID("rdmp", "other", "tsk") not in tkid
    assert TaskID("rdmp", "prjct", "other") not in tkid

    with pytest.raises(TypeError) as excinfo:
        "rdmp" in rmid
    assert str(excinfo.value) == (
        "RoadmapID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
        "not type '<class 'str'>' (value: 'rdmp')."
    )

    with pytest.raises(TypeError) as excinfo:
        3 in rmid  # type: ignore
    assert str(excinfo.value) == (
        "RoadmapID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
        f"not type '<class 'int'>' (value: '3')."
    )

    with pytest.raises(TypeError) as excinfo:
        "prjct" in prid
    assert str(excinfo.value) == (
        "ProjectID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
        "not type '<class 'str'>' (value: 'prjct')."
    )

    with pytest.raises(TypeError) as excinfo:
        3 in prid  # type: ignore
    assert str(excinfo.value) == (
        "ProjectID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
        f"not type '<class 'int'>' (value: '3')."
    )

    with pytest.raises(TypeError) as excinfo:
        "tsk" in tkid
    assert str(excinfo.value) == (
        "TaskID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
        "not type '<class 'str'>' (value: 'tsk')."
    )

    with pytest.raises(TypeError) as excinfo:
        3 in tkid  # type: ignore
    assert str(excinfo.value) == (
        "TaskID.__contains__ only supports instances of RoadmapID, ProjectID, or TaskID, "
        f"not type '<class 'int'>' (value: '3')."
    )
