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
        return handle_change_permission_for_organization_operation(operation)
    elif operation.type == OperationType.CREATE_ROOM:
        return handle_create_room_operation(operation)
    elif operation.type == OperationType.ADD_ROOM_TO_ORGANIZATION:
        return handle_add_room_to_organization_operation(operation)


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
    from ..models import Organization, Room, User, RoomInOrganization
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


def handle_change_permission_for_organization_operation(
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
