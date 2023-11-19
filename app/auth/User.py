from uuid import uuid4
import json
from .UserGroup import UserGroup


class User:
    def __init__(self, name: str, user_groups: list[UserGroup]) -> None:
        self.id = uuid4()
        self.name = name
        self.user_groups = user_groups

    def to_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "name": self.name,
            "user_groups": [UserGroup(i).name for i in self.user_groups],
        }

    def get_id(self) -> str:
        return str(self.id)

    def get(self) -> str:
        val = self.to_dict()
        return json.dumps(val, indent=4)
