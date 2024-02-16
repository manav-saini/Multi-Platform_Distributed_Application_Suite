import zmq
import uuid

class User:
    def __init__(self):
        self.context = zmq.Context()
        self.user_uuid = str(uuid.uuid4())
        self.message_socket = self.context.socket(zmq.REQ)
        self.message_socket.connect("tcp://localhost:2000")

    def receive_live_group_list(self):
        self.message_socket.send_string(f"GROUP LIST REQUEST FROM LOCALHOST:2000 [{self.user_uuid}]")
        server_list = self.message_socket.recv_string()
        print("Group List:")
        print(server_list)

    def connect_group(self):
        self.context = zmq.Context()
        group_server_ip = "localhost"
        group_server_port = input("Enter the port for Group Server: ")
        self.group_socket = self.context.socket(zmq.REQ)
        self.group_socket.connect(f"tcp://{group_server_ip}:{group_server_port}")

    def print_menu(self):
        print("1. Join Group")
        print("2. Leave Group")
        print("3. Get Messages")
        print("4. Send Message")
        print("5. Live Groups")
        print("0. Exit")

    def join_group(self):
        self.group_socket.send_string(f"JOIN REQUEST FROM {self.user_uuid}")
        response = self.group_socket.recv_string()
        print(response)

    def leave_group(self):
        self.group_socket.send_string(f"LEAVE REQUEST FROM {self.user_uuid}")
        response = self.group_socket.recv_string()
        print(response)

    def get_messages(self):
        timestamp = input("Enter timestamp (press Enter for all messages): ")
        self.group_socket.send_string(f"MESSAGE REQUEST FROM {self.user_uuid} {timestamp}")
        response = self.group_socket.recv_string()
        print(response)

    def send_message(self):
        user_message = input("Enter your message: ")
        if user_message=="":
            print("Empty string is not allowed")
        else:
            self.group_socket.send_string(f"MESSAGE SEND FROM {self.user_uuid} {user_message}")
            response = self.group_socket.recv_string()
            print(response)

    def run(self):
        while True: 
            self.print_menu()
            choice = input("Enter your choice (0-5): ")
            if choice == "1":
                self.connect_group()
                self.join_group()
            elif choice == "2":
                self.connect_group()
                self.leave_group()
            elif choice == "3":
                self.connect_group()
                self.get_messages()
            elif choice == "4":
                self.connect_group()
                self.send_message()
            elif choice == "5":
                self.receive_live_group_list()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    user = User()
    user.run()
