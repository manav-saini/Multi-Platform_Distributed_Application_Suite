import zmq
import threading
import uuid
import time
from queue import Queue

class GroupServer:
    def __init__(self, group_name, group_port, message_server_ip):
        self.context = zmq.Context()
        self.group_name = group_name
        self.group_port = group_port
        self.message_server_ip = message_server_ip
        self.group_users = set()
        self.group_messages = {}
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{group_port}")

        # Use a queue to pass messages between the main thread and worker threads
        self.message_queue = Queue()

    def register_with_message_server(self):
        message_socket = self.context.socket(zmq.REQ)
        message_socket.connect(f"tcp://{self.message_server_ip}:2000")
        message_socket.send_string(f"JOIN REQUEST FROM {self.group_port} [{self.group_name}]")
        response = message_socket.recv_string()
        print(response)

    def handle_client(self, message):
        if "JOIN REQUEST" in message:
            _, _, _, user_uuid = message.split()
            self.group_users.add(user_uuid)
            print(f"JOIN REQUEST FROM {user_uuid}")
            self.socket.send_string("SUCCESS")
            time.sleep(1)

        elif "LEAVE REQUEST" in message:
            _, _, _, user_uuid = message.split()
            print(f"LEAVE REQUEST FROM {user_uuid}")
            self.group_users.remove(user_uuid)
            self.socket.send_string("SUCCESS")
            time.sleep(1)

        elif "MESSAGE REQUEST" in message:
            try:
                _, _, _,user_uuid, timestamp = message.split()
                print(f"MESSAGE REQUEST FROM {user_uuid}")
                response_messages = self.get_messages_after_timestamp(timestamp)
                self.socket.send_string("\n".join(response_messages))
                time.sleep(1)
            except:
                _, _, _,user_uuid = message.split()
                timestamp = ""
                print(f"MESSAGE REQUEST FROM {user_uuid}")
                response_messages = self.get_messages_after_timestamp(timestamp)
                self.socket.send_string("\n".join(response_messages))
                time.sleep(1)


        elif "MESSAGE SEND" in message:
            _, _, _, user_uuid, user_message = message.split()
            print(f"MESSAGE SEND FROM {user_uuid}")
            self.store_message(user_uuid, user_message)
            self.socket.send_string("SUCCESS" if user_uuid in self.group_users else "FAIL")
            time.sleep(1)

        else:
            self.socket.send_string("Invalid Request")

    # def get_messages_after_timestamp(self, timestamp):
    #     messages = self.group_messages.get(timestamp, [])
    #     print(self.group_messages)
    #     print(messages)
    #     return [f"{msg['timestamp']} - {msg['user_uuid']}: {msg['content']}" for msg in messages]
    def get_messages_after_timestamp(self, timestamp):
        relevant_messages = []
        for ts, msgs in self.group_messages.items():
            if len(timestamp)!=0 and ts >= timestamp:
                relevant_messages.extend(msgs)
            else:
                relevant_messages.extend(msgs)
        return [f"{msg['timestamp']} - {msg['user_uuid']}: {msg['content']}" for msg in relevant_messages]


    def store_message(self, user_uuid, user_message):
        timestamp = time.strftime("%H:%M:%S")
        if timestamp not in self.group_messages:
            self.group_messages[timestamp] = []
        self.group_messages[timestamp].append({"user_uuid": user_uuid, "content": user_message, "timestamp": timestamp})
        print(self.group_messages)

    def run(self):
        self.register_with_message_server()
        print(f"Group Server {self.group_name} is now registered with the Message Server.")

        while True:
            message = self.socket.recv_string()
            self.handle_client(message)
            # self.message_queue.put(message)  # Put the received message in the queue
            # threading.Thread(target=self.handle_client_worker).start()

    def handle_client_worker(self):
        message = self.message_queue.get()
        if message:
            self.handle_client(message)


if __name__ == "__main__":
    group_name = input("Enter the group name: ")
    group_port = input("Enter group port: ")
    message_server_ip = "localhost"

    group_server = GroupServer(group_name, group_port, message_server_ip)
    group_server.run()
