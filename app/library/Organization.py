import json
from enum import Enum

from uuid import UUID, uuid4
from .Room import Room
from .Event import Event
from ..auth.User import User
from datetime import datetime, timedelta
from .Rectangle import Rectangle
from .Room import RoomPermission


class OrganizationPermission(Enum):
    LIST = "LIST"
    ADD = "ADD"
    ACCESS = "ACCESS"
    DELETE = "DELETE"


class Organization:
    def __init__(
        self,
        owner: User,
        name: str,
        map: Rectangle,
        permissions: dict[User, set[OrganizationPermission]] = None,
        rooms: list[Room] | None = None,
    ) -> None:
        self.id = uuid4()
        self.owner = owner
        self.name = name
        self.map = map

        self.permissions = permissions if permissions else {}

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

    def is_owner(self, user: User) -> bool:
        return user.id == self.owner.id

    def has_permission(self, user: User, permission: OrganizationPermission) -> bool:
        return permission in self.permissions.get(user, set())

    def delete_room(self, id: UUID, user: User) -> None:
        room = self.get_room(id)
        if room and (
            self.is_owner(user)
            or (
                self.has_permission(user, OrganizationPermission.DELETE)
                and room.has_permission(user, RoomPermission.WRITE)
            )
        ):
            # Delete events in that room
            events_to_be_deleted = filter(
                lambda e: e.location.id == room.id, self.reserved_events
            )

            for each in events_to_be_deleted:
                self.reserved_events.remove(each)
                each.delete()

            # Delete room
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
                while current_time <= each.weekly or (
                    current_time.year == each.weekly.year
                    and current_time.month == each.weekly.month
                    and current_time.day == each.weekly.day
                ):
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
            current_time = start_time  # NOT EFFICIENT
            while current_time <= event.weekly or (
                current_time.year == event.weekly.year
                and current_time.month == event.weekly.month
                and current_time.day == event.weekly.day
            ):
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
        return (
            room.x <= rect.top_right_x
            and room.y <= rect.top_right_y
            and room.x >= rect.bottom_left_x
            and room.y >= rect.bottom_left_y
        )

    # find all the rooms in the area with enough capacity to host an event,
    # then check for the available hours for the room
    #
    # checking for available hour: begin iteration from start_date opening_time for the room and
    # iterate until end_date closing hour, iterator will be advanced by expected_duration_minute on each iteration
    #
    # returns the list of tuples (event, Room, startTime)
    def find_room(
        self,
        event: Event,
        rect: Rectangle,
        start_date: datetime,
        end_date: datetime,
        expected_duration_minute: int,
    ):
        available_reservations = []
        # rooms in the rectangle with enough capacity to host the event
        available_rooms = filter(
            lambda x: self.is_inside_rectangle(rect, x)
            and x.capacity >= event.capacity,
            self.rooms,
        )
        # foreach room
        for room in available_rooms:
            date = start_date
            # within specified date range
            while date <= end_date:
                closetime = date + timedelta(
                    hours=room.close_time.hour, minutes=room.close_time.minute
                )
                time = date + timedelta(
                    hours=room.open_time.hour, minutes=room.open_time.minute
                )
                # for each day between opening and closing hours
                while time <= closetime:
                    if time + timedelta(
                        minutes=event.duration
                    ) < closetime and self.is_room_available(
                        room, time, time + timedelta(minutes=event.duration)
                    ):
                        available_reservations += [(event, room, time)]
                    time += timedelta(minutes=expected_duration_minute)
                # next day
                date += timedelta(days=1)
        return available_reservations

    #  NOT HANDLING ALL CASES !!!
    #  sort events based on duration, an assignmsent for event with higher duration will be done priorly
    #  foreach event call find_room to find proper assignments for this event
    #  check whether proper assignment is conflicting with other event's assignment
    #  if it conflicts check for other proper assignment for that event else add it to the result_list
    #  if no assignment could be done with that event return []
    def find_schedule(
        self,
        eventList: list[Event],
        rect: Rectangle,
        start_date: datetime,
        end_date: datetime,
        expected_duration_minute: int,
    ):
        # consists of tuples (event, room, start)
        result_list = []
        # consists of lists which consist of tuples (event, room, start)
        available_assignments_for_events = []
        # sort events descending by the duration
        eventList.sort(reverse=True)
        # foreach event find all assignable hour, room pairs
        # if no assignable hour is found for the event then, the schedule can not be built so return []
        # else add tuple list coming from the function find_room to the available_assignments_for_events list
        for event in eventList:
            temp = self.find_room(
                event, rect, start_date, end_date, expected_duration_minute
            )
            if temp == []:
                return []
            available_assignments_for_events += [temp]

        for assignments in available_assignments_for_events:
            assignment_scheduled = False
            for assignment in assignments:
                # check if the assignment conflicts with previously added ones to the result_list
                conflicts = False
                for i in result_list:
                    if i[1] == assignment[1] and self.are_two_times_conflicting(
                        i[2],
                        i[2] + timedelta(minutes=i[0].duration),
                        assignment[2],
                        assignment[2] + timedelta(minutes=assignment[0].duration),
                    ):
                        conflicts = True
                        break
                if not conflicts:
                    result_list += [assignment]
                    assignment_scheduled = True
                    break
            if not assignment_scheduled:
                return []
        return result_list

    def query(self, rect: Rectangle, title: str, category: str, room: Room = None):
        return_list = []
        # do everything with room
        if rect == None:
            for assignment in self.reserved_events:
                if (
                    assignment.title == title
                    and assignment.category.value == category
                    and assignment.location == room
                ):
                    return_list += [
                        (assignment, assignment.location, assignment.start_time)
                    ]

        # do everything with rect
        else:
            for assignment in self.reserved_events:
                if (
                    assignment.title == title
                    and assignment.category.value == category
                    and self.is_inside_rectangle(rect, assignment.location)
                ):
                    return_list += [
                        (assignment, assignment.location, assignment.start_time)
                    ]
        return return_list
