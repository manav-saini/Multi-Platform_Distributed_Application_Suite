import grpc
from concurrent.futures import ThreadPoolExecutor
import shopping_pb2
import shopping_pb2_grpc

class MarketServicer(shopping_pb2_grpc.MarketServiceServicer):
    def __init__(self):
        self.sellers = []
        self.items = []
        self.buyers_wishlist = {}
        self.items_buyers_rating = {}

    def RegisterSeller(self, request, context):
        print(f"Seller join request from {request.address}, uuid = {request.uuid}")
        for seller in self.sellers:
            if seller.address == request.address:
                self.buyers_wishlist[seller.address]=[]
                return shopping_pb2.Notification(message="FAILED: Seller already registered with this address")
        self.sellers.append(shopping_pb2.SellerRequest(address=request.address, uuid=request.uuid))
        print(self.sellers)
        self.buyers_wishlist[request.address] = []
        return shopping_pb2.Notification(message="SUCCESS")

    def SellItem(self, request, context):
        print(f"Sell Item request from {request.sellerAddress}")
        for seller in self.sellers:
            if seller.address == request.sellerAddress and seller.uuid == request.sellerUUID:
                item_id = len(self.items) + 1
                new_item = shopping_pb2.Item(id=int(item_id), name=request.name, category=request.category, quantity=int(request.quantity),
                                              description=request.description, sellerAddress=request.sellerAddress, sellerUUID=request.sellerUUID,
                                              price=float(request.price))
                self.items.append(new_item)
                self.items_buyers_rating[item_id]={}
                print(self.items)
                return shopping_pb2.Notification(message=f"SUCCESS: Item added with ID {item_id}")
        return shopping_pb2.Notification(message="FAILED: Invalid seller credentials")

    def UpdateItem(self, request, context):
        print(f"Update Item {request.id} request from {request.sellerAddress}")
        for seller in self.sellers:
            if seller.address == request.sellerAddress and seller.uuid == request.sellerUUID:
                for item in self.items:
                    if item.id == request.id:
                        name = item.name
                        id = request.id
                        category = item.category
                        quantity = request.quantity
                        description = item.description
                        sellerAddress = request.sellerAddress
                        sellerUUID = request.sellerUUID
                        price = request.price
                        updated_item = shopping_pb2.Item(id=int(id), name=name, category=category, quantity=int(quantity),
                                              description=description, sellerAddress=sellerAddress, sellerUUID=sellerUUID,
                                              price=float(price))
                        self.items.remove(item)
                        self.items.append(updated_item)
                        self.notify_buyers(updated_item)
                        return shopping_pb2.Notification(message=f"SUCCESS: Item {request.id} updated")
                return shopping_pb2.Notification(message=f"FAILED: Item {request.id} not found")

        return shopping_pb2.Notification(message="FAILED: Invalid seller credentials")

    def DeleteItem(self, request, context):
        print(f"Delete Item {request.id} request from {request.sellerAddress}")
        for seller in self.sellers:
            if seller.address == request.sellerAddress and seller.uuid == request.sellerUUID:
                for item in self.items:
                    if item.id == request.id:
                        self.items.remove(item)
                        return shopping_pb2.Notification(message=f"SUCCESS: Item {request.id} deleted")
                return shopping_pb2.Notification(message=f"FAILED: Item {request.id} not found")

        return shopping_pb2.Notification(message="FAILED: Invalid seller credentials")

    def DisplaySellerItems(self, request, context):
        print(f"Display Items request from {request.address}")
        seller_items = [item for item in self.items if item.sellerAddress == request.address]
        return shopping_pb2.ItemList(items=seller_items)

    def notify_buyers(self, updated_item):
        for buyer_address, wishlist in self.buyers_wishlist.items():
            if updated_item.id in wishlist:
                buyer_channel = grpc.insecure_channel(buyer_address)
                buyer_stub = shopping_pb2_grpc.BuyerServiceStub(buyer_channel)
                notification = shopping_pb2.Notification(message=f"\n\nThe Following Item has been updated:\n\n{updated_item}\n\n")
                buyer_stub.NotifyClient(notification)
    
    def SearchItem(self, request, context):
        print(f"Search request for Item name: {request.itemName}, Category: {request.category}")
        # Add your logic for searching items based on the request
        if request.itemName !="":
            seller_items = [item for item in self.items if item.name == request.itemName]
            return shopping_pb2.ItemList(items=seller_items)
        else:
            return shopping_pb2.ItemList(self.items)
    
    def BuyItem(self, request, context):
        print(f"Buy request {request.quantity} of item {request.itemId}, from {request.buyerAddress}")
        for items in self.items:
            if items.id == request.itemId:
                quant = items.quantity-request.quantity
                if quant>0:
                    items.quantity = items.quantity-request.quantity
                    return shopping_pb2.Notification(message="SUCCESS: Item purchased")
        return shopping_pb2.Notification(message="FAIL")
    
    def AddToWishlist(self, request, context):
        print(f"Wishlist request of item {request.itemId}, from {request.buyerAddress}")
        self.buyers_wishlist[request.buyerAddress].append(request.itemId)
        return shopping_pb2.Notification(message="SUCCESS: Item added to wishlist")
    
    def RateItem(self, request, context):
        print(f"{request.buyerAddress} rated item {request.itemId} with {request.rating} stars.")
        if request.buyerAddress not in self.items_buyers_rating[request.item_id]:
            self.items_buyers_rating[request.item_id][request.buyerAddress] = request.rating
        return shopping_pb2.Notification(message=f"SUCCESS: Item {request.itemId} rated with {request.rating} stars.")
    

def serve():
    server = grpc.server(ThreadPoolExecutor())
    shopping_pb2_grpc.add_MarketServiceServicer_to_server(MarketServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Market server running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
