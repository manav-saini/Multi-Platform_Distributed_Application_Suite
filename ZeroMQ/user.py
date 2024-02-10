# user.py
import zmq
import uuid

class User:
    def __init__(self):
        self.context = zmq.Context()

        # Generate a random user UUID
        self.user_uuid = str(uuid.uuid4())

        # Connect to Message Server
        self.message_socket = self.context.socket(zmq.REQ)
        self.message_socket.connect("tcp://localhost:2000")

        # Send GROUP LIST REQUEST to Message Server
        self.message_socket.send_string(f"GROUP LIST REQUEST FROM LOCALHOST:2000 [{self.user_uuid}]")
        server_list = self.message_socket.recv_string()
        print("Group List:")
        print(server_list)

        # Connect to Group Server
        # group_server_ip = input("Enter the Group Server IP: ")
        group_server_ip = "localhost"
        group_server_port = input("Enter the port for Group Server: ")
        self.group_socket = self.context.socket(zmq.REQ)
        self.group_socket.connect(f"tcp://{group_server_ip}:{group_server_port}")

    def print_menu(self):
        print("1. Join Group")
        print("2. Leave Group")
        print("3. Get Messages")
        print("4. Send Message")
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
        self.group_socket.send_string(f"MESSAGE SEND FROM {self.user_uuid} {user_message}")
        response = self.group_socket.recv_string()
        print(response)

    def run(self):
        while True:
            self.print_menu()
            choice = input("Enter your choice (0-4): ")

            if choice == "1":
                self.join_group()
            elif choice == "2":
                self.leave_group()
            elif choice == "3":
                self.get_messages()
            elif choice == "4":
                self.send_message()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    user = User()
    user.run()
