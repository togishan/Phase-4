from ..client_utils import send_data, get_data
import socket


from ..models import Room, Organization, RoomInOrganization
from ..operation.operation import Operation, OperationType
from .utils import get_random_string


HOST = "localhost"
PORT = 65432


class TestRoomEventOperations:
    def setup_method(self):
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
        
		# Create an organization
        self.organization_name = get_random_string(10)
        create_organization_operation = Operation(
            OperationType.CREATE_ORGANIZATION, {"name": self.organization_name}
        )
        send_data(self.s, create_organization_operation)
        create_organization_operation_response = get_data(self.s)
        self.organization_id = create_organization_operation_response.result[
            "organization"
        ]["id"]
        send_data(self.s, create_organization_operation)
        create_organization_operation_response = get_data(self.s)
        self.organization_id = create_organization_operation_response.result[
            "organization"
        ]["id"]
        
        # Create a room
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
            },
        )
        send_data(self.s, create_room_operation)
        create_room_operation_response = get_data(self.s)
        self.room_id = create_room_operation_response.result["room"]["id"]
        
		# Add room to organization
        add_room_to_organization_operation = Operation(
            OperationType.ADD_ROOM_TO_ORGANIZATION,
            {
                "organization_id": self.organization_id,
                "room_id": self.room_id,
            },
        )
        send_data(self.s, add_room_to_organization_operation)
        add_room_to_organization_operation_response = get_data(self.s)
		
        # Create a non-periodic event but not reserve yet
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
        self.non_periodic_event_id = event_create_operation_response.result["event"]["id"]

        # Create a periodic event but not reserve yet
        event_create_operation = Operation(
            OperationType.CREATE_EVENT,
            {
                "title": get_random_string(10),
                "description": get_random_string(10),
                "category": "MEETING",
                "capacity": 10,
                "duration": 10,
                "weekly": "2023.2.25",
            },
        )
        send_data(self.s, event_create_operation)
        event_create_operation_response = get_data(self.s)
        self.periodic_event_id = event_create_operation_response.result["event"]["id"]

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
        change_user_permissions_for_organization_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_ORGANIZATION,
            {
                "organization_id": self.organization_id,
                "user_id": self.non_owner_user_id,
                "permissions": ["ADD", "ACCESS", "LIST", "DELETE"],
            },
        )
        send_data(self.s, change_user_permissions_for_organization_operation)
        change_user_permissions_for_organization_operation_response = get_data(self.s)

        # Change Room Permissions for a User (Only owner can modify user permissions)
        change_user_permissions_for_room_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_ROOM,
            {
                "room_id": self.room_id,
                "user_id": self.non_owner_user_id,
                "permissions": ["WRITE", "LIST", "RESERVE", "PERRESERVE", "DELETE"],
            },
        )
        send_data(self.s, change_user_permissions_for_room_operation)
        change_user_permissions_for_room_operation_response = get_data(self.s)

        # Change Non-Periodic Event Permissions for a User (Only owner can modify user permissions)
        change_user_permissions_for_event_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_EVENT,
            {
                "event_id": self.non_periodic_event_id,
                "user_id": self.non_owner_user_id,
                "permissions": ["WRITE", "READ"],
            },
        )
        send_data(self.s, change_user_permissions_for_event_operation)
        change_user_permissions_for_event_operation_response = get_data(self.s)

        # Change Periodic Event Permissions for a User (Only owner can modify user permissions)
        change_user_permissions_for_event_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_EVENT,
            {
                "event_id": self.periodic_event_id,
                "user_id": self.non_owner_user_id,
                "permissions": ["WRITE", "READ"],
            },
        )
        send_data(self.s, change_user_permissions_for_event_operation)
        change_user_permissions_for_event_operation_response = get_data(self.s)

        # login as a non owner
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.non_owner_username,
                "password": self.non_owner_password,
            },
        )
        send_data(self.s, login_operation)
        login_operation_response = get_data(self.s)

    def test_reserve_room_non_periodic(self):
        # Non Periodic Reservee
        reserve_room_for_event_operation = Operation(
            OperationType.RESERVE_ROOM_FOR_EVENT,
            {
                "room_id": self.room_id,
                "event_id": self.non_periodic_event_id,
                "start_time": "2021-01-01 09:00",
            },
        )
        send_data(self.s, reserve_room_for_event_operation)
        reserve_room_for_event_operation_response = get_data(self.s)
        assert True == reserve_room_for_event_operation_response.status
        assert (
            self.non_periodic_event_id
            == reserve_room_for_event_operation_response.result[
                "event"
            ]["id"]
        )
        assert (
            self.room_id
            == reserve_room_for_event_operation_response.result[
                "event"
            ]["location"]["id"]
        )

    def test_reserve_room_periodic(self):
        # Create a periodic event

        # Periodic Reservee
        reserve_room_for_event_operation = Operation(
            OperationType.RESERVE_ROOM_FOR_EVENT,
            {
                "room_id": self.room_id,
                "event_id": self.periodic_event_id,
                "start_time": "2021-01-01 09:00",
            },
        )
        send_data(self.s, reserve_room_for_event_operation)
        reserve_room_for_event_operation_response = get_data(self.s)
        assert True == reserve_room_for_event_operation_response.status
        assert (
            self.periodic_event_id
            == reserve_room_for_event_operation_response.result[
                "event"
            ]["id"]
        )
        assert (
            self.room_id
            == reserve_room_for_event_operation_response.result[
                "event"
            ]["location"]["id"]
        )

    # Will fail due to the conflict
        
    #def test_conflict(self):
    #    self.test_reserve_room_non_periodic()
    #    self.test_reserve_room_periodic()

    def test_list_events_in_room(self):
        self.test_reserve_room_non_periodic()
        list_events_of_room_operation = Operation(
            OperationType.LIST_EVENTS_OF_ROOM,
            {
                "room_id": self.room_id,
            },
        )
        send_data(self.s, list_events_of_room_operation)
        list_events_of_room_operation_response = get_data(self.s)

        assert True == list_events_of_room_operation_response.status
        assert (
            self.non_periodic_event_id
            == list_events_of_room_operation_response.result[
                "events"
            ][0]["id"]
        )

    def test_delete_reservation_of_room(self):
        self.test_reserve_room_non_periodic()
        delete_reservation_of_room_operation = Operation(
            OperationType.DELETE_RESERVATION_OF_ROOM,
            {
                "event_id": self.non_periodic_event_id,
            },
        )
        send_data(self.s, delete_reservation_of_room_operation)
        delete_reservation_of_room_operation_response = get_data(self.s)

        assert True == delete_reservation_of_room_operation_response.status
        assert (
            self.non_periodic_event_id
            == delete_reservation_of_room_operation_response.result[
                "event"
            ]["id"]
        )

        # check by looking at reserved events list
        list_events_of_room_operation = Operation(
            OperationType.LIST_EVENTS_OF_ROOM,
            {
                "room_id": self.room_id,
            },
        )
        send_data(self.s, list_events_of_room_operation)
        list_events_of_room_operation_response = get_data(self.s)

        assert True == list_events_of_room_operation_response.status
        assert [] == list_events_of_room_operation_response.result["events"]

    def test_try_without_permissions(self):
        # login as an owner again to change permissions
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.owner_username,
                "password": self.owner_password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)

        # Change Room Permissions for both users
        change_organization_permissions_for_user_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_ROOM,
            {
                 "room_id": self.room_id,
                "user_id": self.non_owner_user_id,
                "permissions": [],
            },
        )
        send_data(self.s, change_organization_permissions_for_user_operation)
        change_user_permissions_for_room_operation_response = get_data(self.s)

        change_organization_permissions_for_user_operation = Operation(
            OperationType.CHANGE_USER_PERMISSON_FOR_ROOM,
            {
                "room_id": self.room_id,
                "user_id": self.owner_user_id,
                "permissions": [],
            },
        )
        send_data(self.s, change_organization_permissions_for_user_operation)
        change_user_permissions_for_room_operation_response = get_data(self.s)

        # execute these as an owner
        # they will pass since the owner does not need a permission
        self.test_delete_reservation_of_room()
        self.test_list_events_in_room()

        # delete event to avoid conflict
        delete_reservation_of_room_operation = Operation(
            OperationType.DELETE_RESERVATION_OF_ROOM,
            {
                "event_id": self.non_periodic_event_id,
            },
        )
        send_data(self.s, delete_reservation_of_room_operation)
        delete_reservation_of_room_operation_response = get_data(self.s)

        self.test_reserve_room_periodic()

        # delete event to avoid conflict
        delete_reservation_of_room_operation = Operation(
            OperationType.DELETE_RESERVATION_OF_ROOM,
            {
                "event_id": self.periodic_event_id,
            },
        )
        send_data(self.s, delete_reservation_of_room_operation)
        delete_reservation_of_room_operation_response = get_data(self.s)


        # now login as a non owner user
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.non_owner_username,
                "password": self.non_owner_password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)

        # Without permission execute reserve
        reserve_room_for_event_operation = Operation(
            OperationType.RESERVE_ROOM_FOR_EVENT,
            {
                "room_id": self.room_id,
                "event_id": self.non_periodic_event_id,
                "start_time": "2021-01-01 09:00",
            },
        )
        send_data(self.s, reserve_room_for_event_operation)
        reserve_room_for_event_operation_response = get_data(self.s)
        assert False == reserve_room_for_event_operation_response.status 
        assert (
            "User does not have permission to reserve events"
            == reserve_room_for_event_operation_response.result["message"]
        )

        # Without permission execute perreserve
        reserve_room_for_event_operation = Operation(
            OperationType.RESERVE_ROOM_FOR_EVENT,
            {
                "room_id": self.room_id,
                "event_id": self.periodic_event_id,
                "start_time": "2021-01-01 09:00",
            },
        )
        send_data(self.s, reserve_room_for_event_operation)
        reserve_room_for_event_operation_response = get_data(self.s)
        assert False == reserve_room_for_event_operation_response.status 
        assert (
            "User does not have permission to reserve events"
            == reserve_room_for_event_operation_response.result["message"]
        )

        # login back as an owner to add reservation (so there will be an object that can be deletable)
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.owner_username,
                "password": self.owner_password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)
        reserve_room_for_event_operation = Operation(
            OperationType.RESERVE_ROOM_FOR_EVENT,
            {
                "room_id": self.room_id,
                "event_id": self.non_periodic_event_id,
                "start_time": "2021-01-01 09:00",
            },
        )
        send_data(self.s, reserve_room_for_event_operation)
        reserve_room_for_event_operation_response = get_data(self.s)
        

        # login back as a non-owner 
        login_operation = Operation(
            OperationType.LOGIN,
            {
                "username": self.non_owner_username,
                "password": self.non_owner_password,
            },
        )
        send_data(self.s, login_operation)
        get_data(self.s)

        # Without permission execute delete
        delete_reservation_of_room_operation = Operation(
            OperationType.DELETE_RESERVATION_OF_ROOM,
            {
                "event_id": self.non_periodic_event_id,
            },
        )
        send_data(self.s, delete_reservation_of_room_operation)
        delete_reservation_of_room_operation_response = get_data(self.s)
        assert False == delete_reservation_of_room_operation_response.status 
        assert (
            "User does not have permission to delete events"
            == delete_reservation_of_room_operation_response.result["message"]
        )

        # Without permission execute list events
        list_events_of_room_operation = Operation(
            OperationType.LIST_EVENTS_OF_ROOM,
            {
                "room_id": self.room_id,
            },
        )
        send_data(self.s, list_events_of_room_operation)
        list_events_of_room_operation_response = get_data(self.s)

        assert False == list_events_of_room_operation_response.status 
        assert (
            "User does not have permission to list events"
            == list_events_of_room_operation_response.result["message"]
        )

    def test_delete_room_from_organization(self):
        # attach an event to room and delete them together 
        self.test_reserve_room_non_periodic()
        delete_room_from_organization_operation = Operation(
            OperationType.DELETE_ROOM_FROM_ORGANIZATION,
            {
                "organization_id": self.organization_id,
                "room_id": self.room_id,
            },
        )
        send_data(self.s, delete_room_from_organization_operation)
        delete_room_from_organization_operation_response = get_data(self.s)
        assert True == delete_room_from_organization_operation_response.status

        list_rooms_of_organization_operation = Operation(
            OperationType.LIST_ROOMS_OF_ORGANIZATION,
            {
                "organization_id": self.organization_id,
            },
        )
        send_data(self.s, list_rooms_of_organization_operation)
        list_rooms_of_organization_operation_response = get_data(self.s)
        assert True == list_rooms_of_organization_operation_response.status
        assert [] == list_rooms_of_organization_operation_response.result["rooms"]
        

    def teardown_method(self):
        self.s.close()

    