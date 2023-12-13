from enum import Enum
import json


class OperationType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"


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
