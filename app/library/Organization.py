from datetime import datetime, timedelta
import json
from uuid import UUID
from .Room import Room
from .Event import Event
from .User import User


# Exceptions not handled


class Organization:
    def __init__(self, owner: User, name: str, rooms: list[Room] | None = None) -> None:
        self.owner = owner
        self.name = name

        self.rooms = rooms if rooms else []

    def get(self) -> str:
        val = {
            "owner": self.owner.to_dict(),
            "name": self.name,
            "rooms": [i.to_dict() for i in self.rooms],
        }
        return json.dumps(val, indent=4)

    def update(self, **kw) -> None:
        for key, value in kw.items():
            setattr(self, key, value)

    def delete(self):
        pass

    def get_room(self, id: UUID) -> Room | None:
        rooms = list(filter(lambda x: x.id == id, self.rooms))
        return rooms[0] if len(rooms) > 0 else None

    def update_room(self, id, **kw):
        room = self.get_room(id)
        if room:
            room.update(kw)

    def delete_room(self, id: UUID) -> None:
        room = self.get_room(id)
        if room:
            self.rooms.remove(self.get_room(id))

    def reserve(self, event: Event, room_id: UUID) -> bool:
        room = self.get_room(room_id)
        if not room:
            return False

        # Reserve room
        return room.reserve(event)

    #   Assuming rectangle consists of x1,x2,y1,y2 attributes and they correspond to:
    #
    # x1,y1 _____________
    #      |             |
    #      |             |
    #      |_____________| x2,y2

    def findRoom(self, event, rect, start, end):
        availableRooms = []
        for i in self.rooms.values():
            if (
                rect.x1 <= i.x
                and rect.x2 >= i.x
                and rect.y1 <= i.y
                and rect.y2 >= i.y
                and event.capacity >= i.capacity
            ):
                noConflict = False
                # for j in self.reservations[]
