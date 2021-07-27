from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class Comment:
    short: str
    detail: str


@dataclass
class Precip:
    amt: Optional[Decimal] = 0
    pt: Optional[int] = None
    hour: Optional[str] = None


@dataclass
class Daily:
    datetime: datetime
    icon: str
    short: str
    detail: str
    high: int
    low: int
    precip: List[Precip]


@dataclass
class Dailies:
    data: List[Daily]
    comment: Comment


@dataclass
class Hourly:
    datetime: datetime
    icon: str
    short: str
    detail: str
    precip: Precip
    temp: int
    wind_speed: int
    wind_dir: str


@dataclass
class Report:
    loc: str
    lat: Decimal
    lon: Decimal
    url: str
    metric: bool
    hourly: List[Hourly]
    today: Daily
    tomorrow: Daily
    twoday: List[Dailies]
    tenday: List[Dailies]

    def __post_init__(self):
        self.datetime = datetime.now().timestamp()
        self.t = self.today
        self.tom = self.tomorrow
