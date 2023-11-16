import json
from enum import Enum
from .Permission import Permission


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
        weekly: bool,
        permissions: list[Permission],
    ):
        self.title = title
        self.description = description
        self.category = category
        self.capacity = capacity
        self.duration = duration
        self.weekly = weekly
        self.permissions = permissions

    def get(self):
        val = {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "capacity": self.capacity,
            "duration": self.duration,
            "weekly": self.weekly,
            "permissions": self.permissions,
        }
        return json.dumps(val, indent=3)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def delete(self):
        pass
