MARKET:
gRPC and Protobuf: 
The code uses gRPC for inter-process communication and Protocol Buffers (protobuf) for defining the service methods and message types. 
shopping_pb2 and shopping_pb2_grpc are generated files from .proto definitions, which contain the classes and methods for the protobuf messages and the gRPC service, respectively.

RegisterSeller: Registers a new seller in the marketplace if they are not already registered.
SellItem: Allows a registered seller to list a new item for sale in the marketplace.
UpdateItem: Enables a seller to update the details of an item they have listed.
DeleteItem: Allows a seller to remove an item they have listed from the marketplace.
DisplaySellerItems: Lists all the items a seller has listed in the marketplace.
SearchItem: Allows users to search for items by name or category.
BuyItem: Facilitates the purchase of an item by a buyer, updating the item's quantity.
AddToWishlist: Allows a buyer to add an item to their wishlist.
RateItem: Enables a buyer to rate an item they have purchased.
notify_seller: Notify a seller when an action occurs related to their items.
notify_buyers: Notify buyers who have an item on their wishlist when that item is updated.

TO RUN:
python market.py

SELLER:
serve:
Prompts the user to enter the seller's IP address, randomly selects a port number, and starts a gRPC server for the seller service on that IP and port.
Adds the SellerServicer to handle incoming RPCs defined in the .proto file.
Uses serve_event.set() to signal that the server has started and is ready to accept connections.
The server runs indefinitely until terminated, waiting for incoming connections and handling them as defined in the SellerServicer class.

run:
Waits for the server to start (serve_event.wait()).
Prompts the user to enter the IP address and port of the marketplace server to establish a connection.
Provides a command-line interface for the seller to perform various operations by sending requests to the marketplace server through a gRPC channel.
Operations include registering as a seller, listing an item, updating an item's details, deleting an item, and viewing all items listed by the seller.
Each operation constructs a corresponding request object (defined in shopping_pb2) and sends it to the marketplace server using the appropriate method on the stub (shopping_pb2_grpc.MarketServiceStub).

Workflow
The seller starts the script, which initializes the gRPC server in a separate thread and waits for it to start.
Once the server is running, the seller is prompted to connect to the marketplace server by providing its address.
The seller can then choose to perform various operations, such as registering, listing items, etc., through a simple command-line interface.
Operations are executed as RPC calls to the marketplace server, and responses are displayed to the seller.
Notifications from the marketplace (e.g., item sold) are received by the seller's server and printed to the console.

TO RUN:
python seller.py

BUYER:
serve:
Sets up and starts the buyer's gRPC server to listen for notifications from the marketplace.
Prompts the user to enter the buyer's IP address, then randomly selects a port number for the server.
Adds the BuyerServicer to the server to handle incoming RPC calls.
Starts the server and signals its readiness using serve_event.set().
The server runs indefinitely, waiting for termination.

run:
Waits for the buyer's server to start (serve_event.wait()).
Prompts the user to enter the marketplace server's address and establishes a gRPC channel to it.
Provides a command-line interface for the buyer to interact with the marketplace, including searching for items, buying items, adding items to a wishlist, and rating items.
For each action, the buyer client constructs an appropriate request, sends it to the marketplace server using the stub (client proxy for the marketplace service), and displays the response.

Search Item: Allows the buyer to search for items by name or category in the marketplace.
Buy Item: Enables the buyer to purchase a specified quantity of an item.
Add to Wishlist: Allows the buyer to add an item to their wishlist.
Rate Item: Lets the buyer rate an item they have interacted with.
Quit: Exits the client-side interface.

TO BUY:
python buyer.py








