import zmq
import uuid

class MessagingAppServer:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:2000")
        self.group_servers = {}

    def handle_group_registration(self, message):
        _, _, _, group_port, group_name = message.split()
        self.group_servers[group_name] = group_port
        print(f"JOIN REQUEST FROM {group_port} {group_name}")
        self.socket.send_string("SUCCESS")

    def handle_group_list_request(self, user_ip):
        print(f"GROUP LIST REQUEST FROM {user_ip}")
        server_list = [f"{name} - {ip}" for name, ip in self.group_servers.items()]
        self.socket.send_string("\n".join(server_list))

    def run(self):
        while True:
            message = self.socket.recv_string()

            if "JOIN REQUEST" in message:
                self.handle_group_registration(message)
            elif "GROUP LIST REQUEST" in message:
                print(message.split())
                _, _, _, _,user_ip,unique_id = message.split()
                self.handle_group_list_request(user_ip)
            else:
                self.socket.send_string("Invalid Request")

if __name__ == "__main__":
    messaging_app_server = MessagingAppServer()
    messaging_app_server.run()
