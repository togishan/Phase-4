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
                print(f"Sending {operation}")
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
                operation_response = OperationResponseFactory.deserialize(
                    operation_response_bytes
                )
                print(f"Received {operation_response}")
                return operation_response

            s.connect((HOST, PORT))

            username = "test_username"
            password = "test_password"
            name = "test_name"

            # Register
            register_operation = Operation(
                type=OperationType.REGISTER,
                args={"username": username, "password": password, "name": name},
            )

            send_data(register_operation)
            register_operation_response = get_data()

            # Login
            login_operation = Operation(
                type=OperationType.LOGIN,
                args={"username": username, "password": password},
            )
            send_data(login_operation)
            login_operation_response = get_data()

            # # Logout
            # logout_operation = Operation(
            #     type=OperationType.LOGOUT,
            #     args={},
            # )
            # send_data(logout_operation)
            # logout_operation_response = get_data()

            # Create organization
            create_organization_operation = Operation(
                type=OperationType.CREATE_ORGANIZATION,
                args={"name": "test_organization"},
            )
            send_data(create_organization_operation)
            create_organization_operation_response = get_data()

            # Create room
            create_room_operation = Operation(
                type=OperationType.CREATE_ROOM,
                args={
                    "name": "test_room",
                    "x": 0,
                    "y": 0,
                    "capacity": 10,
                    "open_time": "10:00",
                    "close_time": "20:00",
                },
            )
            send_data(create_room_operation)
            create_room_operation_response = get_data()

            # Add room to organization
            organization_id = create_organization_operation_response.result[
                "organization"
            ]["id"]
            room_id = create_room_operation_response.result["room"]["id"]

            add_room_to_organization_operation = Operation(
                type=OperationType.ADD_ROOM_TO_ORGANIZATION,
                args={
                    "organization_id": organization_id,
                    "room_id": room_id,
                },
            )
            send_data(add_room_to_organization_operation)
            add_room_to_organization_operation_response = get_data()

    except ServerDisconnectedError:
        print("Server disconnected")
