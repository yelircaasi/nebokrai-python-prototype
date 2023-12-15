from ...nebokrai import NebokraiEntryPoint


def declaration_interactive() -> None:
    print("running 'nebokrai declaration'")


def declaration_add() -> None:
    print("running 'nebokrai declaration add'")


def declaration_remove() -> None:
    print("running 'nebokrai declaration remove'")


def declaration_edit() -> None:
    print("Editing nebokrai declaration.")
    nbkr = NebokraiEntryPoint()
    nbkr.edit_declaration_interactive()


def declaration_search() -> None:
    print("running 'nebokrai declaration search'")


def declaration_export() -> None:
    print("running 'nebokrai declaration export'")
