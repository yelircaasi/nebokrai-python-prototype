from ...nebokrai import NebokraiEntryPoint


def derive_interactive() -> None:
    print("running 'nebokrai derive'")
    nbkr = NebokraiEntryPoint()
    print("Not yet implemented.")


def derive_dryrun() -> None:
    print("running 'nebokrai derive dryrun'")
    nbkr = NebokraiEntryPoint()
    print("Not yet implemented.")


def derive_dryrun_accept() -> None:
    print("running 'nebokrai derive dryrun-accept'")
    nbkr = NebokraiEntryPoint()
    print("Not yet implemented.")


def derive_plan() -> None:
    print("running 'nebokrai derive plan'")
    nbkr = NebokraiEntryPoint()
    nbkr.derive_plan()
    nbkr.save_plan()


def derive_schedules() -> None:
    print("running 'nebokrai derive schedule'")
    nbkr = NebokraiEntryPoint()
    nbkr.open_plan()
    nbkr.derive_schedules()
    nbkr.save_schedules()
