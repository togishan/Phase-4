from ..client_utils import send_data, get_data
import socket


from ..models import Room, Organization, RoomInOrganization
from ..operation.operation import Operation, OperationType
from .utils import get_random_string


HOST = "localhost"
PORT = 65432


class TestOrganizationAddListAccessDelete:
    def setup_method(self):
        # Owner creates an organization and rooms 

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        self.owner_username = get_random_string(10)
        self.owner_password = get_random_string(10)
        self.owner_name = get_random_string(10)

        register_operation = Operation(
            OperationType.REGISTER,
            {
                "username": self.owner_username,
                "password": self.owner_password,
                "name": self.owner_name,
            },
        )
        send_data(self.s, register_operation)
        register_operation_response = get_data(self.s)
        self.owner_user_id = register_operation_response.result["user"]["id"]

        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.owner_username,
                "password": self.owner_password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)

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
        
        self.room1_name = get_random_string(10)
        create_room_operation = Operation(
            OperationType.CREATE_ROOM,
            {
                "name": self.room1_name,
                "x": 15,
                "y": 14,
                "capacity": 10,
                "open_time": "09:00",
                "close_time": "17:00",
            }
        )
        send_data(self.s, create_room_operation)
        create_room_operation_response = get_data(self.s)
        self.room1_id = create_room_operation_response.result["room"]["id"]

        self.room2_name = get_random_string(10)
        create_room_operation = Operation(
            OperationType.CREATE_ROOM,
            {
                "name": self.room2_name,
                "x": 25,
                "y": 12,
                "capacity": 15,
                "open_time": "09:00",
                "close_time": "17:00",
            }
        )
        send_data(self.s, create_room_operation)
        create_room_operation_response = get_data(self.s)
        self.room2_id = create_room_operation_response.result["room"]["id"]

        # register a non owner user 
        self.non_owner_username = get_random_string(10)
        self.non_owner_password = get_random_string(10)
        self.non_owner_name = get_random_string(10)
        register_operation = Operation(
            OperationType.REGISTER,
            {
                "username": self.non_owner_username,
                "password": self.non_owner_password,
                "name": self.non_owner_name,
            },
        )
        send_data(self.s, register_operation)
        register_operation_response = get_data(self.s)
        self.non_owner_user_id = register_operation_response.result["user"]["id"]
        
        # Change Organization Permissions for a User (Only owner can modify user permissions)
        change_organization_permissions_for_user_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_ORGANIZATION,
            {
                "organization_id": self.organization_id,
                "user_id": self.non_owner_user_id,
                "permissions": ["ADD", "ACCESS","LIST","DELETE"],
            }
        )
        send_data(self.s, change_organization_permissions_for_user_operation)
        change_organization_permissions_for_user_operation_response = get_data(self.s)
        
        # now login as a user who does not own the organization

        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.non_owner_username,
                "password": self.non_owner_password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)


    def teardown_method(self):
        self.s.close()

    def test_add_room_to_organization(self):
        
        # A non owner user tries to add room to the organization
        add_room_to_organization_operation = Operation(
            OperationType.ADD_ROOM_TO_ORGANIZATION,
            {
                "organization_id": self.organization_id,
                "room_id": self.room1_id,
            },
        )
        send_data(self.s, add_room_to_organization_operation)
        add_room_to_organization_operation_response = get_data(self.s)
        
        assert True, add_room_to_organization_operation_response.status
        assert self.owner_user_id == add_room_to_organization_operation_response.result["room_in_organization"]["room"]["owner"]["id"]
        


    def test_list_rooms(self):
        self.test_add_room_to_organization()
        
        # A non owner user tries to list rooms
        list_rooms_of_organization_operation = Operation(
            OperationType.LIST_ROOMS_OF_ORGANIZATION,
            {
                "organization_id": self.organization_id,
            },
        )
        send_data(self.s, list_rooms_of_organization_operation)
        list_rooms_of_organization_operation_response = get_data(self.s)
        assert True, list_rooms_of_organization_operation_response.status
        assert False, "ffff"