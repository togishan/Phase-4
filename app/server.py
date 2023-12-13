import socket
from multiprocessing import Process
import sys

from .operation.operation import (
    Operation,
    InvalidOperationFormatError,
    OperationFactory,
)
from .operation.operation_response import OperationResponse
from .operation.handle_operation import handle_operation

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = None  # Port to listen on (non-privileged ports are > 1023)


class ClientDisconnectedError(Exception):
    pass


def handle_client(conn: socket.socket, addr):
    def get_data() -> Operation:
        data_len_bytes = conn.recv(4)
        if not data_len_bytes:
            raise ClientDisconnectedError()

        data_len = int.from_bytes(data_len_bytes, "big")

        operation_bytes = conn.recv(data_len)
        operation = OperationFactory.deserialize(operation_bytes)
        print(f"Received {operation}")
        return operation

    def send_data(operation_response: OperationResponse):
        print(f"Sending {operation_response}")
        response_bytes = operation_response.serialize()

        response_len = len(response_bytes)
        response_len_bytes = response_len.to_bytes(4, "big")

        conn.sendall(response_len_bytes)
        conn.sendall(response_bytes)

    try:
        with conn:
            print(f"Connected by {addr}")
            while True:
                # Parse incoming data to Operation
                try:
                    incoming_operation = get_data()
                except InvalidOperationFormatError:
                    operation_response = OperationResponse(
                        status=False,
                        result={"message": "Invalid operation format"},
                    )
                    send_data(operation_response)
                    continue

                # Handle operation
                operation_response = handle_operation(incoming_operation)

                send_data(operation_response)
    except ClientDisconnectedError:
        print(f"Client {addr} disconnected")


if __name__ == "__main__":
    args = sys.argv
    if not args or len(args) != 3:
        print("Usage: python main.py --port <PORT>")
        sys.exit(1)

    if args[1] != "--port":
        print("Usage: python main.py --port <PORT>")
        sys.exit(1)

    try:
        PORT = int(args[2])
        if PORT < 1024:
            print("PORT must be greater than 1023")
            sys.exit(1)
    except ValueError:
        print("PORT must be an integer")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            p = Process(target=handle_client, args=(conn, addr))
            p.start()
