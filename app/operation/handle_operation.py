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
    elif operation.type == OperationType.CREATE_EVENT:
        return handle_create_event_operation(operation)
    elif operation.type == OperationType.CHANGE_USER_PERMISSON_FOR_EVENT:
        return handle_change_user_permission_for_event_operation(operation)
    elif operation.type == OperationType.RESERVE_ROOM_FOR_EVENT:
        return handle_reserve_room_for_event_operation(operation)
    elif operation.type == OperationType.LIST_EVENTS_OF_ROOM:
        return handle_list_events_of_room_operation(operation)


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

    try:
        user: User = DependencyManager.get(User)

        if user is None:
            return OperationResponse(
                status=False, result={"message": "User not logged in"}
            )

        room: Room = Room.create(
            name=operation.args["name"],
            owner=user,
            x=operation.args["x"],
            y=operation.args["y"],
            capacity=operation.args["capacity"],
            # TODO : Validate time format
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

        # TODO : Also remove events of the room

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

        events = Event.select().where(Event.location == room).execute()

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
    from datetime import datetime

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

        # TODO : Check if room is available
        # TODO : For weekly events, check if room is available for all events

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
