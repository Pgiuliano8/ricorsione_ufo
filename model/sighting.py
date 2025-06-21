from dataclasses import dataclass
from datetime import datetime as dtime
import math


@dataclass
class Sighting:
    id: int
    datetime: dtime
    city: str
    state: str
    country: str
    shape: str
    duration: int
    duration_hm: str
    comments: str
    date_posted: dtime
    latitude: float
    longitude:float

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)