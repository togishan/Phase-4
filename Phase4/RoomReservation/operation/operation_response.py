import json


class InvalidOperationResponseFormatError(Exception):
    pass


class OperationResponse:
    def __init__(self, status: bool, result: dict) -> None:
        self.status: bool = status
        self.result: dict = result

    def to_dict(self) -> dict:
        return {"status": self.status, "result": self.result}

    def serialize(self) -> bytes:
        return json.dumps(self.to_dict()).encode("utf-8")

    def __str__(self) -> str:
        return f"OperationResponse(status={self.status}, result={self.result})"


class OperationResponseFactory:
    @staticmethod
    def from_dict(operation_response_data_json: dict) -> OperationResponse:
        try:
            return OperationResponse(
                status=operation_response_data_json["status"],
                result=operation_response_data_json["result"],
            )
        except:
            raise InvalidOperationResponseFormatError()

    @staticmethod
    def deserialize(operation_response_data: bytes) -> OperationResponse:
        return OperationResponseFactory.from_dict(
            json.loads(operation_response_data.decode("utf-8"))
        )
