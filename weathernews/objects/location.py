from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Location:
    lat: Decimal
    lon: Decimal
    loc: str
    dist: Decimal
    v: str
    s: int
    url: str
