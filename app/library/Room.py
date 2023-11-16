import json
from datetime import datetime
from .Permission import Permission
from .HourMinute import HourMinute


class Room:
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        capacity: int,
        open_time: HourMinute,
        close_time: HourMinute,
        permissions: list[Permission],
    ):
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.open_time = open_time
        self.close_time = close_time
        self.permissions = permissions

    def get(self):
        val = {
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "open_time": self.open_time.get(),
            "close_time": self.close_time.get(),
            "permissions": self.permissions,
        }
        return json.dumps(val, indent=4)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def attach(self, id):
        self.id = id
