def tabularize(s, width, pad: int = 0):
    padding = pad * " "
    return f"┃ {padding}{str(s): <{width - 4 - pad}} ┃"
