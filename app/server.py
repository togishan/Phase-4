import socket
from multiprocessing import Process, Manager, Semaphore
import sys
from .dependency_manager import DependencyManager

from .operation.operation import (
    InvalidOperationFormatError,
    OperationFactory,
)
from .operation.operation_response import OperationResponse
from .operation.handle_operation import handle_operation
from uuid import uuid4, UUID

from .server_utils import ClientDisconnectedError, get_data, send_data

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = None  # Port to listen on (non-privileged ports are > 1023)


def handle_client(
    conn: socket.socket,
    addr,
    query_dict: dict,
    notification_semaphore: Semaphore,
    notification_thread_id: UUID,
):
    DependencyManager.register(dict, query_dict)
    DependencyManager.register(Semaphore, notification_semaphore)
    DependencyManager.register(UUID, notification_thread_id)

    try:
        with conn:
            print(f"Connected by {addr}")
            while True:
                # Parse incoming data to Operation
                try:
                    incoming_operation = get_data(conn)
                except InvalidOperationFormatError:
                    operation_response = OperationResponse(
                        status=False,
                        result={"message": "Invalid operation format"},
                    )
                    send_data(conn, operation_response)
                    continue

                # Handle operation
                operation_response = handle_operation(incoming_operation)

                send_data(conn, operation_response)
    except ClientDisconnectedError:
        print(f"Client {addr} disconnected")


def handle_notification(
    conn: socket.socket,
    addr,
    query_dict: dict,
    notification_semaphore: Semaphore,
    notification_thread_id: UUID,
):
    while True:
        notification_semaphore.acquire()
        print("Notification received")

        my_queries_iterator = filter(
            lambda query: query["notification_thread_id"] == notification_thread_id,
            query_dict.values(),
        )

        for query in my_queries_iterator:
            actual_query = query["query"]
            query_operation = OperationFactory.deserialize(actual_query)
            query_operation_response = handle_operation(query_operation)
            send_data(conn, query_operation_response)


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

    with Manager() as manager:
        query_dict: dict = manager.dict()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Listening on {HOST}:{PORT}")

            while True:
                conn, addr = s.accept()

                notification_thread_id = uuid4()
                notification_semaphore = manager.Semaphore()
                notification_semaphore.acquire()

                notification_process = Process(
                    target=handle_notification,
                    args=(
                        conn,
                        addr,
                        query_dict,
                        notification_semaphore,
                        notification_thread_id,
                    ),
                )
                notification_process.start()

                p = Process(
                    target=handle_client,
                    args=(
                        conn,
                        addr,
                        query_dict,
                        notification_semaphore,
                        notification_thread_id,
                    ),
                )
                notification_semaphore.release()
                p.start()
