import re
import json
from datetime import datetime, timedelta

from weathernews.error import ParserError


def json_or_jquery(response):
    """Parse weird jQuery response from Weathernews and
    regular json responses.

    Expected response:
        'jQuery30002766016168183938_1627346373717(<valid json>);'
    """

    regex = r"jQuery\d*_\d*\((.*)\);"
    r = re.search(regex, response)

    if r:
        return json.loads(r.group())

    return json.loads(response)


def get_number(text):
    """Get positive number from text."""

    r = re.search(r"\d{1,3}", text)
    if not r:
        raise ParserError(
            "Unable to find number from string \'{}\'".format(text),
            None, None
        )

    return int(r.group())


def get_temp(text) -> int:
    """
    Parse pretty temperature text to int.

    Expected text:
        '23℉'
        '24℃'
        '25°F'
        '26°C'
    """

    regex = r"-?\d{1,3}[^°FC℉℃]"

    r = re.search(regex, text)
    if r:
        return r.group()

    raise ParserError(
        "Unable to find temperature value from string \'{}\'".format(text),
        None, None
    )


def get_datetime(date: str, hour: str = "", offset: int = 0) -> datetime:
    """Parse pretty date and time text to datetime.

    Expected date:
        '7月14日（水）'
        '16\n(金)'

    Expected hour:
        '23:00'
    """

    # Japan is UTC+9
    jp_dt = datetime.utcnow() + timedelta(seconds=60*60*9)

    rd = [int(n) for n in re.findall(r"\d{1,2}", date)]
    rm = [int(n) for n in re.findall(r"\d{1,2}", hour)]

    date_m = rd[0] if len(rd) == 2 else jp_dt.month
    date_d = rd[1] if len(rd) == 2 else rd[0]

    time_h = rm[0] if len(rm) == 2 else 0
    time_m = rm[1] if len(rm) == 2 else 0

    jp_dt = jp_dt.replace(
        month=date_m,
        day=date_d,
        hour=time_h,
        minute=time_m,
        second=0,
        microsecond=0
    )

    if offset > 0:
        jp_dt = jp_dt + timedelta(days=offset)

    return jp_dt
