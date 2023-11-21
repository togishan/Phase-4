import json
from uuid import UUID, uuid4
from .Room import Room
from .Event import Event
from ..auth.User import User
from datetime import datetime, timedelta
from .Rectangle import Rectangle


class Organization:
    def __init__(
        self, owner: User, name: str, map: Rectangle, rooms: list[Room] | None = None
    ) -> None:
        self.id = uuid4()
        self.owner = owner
        self.name = name
        self.map = map

        self.rooms = rooms if rooms else []
        self.reserved_events: list[Event] = []

    def get_id(self) -> str:
        return str(self.id)

    def to_dict(self) -> dict:
        return {
            "id": self.get_id(),
            "owner": self.owner.to_dict(),
            "name": self.name,
            "rooms": [i.to_dict() for i in self.rooms],
            "reserved_events": [i.to_dict() for i in self.reserved_events],
            "map": self.map.to_dict(),
        }

    def get(self) -> str:
        val = self.to_dict()
        return json.dumps(val, indent=4)

    def update(self, **kw) -> None:
        for key, value in kw.items():
            setattr(self, key, value)

    def delete(self):
        for each in self.rooms:
            each.delete()

        for each in self.reserved_events:
            each.delete()

        del self

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
            self.rooms.remove(room)
            del room

    def are_two_times_conflicting(
        self,
        start_time1: datetime,
        end_time1: datetime,
        start_time2: datetime,
        end_time2: datetime,
    ) -> bool:
        if start_time1 < start_time2:
            return end_time1 > start_time2
        else:
            return start_time1 < end_time2

    def is_room_available(
        self, room: Room, start_time: datetime, end_time: datetime
    ) -> bool:
        events_in_room = filter(
            lambda x: x.location.id == room.id, self.reserved_events
        )
        
        # Is room open?
        if not (
            (
                (
                    start_time.hour == room.open_time.hour
                    and start_time.minute >= room.open_time.minute
                )
                or (start_time.hour > room.open_time.hour)
            )
            and (
                (
                    end_time.hour == room.close_time.hour
                    and end_time.minute <= room.close_time.minute
                )
                or (end_time.hour < room.close_time.hour)
            )
        ):
            return False

        # Is room available?
        for each in events_in_room:
            
            if each.weekly:
                current_time = each.start_time
                while current_time <= each.weekly or (current_time.year == each.weekly.year and current_time.month == each.weekly.month and current_time.day == each.weekly.day):          
                    if self.are_two_times_conflicting(
                        start_time,
                        end_time,
                        current_time,
                        current_time + timedelta(minutes=each.duration),
                    ):
                        return False
                    current_time += timedelta(days=7)
                    
            else:
                if self.are_two_times_conflicting(
                    start_time,
                    end_time,
                    each.start_time,
                    each.start_time + timedelta(minutes=each.duration),
                ):
                    return False
        
        return True

    def reserve(self, event: Event, room_id: UUID, start_time: datetime) -> bool:
        # Check if room exists
        room = self.get_room(room_id)
        if not room:
            return False

        # Check if user is in a group that can reserve this room
        can_reserve = False
        for each_user_group in room.user_groups:
            if each_user_group in room.user_groups:
                can_reserve = True
                break
        if not can_reserve:
            return False

        # Check if room has enough capacity
        if room.capacity < event.capacity:
            return False

        # Check if room is available
        if event.weekly:
            current_time = start_time           # NOT EFFICIENT 
            while current_time <= event.weekly or (current_time.year == event.weekly.year and current_time.month == event.weekly.month and current_time.day == event.weekly.day):         
                if not self.is_room_available(
                    room, current_time, current_time + timedelta(minutes=event.duration)
                ):
                    return False
                current_time += timedelta(days=7)
        else:
            if not self.is_room_available(
                room, start_time, start_time + timedelta(minutes=event.duration)
            ):
                return False

        # Reserve room
        event.start_time = start_time
        event.location = room
        self.reserved_events.append(event)
        
        return True

    def reassign(self, event: Event, room_id: UUID):
        # Check if event is already assigned
        if (
            not event.location
            or not event.start_time
            or event not in self.reserved_events
        ):
            return False

        # Check if room exists
        room = self.get_room(room_id)
        if not room:
            return False

        # Check if user is in a group that can reserve this room
        can_reserve = False
        for each_user_group in room.user_groups:
            if each_user_group in room.user_groups:
                can_reserve = True
                break
        if not can_reserve:
            return False

        # Check if room has enough capacity
        if room.capacity < event.capacity:
            return False

        # Check if room is available
        if not self.is_room_available(
            room, event.start_time, event.start_time + timedelta(minutes=event.duration)
        ):
            return False

        # Reserve room
        event.location = room
        
        return True
    
   
    def is_inside_rectangle(self, rect: Rectangle, room: Room) -> bool:
        return room.x <= rect.top_right_x and room.y <= rect.top_right_y and room.x >= rect.bottom_left_x and room.y >= rect.bottom_left_y
        
    # find all the rooms in the area with enough capacity to host an event, 
    # then check for the available hours for the room  
    #
    # checking for available hour: begin iteration from start_date opening_time for the room and 
    # iterate until end_date closing hour, iterator will be advanced by expected_duration_minute on each iteration
    #
    # returns the list of tuples (event, Room, startTime) 
    def find_room(
        self, event: Event, rect: Rectangle, start_date: datetime, end_date: datetime, expected_duration_minute: int
    ):
        available_reservations = []
        # rooms in the rectangle with enough capacity to host the event
        available_rooms = filter(
            lambda x: self.is_inside_rectangle(rect, x) and x.capacity >= event.capacity, self.rooms
        )
        # foreach room
        for room in available_rooms:
            
            date = start_date
            # within specified date range
            while date <= end_date:
                closetime = date + timedelta(hours=room.close_time.hour, minutes=room.close_time.minute)
                time = date + timedelta(hours=room.open_time.hour, minutes=room.open_time.minute)
                # for each day between opening and closing hours
                while time <= closetime:
                    if self.is_room_available(room, time, time + timedelta(minutes=event.duration)):
                        available_reservations += [(event, room, time)]
                    time += timedelta(minutes = expected_duration_minute)
                # next day
                date += timedelta(days=1)
        return available_reservations

    def find_schedule(
        self, eventList: list[Event], rect: Rectangle, start_time: datetime, end_time: datetime
    ):
        pass


