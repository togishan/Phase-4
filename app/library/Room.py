import json
from datetime import datetime
from .Permission import Permission


class Room:
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        capacity: int,
        working_hours: tuple[datetime],
        permissions: list[Permission],
    ):
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.working_hours = working_hours
        self.permissions = permissions

    def get(self):
        val = {
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "workingHours": self.working_hours,
            "permissions": self.permissions,
        }
        return json.dumps(val, indent=3)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def attach(self, id):
        self.id = id
