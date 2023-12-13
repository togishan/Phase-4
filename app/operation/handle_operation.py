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
                "user": {"id": user.id, "username": user.username, "name": user.name}
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
                "user": {"id": user.id, "username": user.username, "name": user.name}
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
