class InvalidOperationFormatError(Exception):
    pass


class Operation:
    def __init__(self, operation_data_json: dict) -> None:
        try:
            self.name: str = operation_data_json["name"]
            self.args: dict = operation_data_json["args"]
        except:
            raise InvalidOperationFormatError()
