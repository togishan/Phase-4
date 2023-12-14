from ..client_utils import send_data, get_data
import socket

HOST = "localhost"
PORT = 65432


class TestFindRoom:
    def setup_method(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def teardown_method(self):
        self.s.close()

    def test_find_room_initial(self):
        pass
