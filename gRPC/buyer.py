import grpc
from concurrent.futures import ThreadPoolExecutor
import shopping_pb2
import shopping_pb2_grpc
import random

class BuyerServicer(shopping_pb2_grpc.BuyerServiceServicer):
    def NotifyClient(self, request, context):
        print(request.message)

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = shopping_pb2_grpc.MarketServiceStub(channel)
        print("1. Search Item")
        print("2. Buy Item")
        print("3. Add to Wishlist")
        print("4. Rate Item")
        print("5. Quit")
        ip_address = "192.168.29.25"
        port = random.randint(5001,5999)
        ip_address = ip_address+":"+str(port) 
        user_input = input("Enter selection: ")
        while user_input!="5":
            if user_input == "1":
                name = input("Enter item name: ")
                if len(name) != 0:
                    category = input("Enter item category: ")
                    search_item_request = shopping_pb2.SearchRequest(itemName=name, category=category)
                    itemlist = stub.SearchItem(search_item_request)
                    for item in itemlist.items:
                        print(f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {item.category}, Description: {item.description}, Quantity Remaining: {item.quantity}, Rating: {item.rating} | Seller: {item.sellerAddress}")
                    # print(f"""Item ID: {itemlist.Item.id}, Name: {itemlist.Item.name},Category: {itemlist.Item.category},
                    #       Description: {itemlist.Item.description},
                    #       Quantity Remaining: {itemlist.Item.quantity},
                    #       Rating: {itemlist.Item.rating} / 5 | Seller: {itemlist.Item.sellerAddress}""")
            elif user_input == "2":
                item_id = input("Item ID: ")
                quant = input("Quantity: ")
                buy_item_request = shopping_pb2.BuyerRequest(itemName="", category="", itemId=item_id, quantity=quant, buyerAddress=ip_address, buyerUUID="", rating=0)
                status = stub.BuyItem(buy_item_request)
                print(status.message)

            elif user_input == "3":
                item_id = input("Item ID: ")
                wishlist_request = shopping_pb2.BuyerRequest(itemName="", category="", itemId=item_id, quantity=0, buyerAddress=ip_address, buyerUUID="", rating=0)
                status = stub.AddToWishlist(wishlist_request)
                print(status.message)

            elif user_input == "4":
                item_id = input("Item ID: ")
                rate_item_request = shopping_pb2.BuyerRequest(itemName="", category="", itemId=item_id, quantity=0, buyerAddress=ip_address, buyerUUID="", rating=0)
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
    run()
