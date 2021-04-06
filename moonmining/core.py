import datetime as dt
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import List

from . import helpers


@dataclass
class CalculatedExtraction:
    """An extraction calculated from moon mining notifications."""

    class Status(IntEnum):
        STARTED = auto()
        CANCELED = auto()
        READY = auto()
        COMPLETED = auto()
        UNDEFINED = auto()

    refinery_id: int
    ready_time: dt.datetime

    status: str
    started_by: int
    auto_time: dt.datetime = None
    canceled_at: dt.datetime = None
    canceled_by: int = None
    finished_at: dt.datetime = None
    fractured_at: dt.datetime = None
    fractured_by: int = None
    products: List["CalculatedExtractionProduct"] = None

    def __post_init__(self):
        self.ready_time = helpers.round_seconds(self.ready_time)


@dataclass
class CalculatedExtractionProduct:
    """Product of an extraction calculated from moon mining notifications."""

    ore_type_id: int
    volume: float

    @classmethod
    def create_list_from_dict(cls, ores: dict):
        return [cls(ore_type_id, volume) for ore_type_id, volume in ores.items()]
