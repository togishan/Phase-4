import socket
from multiprocessing import Process
import sys
import json

from .operation.operation import Operation, InvalidOperationFormatError
from .operation.handle_operation import handle_operation

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = None  # Port to listen on (non-privileged ports are > 1023)


def handle_client(conn: socket.socket, addr):
    def get_data() -> Operation:
        data_len_bytes = conn.recv(4)
        data_len = int.from_bytes(data_len_bytes, "big")
        print(f"Received data length: {data_len}")
        data = conn.recv(data_len)
        data_str = data.decode("utf-8")
        data_json = json.loads(data_str)
        print(f"Received data: {data_json}")
        return Operation(data_json)

    def send_data(data: dict):
        print(f"Sending data: {data}")
        response_str = json.dumps(data)
        response_bytes = response_str.encode("utf-8")
        response_len = len(response_bytes)
        print(f"Sending data length: {response_len}")
        response_len_bytes = response_len.to_bytes(4, "big")
        conn.sendall(response_len_bytes)
        conn.sendall(response_bytes)

    with conn:
        print(f"Connected by {addr}")
        while True:
            try:
                incoming_operation = get_data()
            except InvalidOperationFormatError:
                print("Invalid operation format")
                continue

            try:
                operation_response = handle_operation(incoming_operation)
            except:  # TODO : catch specific errors
                print("Cannot perform operation")
                continue

            send_data({"status": "success", "result": None})


if __name__ == "__main__":
    args = sys.argv
    if not args or len(args) != 3:
        print("Usage: python main.py --port <PORT>")
        sys.exit(1)

    if args[1] != "--port":
        print("Usage: python main.py --port <PORT>")
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
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            p = Process(target=handle_client, args=(conn, addr))
            p.start()
