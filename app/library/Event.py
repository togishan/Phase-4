import json
from enum import Enum
from datetime import datetime
from .Permission import Permission
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
        permissions: list[Permission],
        start_time: datetime | None = None,
        location: Room | None = None,
        weekly: datetime | None = None,
    ):
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.permissions = permissions
        self.start_time = start_time
        self.location = location
        self.weekly = weekly

    def get(self):
        val = {
            "title": self.title,
            "description": self.description,
            "category": EventCategory(self.category).name,
            "capacity": self.capacity,
            "duration": self.duration,
            "permissions": self.permissions,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")
            if self.start_time
            else None,
            "location": self.location.get() if self.location else None,
            "weekly": self.weekly,
        }
        return json.dumps(val, indent=4)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def delete(self):
        pass
