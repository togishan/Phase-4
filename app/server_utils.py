import socket
from .operation.operation import Operation, OperationFactory
from .operation.operation_response import OperationResponse


class ClientDisconnectedError(Exception):
    pass


def get_data(conn: socket.socket) -> Operation:
    data_len_bytes = conn.recv(4)
    if not data_len_bytes:
        raise ClientDisconnectedError()

    data_len = int.from_bytes(data_len_bytes, "big")

    operation_bytes = conn.recv(data_len)
    operation = OperationFactory.deserialize(operation_bytes)
    print(f"Received {operation}")
    return operation


def send_data(conn: socket.socket, operation_response: OperationResponse):
    print(f"Sending {operation_response}")
    response_bytes = operation_response.serialize()

    response_len = len(response_bytes)
    response_len_bytes = response_len.to_bytes(4, "big")

    conn.sendall(response_len_bytes)
    conn.sendall(response_bytes)
