from ..client_utils import send_data, get_data
import socket


from ..models import Room, Organization, RoomInOrganization
from ..operation.operation import Operation, OperationType
from .utils import get_random_string


HOST = "localhost"
PORT = 65432


class TestRegisterLogin:
    def setup_method(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        self.username = get_random_string(10)
        self.password = get_random_string(10)
        self.name = get_random_string(10)

    def teardown_method(self):
        self.s.close()

    def test_register_login(self):
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

        assert register_operation_response.result["user"]["name"] == self.name
        assert register_operation_response.result["user"]["username"] == self.username

        # login with correct credentials
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.username,
                "password": self.password,
            },
        )
        send_data(self.s, login_operation)
        login_operation_response = get_data(self.s)

        assert login_operation_response.result["user"]["name"] == self.name
        assert login_operation_response.result["user"]["username"] == self.username

        # wrong username
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": "wrong-username",
                "password": self.password,
            },
        )
        send_data(self.s, login_operation)
        login_operation_response = get_data(self.s)

        assert login_operation_response.status == False
        
        # wrond password
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.username,
                "password": "123",
            },
        )
        send_data(self.s, login_operation)
        login_operation_response = get_data(self.s)
        assert login_operation_response.status == False
        

    
