from .operation.operation import Operation
from .operation.operation_response import OperationResponse, OperationResponseFactory
import socket


class ServerDisconnectedError(Exception):
    pass


def send_data(s: socket.socket, operation: Operation):
    print(f"Sending {operation}")
    response_bytes = operation.serialize()

    response_len = len(response_bytes)
    response_len_bytes = response_len.to_bytes(4, "big")

    s.sendall(response_len_bytes)
    s.sendall(response_bytes)


def get_data(s: socket.socket) -> OperationResponse:
    data_len_bytes = s.recv(4)
    if not data_len_bytes:
        raise ServerDisconnectedError()
    data_len = int.from_bytes(data_len_bytes, "big")

    operation_response_bytes = s.recv(data_len)
    operation_response = OperationResponseFactory.deserialize(operation_response_bytes)
    print(f"Received {operation_response}")
    return operation_response
