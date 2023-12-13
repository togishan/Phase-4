class InvalidOperationResponseFormatError(Exception):
    pass


class OperationResponse:
    def __init__(self, operation_response_data_json: dict) -> None:
        try:
            self.status = operation_response_data_json["status"]
            self.result = operation_response_data_json["result"]
        except:
            raise InvalidOperationResponseFormatError()
