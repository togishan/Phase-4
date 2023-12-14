from .operation import Operation, OperationType
from .operation_response import OperationResponse
import bcrypt


def handle_operation(
    operation: Operation,
) -> OperationResponse:
    if operation.type == OperationType.REGISTER:
        return handle_register_operation(operation)
    elif operation.type == OperationType.LOGIN:
        return handle_login_operation(operation)
    elif operation.type == OperationType.LOGOUT:
        return handle_logout_operation(operation)
    elif operation.type == OperationType.CREATE_ORGANIZATION:
        return handle_create_organization_operation(operation)
    elif operation.type == OperationType.CHANGE_USER_PERMISSON_FOR_ORGANIZATION:
        return handle_change_user_permission_for_organization_operation(operation)
    elif operation.type == OperationType.QUERY_ORGANIZATION:
        return handle_query_organization_operation(operation)
    elif operation.type == OperationType.CREATE_ROOM:
        return handle_create_room_operation(operation)
    elif operation.type == OperationType.CHANGE_USER_PERMISSON_FOR_ROOM:
        return handle_change_user_permission_for_room_operation(operation)
    elif operation.type == OperationType.ADD_ROOM_TO_ORGANIZATION:
        return handle_add_room_to_organization_operation(operation)
    elif operation.type == OperationType.LIST_ROOMS_OF_ORGANIZATION:
        return handle_list_rooms_of_organization_operation(operation)
    elif operation.type == OperationType.DELETE_ROOM_FROM_ORGANIZATION:
        return handle_delete_room_from_organization_operation(operation)
    elif operation.type == OperationType.DELETE_RESERVATION_OF_ROOM:
        return handle_delete_reservation_of_room_operation(operation)
    elif operation.type == OperationType.ACCESS_ROOM:
        return handle_access_room_operation(operation)
    elif operation.type == OperationType.FIND_ROOM_OF_ORGANIZATION_FOR_EVENT:
        return handle_find_room_of_organization_for_event_operation(operation)
    elif operation.type == OperationType.FIND_ROOM_SCHEDULE_OF_ORGANIZATION_FOR_EVENTS:
        return handle_find_room_schedule_of_organization_for_events_operation(operation)
    elif operation.type == OperationType.CREATE_EVENT:
        return handle_create_event_operation(operation)
    elif operation.type == OperationType.CHANGE_USER_PERMISSON_FOR_EVENT:
        return handle_change_user_permission_for_event_operation(operation)
    elif operation.type == OperationType.RESERVE_ROOM_FOR_EVENT:
        return handle_reserve_room_for_event_operation(operation)
    elif operation.type == OperationType.RERESERVE_ROOM_FOR_EVENT:
        return handle_rereserve_room_for_event_operation(operation)
    elif operation.type == OperationType.LIST_EVENTS_OF_ROOM:
        return handle_list_events_of_room_operation(operation)
    elif operation.type == OperationType.ADD_QUERY:
        return handle_add_query_operation(operation)
    elif operation.type == OperationType.DEL_QUERY:
        return handle_del_query_operation(operation)
    elif operation.type == OperationType.ROOM_VIEW:
        return handle_room_view_operation(operation)
    elif operation.type == OperationType.DAY_VIEW:
        return handle_day_view_operation(operation)


