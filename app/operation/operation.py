from enum import Enum
import json


class OperationType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"

    CREATE_ORGANIZATION = "create_organization"
    CHANGE_USER_PERMISSON_FOR_ORGANIZATION = "change_user_permission_for_organization"
    QUERY_ORGANIZATION = "query_organization"

    CREATE_ROOM = "create_room"
    CHANGE_USER_PERMISSON_FOR_ROOM = "change_user_permission_for_room"
    ADD_ROOM_TO_ORGANIZATION = "add_room_to_organization"
    LIST_ROOMS_OF_ORGANIZATION = "list_rooms_of_organization"
    DELETE_ROOM_FROM_ORGANIZATION = "delete_room_from_organization"
    DELETE_RESERVATION_OF_ROOM = "delete_reservation_of_room"
    ACCESS_ROOM = "access_room"
    FIND_ROOM_OF_ORGANIZATION_FOR_EVENT = "find_room_of_organization_for_event"
    FIND_ROOM_SCHEDULE_OF_ORGANIZATION_FOR_EVENTS = (
        "find_schedule_of_room_of_organization"
    )

    CREATE_EVENT = "create_event"
    CHANGE_USER_PERMISSON_FOR_EVENT = "change_user_permission_for_event"
    RESERVE_ROOM_FOR_EVENT = "reserve_room_for_event"
    RERESERVE_ROOM_FOR_EVENT = "rereserve_room_for_event"
    LIST_EVENTS_OF_ROOM = "list_events_of_room"

    ADD_QUERY = "add_query"
    DEL_QUERY = "del_query"
    ROOM_VIEW = "room_view"
    DAY_VIEW = "day_view"


class InvalidOperationFormatError(Exception):
    pass


class Operation:
    def __init__(self, type: OperationType, args: dict) -> None:
        self.type: OperationType = type
        self.args: dict = args

    def to_dict(self) -> dict:
        return {"type": self.type, "args": self.args}

    def serialize(self) -> bytes:
        return json.dumps(self.to_dict()).encode("utf-8")

    def __str__(self) -> str:
        return f"Operation(type={self.type}, args={self.args})"


class OperationFactory:
    @staticmethod
    def from_dict(operation_data_json: dict) -> Operation:
        try:
            operation_type: OperationType = OperationType(operation_data_json["type"])
            args: dict = operation_data_json["args"]
            return Operation(type=operation_type, args=args)
        except:
            raise InvalidOperationFormatError()

    @staticmethod
    def deserialize(operation_data: bytes) -> Operation:
        return OperationFactory.from_dict(json.loads(operation_data.decode("utf-8")))
