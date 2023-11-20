import json
from enum import Enum
from uuid import uuid4
from datetime import datetime
from .Room import Room


class EventCategory(Enum):
    MEETING = "MEETING"
    LECTURE = "LECTURE"
    CONCERT = "CONCERT"
    SEMINAR = "SEMINAR"
    STUDY = "STUDY"


class Event:
    def __init__(
        self,
        title: str,
        description: str,
        category: EventCategory,
        capacity: int,
        duration: int,
        start_time: datetime | None = None,
        location: Room | None = None,
        weekly: datetime | None = None,
    ):
        self.id = uuid4()
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.start_time = start_time
        self.location = location
        self.weekly = weekly

    def get_id(self) -> str:
        return str(self.id)

    def to_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "title": self.title,
            "description": self.description,
            "category": EventCategory(self.category).name,
            "capacity": self.capacity,
            "duration": self.duration,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")
            if self.start_time
            else None,
            "location": self.location.to_dict() if self.location else None,
            "weekly": self.weekly.strftime("%Y-%m-%d") if self.weekly else None,
        }

    def get(self):
        val = self.to_dict()
        return json.dumps(val, indent=4)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def delete(self):
        del self