def handle_register_operation(operation: Operation) -> OperationResponse:
    try:
        from ..models import User

        hashed_password = bcrypt.hashpw(
            operation.args["password"].encode("utf-8"), bcrypt.gensalt()
        )

        user: User = User.create(
            username=operation.args["username"],
            password=hashed_password,
            name=operation.args["name"],
        )

        return OperationResponse(
            status=True,
            result={
                "user": user.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_login_operation(operation: Operation) -> OperationResponse:
    try:
        from ..models import User
        from ..dependency_manager import DependencyManager

        user: User = User.get(User.username == operation.args["username"])

        if not bcrypt.checkpw(
            operation.args["password"].encode("utf-8"), user.password.encode("utf-8")
        ):
            return OperationResponse(
                status=False, result={"message": "Invalid password"}
            )

        DependencyManager.register(User, user)

        return OperationResponse(
            status=True,
            result={
                "user": user.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_logout_operation(operation: Operation) -> OperationResponse:
    from ..models import User
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        DependencyManager.unregister(User)
        return OperationResponse(
            status=True,
            result={},
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_create_organization_operation(operation: Operation) -> OperationResponse:
    from ..models import Organization, User
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        organization: Organization = Organization.create(
            name=operation.args["name"], owner=user
        )

        return OperationResponse(
            status=True,
            result={
                "organization": organization.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_create_room_operation(operation: Operation) -> OperationResponse:
    from ..models import Room, User
    from ..dependency_manager import DependencyManager

    import re

    def is_valid_time_of_day_format(input_string: str) -> bool:
        pattern = re.compile(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
        return bool(pattern.match(input_string))

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        if not is_valid_time_of_day_format(operation.args["open_time"]):
            return OperationResponse(
                status=False, result={"message": "Invalid open time format"}
            )

        if not is_valid_time_of_day_format(operation.args["close_time"]):
            return OperationResponse(
                status=False, result={"message": "Invalid close time format"}
            )

        room: Room = Room.create(
            name=operation.args["name"],
            owner=user,
            x=operation.args["x"],
            y=operation.args["y"],
            capacity=operation.args["capacity"],
            open_time=operation.args["open_time"],
            close_time=operation.args["close_time"],
        )

        return OperationResponse(
            status=True,
            result={
                "room": room.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_add_room_to_organization_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import (
        Organization,
        Room,
        User,
        RoomInOrganization,
        UserPermissionForOrganization,
    )
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        organization: Organization = Organization.get(
            Organization.id == operation.args["organization_id"]
        )

        if organization.owner != user:
            try:
                user_permission_for_organization: UserPermissionForOrganization = (
                    UserPermissionForOrganization.get(
                        (UserPermissionForOrganization.user_id == user.id)
                        & (UserPermissionForOrganization.organization == organization)
                        & (UserPermissionForOrganization.permission == "ADD")
                    )
                )
            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={"message": "User does not have permission to add room"},
                )

        room: Room = Room.get(Room.id == operation.args["room_id"])

        room_in_organization = RoomInOrganization.create(
            room=room,
            organization=organization,
        )

        return OperationResponse(
            status=True,
            result={
                "room_in_organization": room_in_organization.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_change_user_permission_for_organization_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import Organization, User, UserPermissionForOrganization
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        organization: Organization = Organization.get(
            Organization.id == operation.args["organization_id"]
        )

        if organization.owner != user:
            return OperationResponse(
                status=False,
                result={"message": "User is not the owner of the organization"},
            )

        user_id = operation.args["user_id"]
        permissions = operation.args["permissions"]

        UserPermissionForOrganization.delete().where(
            (UserPermissionForOrganization.user_id == user_id)
            & (UserPermissionForOrganization.organization == organization)
        ).execute()

        for permission in permissions:
            UserPermissionForOrganization.create(
                user_id=user_id,
                organization=organization,
                permission=permission,
            )

        return OperationResponse(
            status=True,
            result={},
        )

    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_change_user_permission_for_room_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import Room, User, UserPermissionForRoom
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        room: Room = Room.get(Room.id == operation.args["room_id"])

        if room.owner != user:
            return OperationResponse(
                status=False,
                result={"message": "User is not the owner of the room"},
            )

        user_id = operation.args["user_id"]
        permissions = operation.args["permissions"]

        UserPermissionForRoom.delete().where(
            (UserPermissionForRoom.user_id == user_id)
            & (UserPermissionForRoom.room == room)
        ).execute()

        for permission in permissions:
            UserPermissionForRoom.create(
                user_id=user_id,
                room=room,
                permission=permission,
            )

        return OperationResponse(
            status=True,
            result={},
        )

    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_create_event_operation(operation: Operation) -> OperationResponse:
    from ..models import Event, User
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        event: Event = Event.create(
            title=operation.args["title"],
            description=operation.args["description"],
            owner=user,
            category=operation.args["category"],
            capacity=operation.args["capacity"],
            duration=operation.args["duration"],
            weekly=operation.args["weekly"],
        )

        return OperationResponse(
            status=True,
            result={
                "event": event.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_change_user_permission_for_event_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import Event, User, UserPermissionForEvent
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        event: Event = Event.get(Event.id == operation.args["event_id"])

        if event.owner != user:
            return OperationResponse(
                status=False,
                result={"message": "User is not the owner of the event"},
            )

        user_id = operation.args["user_id"]
        permissions = operation.args["permissions"]

        UserPermissionForEvent.delete().where(
            (UserPermissionForEvent.user_id == user_id)
            & (UserPermissionForEvent.event == event)
        ).execute()

        for permission in permissions:
            UserPermissionForEvent.create(
                user_id=user_id,
                event=event,
                permission=permission,
            )

        return OperationResponse(
            status=True,
            result={},
        )

    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_list_rooms_of_organization_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import (
        Organization,
        RoomInOrganization,
        User,
        UserPermissionForOrganization,
    )
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        organization: Organization = Organization.get(
            Organization.id == operation.args["organization_id"]
        )

        if organization.owner != user:
            try:
                user_permission_for_organization: UserPermissionForOrganization = (
                    UserPermissionForOrganization.get(
                        (UserPermissionForOrganization.user_id == user.id)
                        & (UserPermissionForOrganization.organization == organization)
                        & (UserPermissionForOrganization.permission == "LIST")
                    )
                )
            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={"message": "User does not have permission to list rooms"},
                )

        RoomInOrganization.select().where(
            RoomInOrganization.organization == organization
        ).execute()

        return OperationResponse(
            status=True,
            result={},
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_delete_room_from_organization_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import (
        Organization,
        RoomInOrganization,
        User,
        UserPermissionForOrganization,
        UserPermissionForRoom,
        Event,
    )
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        organization: Organization = Organization.get(
            Organization.id == operation.args["organization_id"]
        )

        if organization.owner != user:
            try:
                user_permission_for_organization: UserPermissionForOrganization = (
                    UserPermissionForOrganization.get(
                        (UserPermissionForOrganization.user_id == user.id)
                        & (UserPermissionForOrganization.organization == organization)
                        & (UserPermissionForOrganization.permission == "DELETE")
                    )
                )

                user_permission_for_room: UserPermissionForRoom = (
                    UserPermissionForRoom.get(
                        (UserPermissionForRoom.user_id == user.id)
                        & (UserPermissionForRoom.room == operation.args["room_id"])
                        & (UserPermissionForRoom.permission == "DELETE")
                    )
                )
            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={"message": "User does not have permission to delete rooms"},
                )

        Event.delete().where(Event.location == operation.args["room_id"]).execute()

        RoomInOrganization.delete().where(
            RoomInOrganization.organization
            == organization & RoomInOrganization.room
            == operation.args["room_id"],
        ).execute()

        return OperationResponse(
            status=True,
            result={},
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_list_events_of_room_operation(operation: Operation) -> OperationResponse:
    from ..models import (
        Event,
        Room,
        User,
        UserPermissionForRoom,
    )
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        room: Room = Room.get(Room.id == operation.args["room_id"])

        if room.owner != user:
            try:
                user_permission_for_room: UserPermissionForRoom = (
                    UserPermissionForRoom.get(
                        (UserPermissionForRoom.user_id == user.id)
                        & (UserPermissionForRoom.room == room)
                        & (UserPermissionForRoom.permission == "LIST")
                    )
                )
            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={"message": "User does not have permission to list events"},
                )

        events = Event.select().where(Event.location == room)

        return OperationResponse(
            status=True,
            result={
                "events": [event.to_dict() for event in events],
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_reserve_room_for_event_operation(operation: Operation) -> OperationResponse:
    from ..models import (
        Event,
        Room,
        User,
        UserPermissionForRoom,
    )
    from ..dependency_manager import DependencyManager
    from datetime import datetime, timedelta
    from .utils import is_room_available

    try:
        user: User = DependencyManager.get(User)

        room: Room = Room.get(Room.id == operation.args["room_id"])

        event: Event = Event.get(Event.id == operation.args["event_id"])

        if room.owner != user:
            try:
                user_permission_for_room: UserPermissionForRoom = (
                    UserPermissionForRoom.get(
                        (UserPermissionForRoom.user_id == user.id)
                        & (UserPermissionForRoom.room == room)
                        & (
                            (UserPermissionForRoom.permission == "RESERVE")
                            | (UserPermissionForRoom.permission == "PERRESERVE")
                            if event.weekly is None
                            else (UserPermissionForRoom.permission == "PERRESERVE")
                        )
                    )
                )
            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={
                        "message": "User does not have permission to reserve events"
                    },
                )

        if not is_room_available(
            room.id,
            datetime.fromisoformat(operation.args["start_time"]),
            datetime.fromisoformat(operation.args["start_time"])
            + timedelta(minutes=event.duration),
        ):
            return OperationResponse(
                status=False,
                result={"message": "Room is not available for this event"},
            )

        event.location = room
        event.start_time = datetime.fromisoformat(operation.args["start_time"])
        event.save()

        return OperationResponse(
            status=True,
            result={
                "event": event.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_delete_reservation_of_room_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import (
        Event,
        Room,
        User,
        UserPermissionForRoom,
        UserPermissionForEvent,
    )
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        event: Event = Event.get(Event.id == operation.args["event_id"])

        room: Room = event.location

        if room.owner != user:
            try:
                user_permission_for_room: UserPermissionForRoom = (
                    UserPermissionForRoom.get(
                        (UserPermissionForRoom.user_id == user.id)
                        & (UserPermissionForRoom.room == room)
                        & (UserPermissionForRoom.permission == "DELETE")
                    )
                )

                user_permission_for_event: UserPermissionForEvent = (
                    UserPermissionForEvent.get(
                        (UserPermissionForEvent.user_id == user.id)
                        & (UserPermissionForEvent.event == event)
                        & (UserPermissionForEvent.permission == "WRITE")
                    )
                )

            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={
                        "message": "User does not have permission to delete events"
                    },
                )

        event.location = None
        event.start_time = None
        event.save()

        return OperationResponse(
            status=True,
            result={
                "event": event.to_dict(),
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_access_room_operation(operation: Operation) -> OperationResponse:
    from ..models import Room, User, UserPermissionForRoom, Event
    from ..dependency_manager import DependencyManager

    try:
        user: User = DependencyManager.get(User)

        room: Room = Room.get(Room.id == operation.args["room_id"])

        if room.owner != user:
            try:
                user_permission_for_room: UserPermissionForRoom = (
                    UserPermissionForRoom.get(
                        (UserPermissionForRoom.user_id == user.id)
                        & (UserPermissionForRoom.room == room)
                        & (UserPermissionForRoom.permission == "ACCESS")
                    )
                )
            except Exception as e:
                return OperationResponse(
                    status=False,
                    result={"message": "User does not have permission to access room"},
                )

        events = Event.select().where(Event.location == room).execute()

        return OperationResponse(
            status=True,
            result={
                "room": room.to_dict(),
                "events": [event.to_dict() for event in events],
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_query_organization_operation(operation: Operation) -> OperationResponse:
    from .utils import is_inside_rectangle
    from ..models import Room

    try:
        top_right_x = operation.args["top_right_x"]
        top_right_y = operation.args["top_right_y"]
        bottom_left_x = operation.args["bottom_left_x"]
        bottom_left_y = operation.args["bottom_left_y"]

        room_id = operation.args["room_id"]
        title = operation.args["title"]
        category = operation.args["category"]

        room = Room.get(Room.id == room_id)
        events_of_room = room.events

        #  def query(self, rect: Rectangle, title: str, category: str, room: Room = None):
        return_list = []
        # do everything with room
        if room_id:
            for assignment in events_of_room:
                if (
                    assignment.title == title
                    and assignment.category == category
                    and assignment.location_id == room_id
                ):
                    return_list += [
                        (assignment, assignment.location, assignment.start_time)
                    ]

        # do everything with rect
        else:
            for assignment in events_of_room:
                if (
                    assignment.title == title
                    and assignment.category.value == category
                    and is_inside_rectangle(
                        top_right_x=top_right_x,
                        top_right_y=top_right_y,
                        bottom_left_x=bottom_left_x,
                        bottom_left_y=bottom_left_y,
                        x=assignment.location.x,
                        y=assignment.location.y,
                    )
                ):
                    return_list += [
                        (assignment, assignment.location, assignment.start_time)
                    ]
        return OperationResponse(
            status=True,
            result={
                "assignments": return_list,
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_find_room_of_organization_for_event_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import (
        Room,
        Event,
    )

    from datetime import datetime, timedelta

    from .utils import is_inside_rectangle, is_room_available

    try:
        # find all the rooms in the area with enough capacity to host an event,
        # then check for the available hours for the room
        #
        # checking for available hour: begin iteration from start_date opening_time for the room and
        # iterate until end_date closing hour, iterator will be advanced by expected_duration_minute on each iteration
        #
        # returns the list of tuples (event, Room, startTime)

        expected_duration_minute = 30

        event = Event.get(Event.id == operation.args["event_id"])

        available_reservations = []
        # rooms in the rectangle with enough capacity to host the event
        available_rooms = Room.select().where(
            Room.capacity
            >= event.capacity
            & is_inside_rectangle(
                operation.args["top_right_x"],
                operation.args["top_right_y"],
                operation.args["bottom_left_x"],
                operation.args["bottom_left_y"],
                Room.x,
                Room.y,
            )
        )

        # foreach room
        for room in available_rooms:
            date = datetime.fromisoformat(operation.args["start_time"])
            room_open_time_hour = int(room.open_time[:2])
            room_open_time_minute = int(room.open_time[3:])

            room_close_time_hour = int(room.close_time[:2])
            room_close_time_minute = int(room.close_time[3:])
            # within specified date range
            while date <= datetime.fromisoformat(operation.args["end_time"]):
                closetime = date + timedelta(
                    hours=room_close_time_hour, minutes=room_close_time_minute
                )
                time = date + timedelta(
                    hours=room_open_time_hour, minutes=room_open_time_minute
                )
                # for each day between opening and closing hours
                while time <= closetime:
                    if time + timedelta(
                        minutes=event.duration
                    ) < closetime and is_room_available(
                        room.id, time, time + timedelta(minutes=event.duration)
                    ):
                        available_reservations += [(event, room, time)]
                    time += timedelta(minutes=expected_duration_minute)
                # next day
                date += timedelta(days=1)
        return OperationResponse(
            status=True,
            result={
                "available_reservations": available_reservations,
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_find_room_schedule_of_organization_for_events_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import (
        Event,
    )

    from datetime import datetime, timedelta
    from .utils import are_two_times_conflicting

    try:
        event_ids = operation.args["event_ids"]
        event_list = (
            Event.select()
            .where(Event.id.in_(event_ids))
            .order_by(Event.duration.desc())
        )

        # consists of tuples (event, room, start)
        result_list = []
        # consists of lists which consist of tuples (event, room, start)
        available_assignments_for_events = []
        # sort events descending by the duration

        # foreach event find all assignable hour, room pairs
        # if no assignable hour is found for the event then, the schedule can not be built so return []
        # else add tuple list coming from the function find_room to the available_assignments_for_events list
        for event in event_list:
            find_room_operation = Operation(
                type=OperationType.FIND_ROOM_OF_ORGANIZATION_FOR_EVENT,
                args={
                    "event_id": event.id,
                    "top_right_x": operation.args["top_right_x"],
                    "top_right_y": operation.args["top_right_y"],
                    "bottom_left_x": operation.args["bottom_left_x"],
                    "bottom_left_y": operation.args["bottom_left_y"],
                    "start_time": operation.args["start_time"],
                    "end_time": operation.args["end_time"],
                },
            )
            find_room_operation_response = (
                handle_find_room_of_organization_for_event_operation(
                    find_room_operation
                ),
            )

            available_reservations = find_room_operation_response.result[
                "available_reservations"
            ]

            if available_reservations.length == 0:
                return OperationResponse(
                    status=None,
                    result={
                        "message": "No schedule can be built for the given events",
                    },
                )

            available_assignments_for_events += [available_reservations]

        for assignments in available_assignments_for_events:
            assignment_scheduled = False
            for assignment in assignments:
                # check if the assignment conflicts with previously added ones to the result_list
                conflicts = False
                for i in result_list:
                    i_room_id = i[1].id
                    assignment_room_id = assignment[1].id

                    if i_room_id == assignment_room_id and are_two_times_conflicting(
                        datetime.fromisoformat(i[2]),
                        datetime.fromisoformat(i[2]) + timedelta(minutes=i[0].duration),
                        datetime.fromisoformat(assignment[2]),
                        datetime.fromisoformat(assignment[2])
                        + timedelta(minutes=assignment[0].duration),
                    ):
                        conflicts = True
                        break
                if not conflicts:
                    result_list += [assignment]
                    assignment_scheduled = True
                    break
            if not assignment_scheduled:
                return OperationResponse(
                    status=None,
                    result={
                        "message": "No schedule can be built for the given events",
                    },
                )

        return OperationResponse(
            status=True,
            result={
                "schedule": result_list,
            },
        )
    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_rereserve_room_for_event_operation(
    operation: Operation,
) -> OperationResponse:
    from ..models import Event
    from .utils import is_room_available
    from datetime import timedelta

    try:
        event_id = operation.args["event_id"]
        room_id = operation.args["room_id"]

        event = Event.get(Event.id == event_id)

        if is_room_available(
            room_id,
            event.start_time,
            event.start_time + timedelta(minutes=event.duration),
        ):
            event.location_id = room_id
            event.save()
            return OperationResponse(
                status=True,
                result={
                    "event": event.to_dict(),
                },
            )

        return OperationResponse(
            status=False,
            result={
                "message": "Room is not available for this event",
            },
        )

    except Exception as e:
        return OperationResponse(status=False, result={"message": str(e)})


def handle_add_query_operation(operation: Operation) -> OperationResponse:
    # TODO : Implement
    return OperationResponse(status=False, result={"message": "Not implemented"})


def handle_del_query_operation(operation: Operation) -> OperationResponse:
    # TODO : Implement
    return OperationResponse(status=False, result={"message": "Not implemented"})


def handle_room_view_operation(operation: Operation) -> OperationResponse:
    # TODO : Implement
    return OperationResponse(status=False, result={"message": "Not implemented"})


def handle_day_view_operation(operation: Operation) -> OperationResponse:
    # TODO : Implement
    return OperationResponse(status=False, result={"message": "Not implemented"})
