import grpc
import shopping_pb2
import shopping_pb2_grpc
from concurrent.futures import ThreadPoolExecutor
import random
import uuid
import threading

ip_address = "0"
port = "0"
serve_event = threading.Event()

class BuyerServicer(shopping_pb2_grpc.BuyerServiceServicer):
    def NotifyClient(self, request, context):
        print("\n[NOTIFICATION] ITEM UPDATED BY SELLER")
        print(request)
        return shopping_pb2.Notification(message=f"RECEIVED")

def serve():
    global ip_address, port
    ip_address = input("Enter buyer IP address: ")
    port = str(random.randint(5001, 5999))
    server = grpc.server(ThreadPoolExecutor())
    shopping_pb2_grpc.add_BuyerServiceServicer_to_server(BuyerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Buyer server running on port {port}")
    serve_event.set() 
    server.wait_for_termination()

def run():
    serve_event.wait()
    market_ip = input("Enter Market host ip with addr: ")
    with grpc.insecure_channel(market_ip) as channel:
        global ip_address, port
        stub = shopping_pb2_grpc.MarketServiceStub(channel)
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add to Wishlist")
        print("4. Rate Item")
        print("5. Quit")
        ip_address = ip_address + ":" + str(port)
        user_input = input("Enter selection: ")
        while user_input != "5":
            if user_input == "1":
                name = input("Enter item name: ")
                if len(name) != 0:
                    category = input("Enter item category: ")
                    search_item_request = shopping_pb2.SearchRequest(itemName=name, category=category)
                    itemlist = stub.SearchItem(search_item_request)
                    for item in itemlist.items:
                        print(f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {item.category}, Description: {item.description}, Quantity Remaining: {item.quantity}, Rating: {item.rating} | Seller: {item.sellerAddress}")
                else:
                    category = input("Enter item category: ")
                    search_item_request = shopping_pb2.SearchRequest(itemName="", category=category)
                    itemlist = stub.SearchItem(search_item_request)
                    for item in itemlist.items:
                        print(f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {item.category}, Description: {item.description}, Quantity Remaining: {item.quantity}, Rating: {item.rating} | Seller: {item.sellerAddress}")           
            elif user_input == "2":
                item_id = int(input("Item ID: "))
                quant = int(input("Quantity: "))
                buy_item_request = shopping_pb2.BuyerRequest(itemName="", category="", itemId=item_id, quantity=quant, buyerAddress=ip_address, buyerUUID="", rating=0)
                status = stub.BuyItem(buy_item_request)
                print(status.message)
            elif user_input == "3":
                item_id = int(input("Item ID: "))
                wishlist_request = shopping_pb2.BuyerRequest(itemName="", category="", itemId=item_id, quantity=0, buyerAddress=ip_address, buyerUUID="", rating=0)
                status = stub.AddToWishlist(wishlist_request)
                print(status.message)
            elif user_input == "4":
                item_id = int(input("Item ID: "))
                rating = int(input("Enter rating: "))
                rate_item_request = shopping_pb2.BuyerRequest(itemName="", category="", itemId=item_id, quantity=0, buyerAddress=ip_address, buyerUUID="", rating=rating)
                status = stub.RateItem(rate_item_request)
                print(status.message)
            elif user_input == "5":
                break
            print("1. Search Item")
            print("2. Buy Item")
            print("3. Add to Wishlist")
            print("4. Rate Item")
            print("5. Quit")
            user_input = input("Enter selection: ")
        return 0

if __name__ == '__main__':
    serve_thread = threading.Thread(target=serve)
    serve_thread.start()
    run()
