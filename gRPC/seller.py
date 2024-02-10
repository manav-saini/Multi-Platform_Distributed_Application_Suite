import grpc
import shopping_pb2
import shopping_pb2_grpc
import random
import uuid

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = shopping_pb2_grpc.MarketServiceStub(channel)
        print("1. Register Seller")
        print("2. Sell Item")
        print("3. Update Item")
        print("4. Delete Item")
        print("5. Display Seller Items")
        print("6. Stop Service")
        ip_address = "192.168.29.25"
        port = random.randint(5001,5999)
        ip_address = ip_address+":"+str(port) 
        user_input = input("Enter selection: ")
        unique_id=""
        while(user_input!=6):
            if user_input == "1":
                unique_id = str(uuid.uuid1())
                register_request = shopping_pb2.SellerRequest(address=ip_address, uuid=unique_id)
                response = stub.RegisterSeller(register_request)
                print(response.message)
            elif user_input == "2":
                item_name = input("Item Name: ")
                item_category = input("Category: ")
                item_quant = input("Quantity: ")
                item_description = input("Description: ")
                item_price = input("Price: ")
                item = shopping_pb2.Item(name=item_name, category=item_category, quantity=int(item_quant), description=item_description, sellerAddress=ip_address, sellerUUID=unique_id, price=float(item_price))
                response = stub.SellItem(item)
                print(response.message)
            elif user_input == "3":
                item_id = input("Item ID: ")
                item_quant = input("Quantity: ")
                item_price = input("Price: ")
                updated_item = shopping_pb2.Item(id=int(item_id), price=float(item_price), quantity=int(item_quant), sellerAddress=ip_address, sellerUUID=unique_id)
                response = stub.UpdateItem(updated_item)
                print(response.message)
            elif user_input == "4":
                item_id = input("Item ID: ")
                item_to_delete = shopping_pb2.Item(id=int(item_id), sellerAddress=ip_address, sellerUUID=unique_id)
                response = stub.DeleteItem(item_to_delete)
                print(response.message)
            elif user_input == "5":
                seller_info = shopping_pb2.SellerRequest(address=ip_address, uuid=unique_id)
                response = stub.DisplaySellerItems(seller_info)
                for item in response.items:
                    print(f"Item ID: {item.id}, Price: ${item.price}, Name: {item.name}, Category: {item.category}, Description: {item.description}, Quantity Remaining: {item.quantity} | Seller: {item.sellerAddress}")
            elif user_input == "6":
                break
            print("1. Register Seller")
            print("2. Sell Item")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. Display Seller Items")
            print("6. Stop Service")
            user_input = input("Enter selection: ")

        return 0

if __name__ == '__main__':
    run()