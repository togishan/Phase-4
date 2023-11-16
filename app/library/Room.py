from datetime import datetime, timedelta
import json
from uuid import uuid4
from .Permission import Permission
from .HourMinute import HourMinute
from .Event import Event


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
        self.id = uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.open_time = open_time
        self.close_time = close_time
        self.permissions = permissions

    def get(self) -> str:
        val = self.to_dict()
        return json.dumps(val, indent=4)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "open_time": self.open_time.to_dict(),
            "close_time": self.close_time.to_dict(),
            "permissions": self.permissions,
        }

    def is_available(self, start_time: datetime, end_time: datetime) -> bool:
        # TODO
        return True

    def reserve(self, event: Event):
        # Check if room is available
        if not self.is_available(
            event.start_time, event.start_time + timedelta(minutes=event.duration)
        ):
            return False

        # Check if room has enough capacity
        if self.capacity < event.capacity:
            return False

        # TODO: Reserve room
        return True
