import socket
import json
import time
import sys
from .operation.operation import Operation
from .operation.operation_response import OperationResponse

HOST = "0.0.0.0"
PORT = 65432

if __name__ == "__main__":
    args = sys.argv
    if not args or len(args) != 3:
        print("Usage: python client.py --port <PORT>")
        sys.exit(1)

    if args[1] != "--port":
        print("Usage: python client.py --port <PORT>")
        sys.exit(1)

    try:
        PORT = int(args[2])
        if PORT < 1024:
            print("PORT must be greater than 1023")
            sys.exit(1)
    except ValueError:
        print("PORT must be an integer")
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        def send_data(data: dict):
            print(f"Sending data: {data}")
            response_str = json.dumps(data)
            response_bytes = response_str.encode("utf-8")
            response_len = len(response_bytes)
            print(f"Sending data length: {response_len}")
            response_len_bytes = response_len.to_bytes(4, "big")
            s.sendall(response_len_bytes)
            s.sendall(response_bytes)

        def get_data() -> OperationResponse:
            data_len_bytes = s.recv(4)
            data_len = int.from_bytes(data_len_bytes, "big")
            print(f"Received data length: {data_len}")
            data = s.recv(data_len)
            data_str = data.decode("utf-8")
            data_json = json.loads(data_str)
            print(f"Received data: {data_json}")
            return OperationResponse(data_json)

        s.connect((HOST, PORT))

        dummy_operation_json = {"name": "dummy", "args": {}}
        send_data(dummy_operation_json)

        while True:
            try:
                operation_response = get_data()
            except:
                print("Cannot parse operation response")
