import socket
import sys
from .operation.operation import Operation, OperationType
from datetime import datetime

from .client_utils import send_data, get_data, ServerDisconnectedError

HOST = "0.0.0.0"
PORT = 65432


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
            s.connect((HOST, PORT))

            username1 = "test1"
            password1 = "test1"
            name1 = "test_name1"

            # Register user1
            register_operation1 = Operation(
                type=OperationType.REGISTER,
                args={"username": username1, "password": password1, "name": name1},
            )

            username2 = "test2"
            password2 = "test2"
            name2 = "test_name2"
            send_data(s, register_operation1)
            register_operation1_response = get_data(s)

            # Register user2
            register_operation2 = Operation(
                type=OperationType.REGISTER,
                args={"username": username2, "password": password2, "name": name2},
            )
            send_data(s, register_operation2)
            register_operation2_response = get_data(s)

            # Login
            login_operation = Operation(
                type=OperationType.LOGIN,
                args={"username": username1, "password": password1},
            )
            send_data(s, login_operation)
            login_operation_response = get_data(s)

            # # Logout
            # logout_operation = Operation(
            #     type=OperationType.LOGOUT,
            #     args={},
            # )
            # send_data(s, logout_operation)
            # logout_operation_response = get_data(s)

            # Create organization
            create_organization_operation = Operation(
                type=OperationType.CREATE_ORGANIZATION,
                args={"name": "test_organization"},
            )
            send_data(s, create_organization_operation)
            create_organization_operation_response = get_data(s)

            # Change permissions of organization
            user_id = 2
            permissions = ["LIST"]
            organization_id = create_organization_operation_response.result[
                "organization"
            ]["id"]

            change_permissions_of_organization_operation = Operation(
                type=OperationType.CHANGE_USER_PERMISSON_FOR_ORGANIZATION,
                args={
                    "user_id": user_id,
                    "organization_id": organization_id,
                    "permissions": permissions,
                },
            )
            send_data(s, change_permissions_of_organization_operation)
            change_permissions_of_organization_operation_response = get_data(s)

            # Change permissions of organization again
            user_id = 2
            permissions = ["ADD"]
            organization_id = create_organization_operation_response.result[
                "organization"
            ]["id"]

            change_permissions_of_organization_operation = Operation(
                type=OperationType.CHANGE_USER_PERMISSON_FOR_ORGANIZATION,
                args={
                    "user_id": user_id,
                    "organization_id": organization_id,
                    "permissions": permissions,
                },
            )
            send_data(s, change_permissions_of_organization_operation)
            change_permissions_of_organization_operation_response = get_data(s)

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
            send_data(s, create_room_operation)
            create_room_operation_response = get_data(s)

            # Login
            login_operation = Operation(
                type=OperationType.LOGIN,
                args={"username": username2, "password": password2},
            )
            send_data(s, login_operation)
            login_operation_response = get_data(s)

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
            send_data(s, add_room_to_organization_operation)
            add_room_to_organization_operation_response = get_data(s)

            # Change permissions of room
            user_id = 2
            permissions = ["WRITE"]
            room_id = create_room_operation_response.result["room"]["id"]

            change_user_permission_for_room_operation = Operation(
                type=OperationType.CHANGE_USER_PERMISSON_FOR_ROOM,
                args={
                    "user_id": user_id,
                    "room_id": room_id,
                    "permissions": permissions,
                },
            )
            send_data(s, change_user_permission_for_room_operation)
            change_user_permission_for_room_operation_response = get_data(s)

            # Create event
            create_event_operation = Operation(
                type=OperationType.CREATE_EVENT,
                args={
                    "title": "test_event",
                    "description": "test_description",
                    "category": "STUDY",
                    "capacity": 100,
                    "duration": 60,
                    "weekly": None,
                },
            )
            send_data(s, create_event_operation)
            create_event_operation_response = get_data(s)

            # Change permissions of event
            user_id = 2
            permissions = ["WRITE"]
            event_id = create_event_operation_response.result["event"]["id"]

            change_user_permission_for_event_operation = Operation(
                type=OperationType.CHANGE_USER_PERMISSON_FOR_EVENT,
                args={
                    "user_id": user_id,
                    "event_id": event_id,
                    "permissions": permissions,
                },
            )
            send_data(s, change_user_permission_for_event_operation)
            change_user_permission_for_event_operation_response = get_data(s)

            # Login
            login_operation = Operation(
                type=OperationType.LOGIN,
                args={"username": username1, "password": password1},
            )
            send_data(s, login_operation)
            login_operation_response = get_data(s)

            # List rooms of organization
            organization_id = create_organization_operation_response.result[
                "organization"
            ]["id"]

            list_rooms_of_organization_operation = Operation(
                type=OperationType.LIST_ROOMS_OF_ORGANIZATION,
                args={
                    "organization_id": organization_id,
                },
            )
            send_data(s, list_rooms_of_organization_operation)
            list_rooms_of_organization_operation_response = get_data(s)

            # # Delete room
            # room_id = create_room_operation_response.result["room"]["id"]
            # organization_id = create_organization_operation_response.result[
            #     "organization"
            # ]["id"]

            # delete_room_operation = Operation(
            #     type=OperationType.DELETE_ROOM_FROM_ORGANIZATION,
            #     args={
            #         "room_id": room_id,
            #         "organization_id": organization_id,
            #     },
            # )
            # send_data(s, delete_room_operation)
            # delete_room_operation_response = get_data(s)

            # Reserve room for event
            event_id = create_event_operation_response.result["event"]["id"]
            room_id = create_room_operation_response.result["room"]["id"]
            start_time = datetime.now().isoformat()

            reserve_room_for_event_operation = Operation(
                type=OperationType.RESERVE_ROOM_FOR_EVENT,
                args={
                    "event_id": event_id,
                    "room_id": room_id,
                    "start_time": start_time,
                },
            )
            send_data(s, reserve_room_for_event_operation)
            reserve_room_for_event_operation_response = get_data(s)

            # List events of room
            room_id = create_room_operation_response.result["room"]["id"]

            list_events_of_room_operation = Operation(
                type=OperationType.LIST_EVENTS_OF_ROOM,
                args={
                    "room_id": room_id,
                },
            )
            send_data(s, list_events_of_room_operation)
            list_events_of_room_operation_response = get_data(s)

            # Delete reservation of room
            event_id = create_event_operation_response.result["event"]["id"]

            delete_reservation_of_room_operation = Operation(
                type=OperationType.DELETE_RESERVATION_OF_ROOM,
                args={
                    "event_id": event_id,
                },
            )
            send_data(s, delete_reservation_of_room_operation)
            delete_reservation_of_room_operation_response = get_data(s)

            # List events of room
            room_id = create_room_operation_response.result["room"]["id"]

            list_events_of_room_operation = Operation(
                type=OperationType.LIST_EVENTS_OF_ROOM,
                args={
                    "room_id": room_id,
                },
            )
            send_data(s, list_events_of_room_operation)
            list_events_of_room_operation_response = get_data(s)

            # # Reserve room for event
            # event_id = create_event_operation_response.result["event"]["id"]
            # room_id = create_room_operation_response.result["room"]["id"]
            # start_time = datetime.now().isoformat()

            # reserve_room_for_event_operation = Operation(
            #     type=OperationType.RESERVE_ROOM_FOR_EVENT,
            #     args={
            #         "event_id": event_id,
            #         "room_id": room_id,
            #         "start_time": start_time,
            #     },
            # )
            # send_data(s, reserve_room_for_event_operation)
            # reserve_room_for_event_operation_response = get_data(s)

            # Access room
            room_id = create_room_operation_response.result["room"]["id"]

            access_room_operation = Operation(
                type=OperationType.ACCESS_ROOM,
                args={
                    "room_id": room_id,
                },
            )
            send_data(s, access_room_operation)
            access_room_operation_response = get_data(s)

    except ServerDisconnectedError:
        print("Server disconnected")
