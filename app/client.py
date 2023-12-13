import socket
import sys
from .operation.operation import Operation, OperationType
from .operation.operation_response import OperationResponse, OperationResponseFactory

HOST = "0.0.0.0"
PORT = 65432


class ServerDisconnectedError(Exception):
    pass


if __name__ == "__main__":
    args = sys.argv
    if not args or len(args) != 3:
        print("Usage: python client.py --port <PORT>")
        sys.exit(1)

    if args[1] != "--port":
        print("Usage: python client.py --port <PORT>")
        sys.exit(1)

    try:
        PORT = int(args[2])
        if PORT < 1024:
            print("PORT must be greater than 1023")
            sys.exit(1)
    except ValueError:
        print("PORT must be an integer")
        sys.exit(1)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            def send_data(operation: Operation):
                response_bytes = operation.serialize()

                response_len = len(response_bytes)
                response_len_bytes = response_len.to_bytes(4, "big")

                s.sendall(response_len_bytes)
                s.sendall(response_bytes)

            def get_data() -> OperationResponse:
                data_len_bytes = s.recv(4)
                if not data_len_bytes:
                    raise ServerDisconnectedError()
                data_len = int.from_bytes(data_len_bytes, "big")

                operation_response_bytes = s.recv(data_len)
                return OperationResponseFactory.deserialize(operation_response_bytes)

            s.connect((HOST, PORT))

            dummy_operation = Operation(type=OperationType.LOGIN, args={})
            print(f"Sending {dummy_operation}")

            send_data(dummy_operation)

            while True:
                operation_response = get_data()
                print(f"Received {operation_response}")
    except ServerDisconnectedError:
        print("Server disconnected")
