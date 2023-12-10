import json
from uuid import uuid4
from .HourMinute import HourMinute
from ..auth.UserGroup import UserGroup
from ..auth.User import User
from enum import Enum


class RoomPermission(Enum):
    WRITE = "WRITE"


class Room:
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        capacity: int,
        open_time: HourMinute,
        close_time: HourMinute,
        permissions: dict[User, set[RoomPermission]] = None,
        user_groups: list[UserGroup] = None,
    ):
        self.id = uuid4()
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.open_time = open_time
        self.close_time = close_time

        self.permissions = permissions if permissions else {}
        self.user_groups = user_groups if user_groups else []

    def get_id(self) -> str:
        return str(self.id)

    def get(self) -> str:
        val = self.to_dict()
        return json.dumps(val, indent=4)

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity,
            "open_time": self.open_time.to_dict(),
            "close_time": self.close_time.to_dict(),
            "user_groups": [UserGroup(i).name for i in self.user_groups],
        }

    def has_permission(self, user: User, permission: RoomPermission) -> bool:
        return permission in self.permissions.get(user, set())
