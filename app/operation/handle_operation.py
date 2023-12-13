from .operation import Operation
from .operation_response import OperationResponse


def handle_operation(
    operation: Operation, authenticated_user_id: str
) -> OperationResponse:
    return OperationResponse(status=False, result={"message": "Not implemented"})
    pass  # TODO : implement
