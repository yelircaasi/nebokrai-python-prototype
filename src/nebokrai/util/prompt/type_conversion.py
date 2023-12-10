from ..nkdatetime.nktime import NKTime


def convert_time_amount(s: str) -> float:
    r"""
    Designed to accept string inputs of the form \d+ and \d\d?:\d\d and return a float in either
      case.
    """
    s = s.strip()
    if s.replace(".", "", 1).isdigit():
        return float(s)
    if ":" in s:
        nktime = NKTime.from_string(s)
        return float(60 * nktime.hour + nktime.minute)
    raise ValueError(f"Input string {s} cannot be converted to float.")
