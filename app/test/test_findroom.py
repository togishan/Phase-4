from ..client_utils import send_data, get_data
import socket


from ..models import Room, Organization, RoomInOrganization
from ..operation.operation import Operation, OperationType
from .utils import get_random_string


HOST = "localhost"
PORT = 65432


class TestFindRoom:
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

        event_create_operation = Operation(
            OperationType.CREATE_EVENT,
            {
                "title": get_random_string(10),
                "description": get_random_string(10),
                "category": "MEETING",
                "capacity": 10,
                "duration": 10,
                "weekly": None,
            },
        )
        send_data(self.s, event_create_operation)
        event_create_operation_response = get_data(self.s)
        self.event_id = event_create_operation_response.result["event"]["id"]

    def teardown_method(self):
        self.s.close()

    def test_find_room_initial(self):
        find_room_operation = Operation(
            OperationType.FIND_ROOM_OF_ORGANIZATION_FOR_EVENT,
            {
                "event_id": self.event_id,
                "organization_id": self.organization_id,
                "top_right_x": 15,
                "top_right_y": 14,
                "bottom_left_x": 10,
                "bottom_left_y": 5,
                "start_time": "2021-01-01 09:00",
                "end_time": "2021-01-01 10:00",
            },
        )
        send_data(self.s, find_room_operation)
        find_room_operation_response = get_data(self.s)

        assert find_room_operation_response["room"]["id"] == self.room_id
