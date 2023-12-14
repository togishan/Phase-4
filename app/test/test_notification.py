import socket

from ..operation.operation import Operation, OperationType
from ..client_utils import send_data, get_data
from .utils import get_random_string
from ..models import Room, Organization, RoomInOrganization

HOST = "localhost"
PORT = 65432


class TestNotification:
    def setup_method(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        self.username = get_random_string(10)
        self.password = get_random_string(10)
        self.name = get_random_string(10)

        register_operation = Operation(
            OperationType.REGISTER,
            {
                "username": self.username,
                "password": self.password,
                "name": self.name,
            },
        )
        send_data(self.s, register_operation)
        register_operation_response = get_data(self.s)
        self.user_id = register_operation_response.result["user"]["id"]

        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.username,
                "password": self.password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)

        self.organization_id = Organization.create(
            name=get_random_string(10), owner_id=self.user_id
        ).id
        self.room_id = Room.create(
            name=get_random_string(10),
            owner_id=self.user_id,
            x=15,
            y=14,
            capacity=10,
            open_time="09:00",
            close_time="17:00",
        ).id

        RoomInOrganization.create(
            room_id=self.room_id, organization_id=self.organization_id
        )

    def teardown_method(self):
        self.s.close()

    def test_add_delete_query(self):
        add_query_operation = Operation(
            OperationType.ADD_QUERY,
            {
                "organization_id": 1,
                "room_id": 1,
                "category": "MEETING",
                "title": "",
                "top_left_x": None,
                "top_left_y": None,
                "bottom_right_x": None,
                "bottom_right_y": None,
            },
        )
        send_data(self.s, add_query_operation)
        add_query_operation_response = get_data(self.s)

        delete_query_operation = Operation(
            OperationType.DEL_QUERY,
            {
                "query_id": add_query_operation_response.result["query_id"],
            },
        )
        send_data(self.s, delete_query_operation)
        delete_query_operation_response = get_data(self.s)

        # event_create_operation = Operation(
        #     OperationType.CREATE_EVENT,
        #     {
        #         "title": "Test title",
        #         "description": "Test description",
        #         "category": "MEETING",
        #         "capacity": 10,
        #         "duration": 10,
        #         "weekly": None,
        #     },
        # )
        # send_data(self.s, event_create_operation)
        # event_create_operation_response = get_data(self.s)

        # self.event_id = event_create_operation_response.result["event"]["id"]

        # reserve_operation = Operation(
        #     OperationType.RESERVE_ROOM_FOR_EVENT,
        #     {
        #         "event_id": self.event_id,
        #         "room_id": self.room_id,
        #         "start_time": "2021-01-01 09:00",
        #     },
        # )
        # send_data(self.s, reserve_operation)
        # reserve_operation_response = get_data(self.s)
