MESSAGE SERVER:
Initialization:
Context Setup: 
Initializes a ZeroMQ context (self.context = zmq.Context()). 
A ZMQ context is an environment in which sockets operate and is required for creating sockets.
Socket Creation: 
Creates a REP (Reply) socket (self.socket = self.context.socket(zmq.REP)). 
REP sockets are part of the request-reply pattern in ZMQ, where each request received is replied to with a corresponding response.
Socket Binding: 
Binds the socket to listen on all interfaces (*) at TCP port 2000 (tcp://*:2000). 
This means the server will listen for incoming connections on port 2000.
Group Servers Dictionary: 
Initializes an empty dictionary (self.group_servers = {}) to store the group servers' information, mapping group names to their respective ports.

handle_group_registration:
This method processes join requests from group servers:

handle_group_list_request:
This method sends a list of available group servers to a user:

run:
Checks the content of the message to determine its type. 
If it's a join request (contains "JOIN REQUEST"), it calls handle_group_registration. 
If it's a group list request (contains "GROUP LIST REQUEST"), it extracts the user's IP from the message, logs the request, and calls handle_group_list_request.

TO RUN:
python message_server.py

GROUP:
Initialization: 
Sets up the ZeroMQ context and REP socket, binding it to the specified group_port. 
Initializes sets and dictionaries to keep track of users and messages within the group.

Registration with a Message Server (register_with_message_server method): 
Connects to a central message server (presumed to be running at message_server_ip:2000) and sends a registration request. 
This step allows the group server to announce its presence to a central server that might be managing multiple groups.

Handling Client Requests (handle_client method): 
Processes different types of client requests such as joining or leaving the group, sending a message, or requesting messages. 
Each request type is identified by specific keywords in the received messages.
    Join/Leave Requests: Adds/removes the user's UUID to/from a set tracking current group members.
    Message Requests: Clients can request messages sent after a specific timestamp. The server responds with relevant messages.
    Sending Messages: Clients can send messages to the group. The server stores these with a timestamp.

Storing Messages (store_message method): Saves incoming messages with their sender UUID and a timestamp.

Retrieving Messages (get_messages_after_timestamp method): Compiles a list of messages sent after a given timestamp, formatted for presentation.

Running the Server (run method): 
Registers the server with the message server and enters a loop to continuously receive and handle messages. 
Each incoming message spawns a new thread to handle the request, allowing for concurrent processing.

Threading
The run method uses the threading module to handle each client request in a separate thread, improving the server's ability to manage multiple simultaneous requests. 
After receiving a message, a new thread is started with handle_client as the target function, and the message as an argument. 
thread.join() is called to ensure the main thread waits for the thread to complete, which might limit concurrency and could be omitted to allow true parallel processing.

TO RUN:
python group_server.py

USER:
Initialization: 
Sets up the ZeroMQ context and creates a REQ (Request) socket that connects to the central message server at localhost:2000. 
Each user instance is assigned a unique UUID.

Rreceive_live_group_list: 
Sends a request to the central message server to retrieve a list of active groups. 
The list is received as a string and printed to the console.

connect_group: 
Prompts the user to enter the port number of a group server and connects to it by setting up another REQ socket. 
This connection is used for subsequent group-specific operations.

join_group: 
Sends a join request to the currently connected group server and prints the server's response. This request includes the user's UUID.

leave_group: 
Sends a leave request to the group server and prints the server's response, similar to the join group functionality.

get_messages: 
Prompts the user to enter a timestamp (to retrieve messages sent after that timestamp) and sends a message request to the group server. The server's response (messages) is printed to the console.

send_message: 
Prompts the user to enter a message and sends it to the group server. An empty message is not allowed, and the server's response is printed.

TO RUN:
python user.py