from ..client_utils import send_data, get_data
import socket


from ..models import Room, Organization, RoomInOrganization
from ..operation.operation import Operation, OperationType
from .utils import get_random_string


HOST = "localhost"
PORT = 65432


class TestCreate:
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

    def teardown_method(self):
        self.s.close()

    def test_create_organization(self):

        self.organization_name = get_random_string(10)

        create_organization_operation = Operation(
            OperationType.CREATE_ORGANIZATION,
            {
                "name": self.organization_name
            }
        )
        send_data(self.s, create_organization_operation)
        create_organization_operation_response = get_data(self.s)
        self.organization_id = create_organization_operation_response.result["organization"]["id"]
        assert create_organization_operation_response.status == True
        assert create_organization_operation_response.result["organization"]["name"] == self.organization_name
        assert create_organization_operation_response.result["organization"]["owner"]["id"] == self.user_id

       
    def test_create_room(self):
        self.room_name = get_random_string(10)
        create_room_operation = Operation(
            OperationType.CREATE_ROOM,
            {
                "name": self.room_name,
                "x": 15,
                "y": 14,
                "capacity": 10,
                "open_time": "09:00",
                "close_time": "17:00",
            }
        )
        send_data(self.s, create_room_operation)
        create_room_operation_response = get_data(self.s)
        self.room_id = create_room_operation_response.result["room"]["id"]
        assert True, create_room_operation_response
        assert create_room_operation_response.result["room"]["name"] == self.room_name

       
    def test_create_event(self):
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
        assert True, event_create_operation.status