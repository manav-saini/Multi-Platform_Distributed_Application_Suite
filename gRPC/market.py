import grpc
from concurrent.futures import ThreadPoolExecutor
import shopping_pb2
import shopping_pb2_grpc
import random

class MarketServicer(shopping_pb2_grpc.MarketServiceServicer):
    def __init__(self):
        self.sellers = []
        self.items = []
        self.buyers_wishlist = {}
        self.items_buyers_rating = {}
        self.items_seller = {}

    def RegisterSeller(self, request, context):
        print(f"Seller join request from {request.address}, uuid = {request.uuid}")
        for seller in self.sellers:
            if seller.address == request.address:
                return shopping_pb2.Notification(message="FAILED: Seller already registered with this address")
        self.sellers.append(shopping_pb2.SellerRequest(address=request.address, uuid=request.uuid))
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
                self.items_seller[item_id] = request.sellerAddress
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
                        rating = item.rating
                        updated_item = shopping_pb2.Item(id=int(id), name=name, category=category, quantity=int(quantity),
                                              description=description, sellerAddress=sellerAddress, sellerUUID=sellerUUID,
                                              price=float(price),rating=rating)
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

    def notify_seller(self, item):
        print(self.items_seller)
        seller_address = self.items_seller[item.id]
        seller_channel = grpc.insecure_channel(seller_address)
        seller_stub = shopping_pb2_grpc.SellerServiceStub(seller_channel)
        response = seller_stub.NotifyClient(item)
        
    def notify_buyers(self, updated_item):
        for buyer_address in self.buyers_wishlist:
            wishlist = self.buyers_wishlist[buyer_address]
            if updated_item.id in wishlist:
                print(buyer_address)
                buyer_channel = grpc.insecure_channel(buyer_address)
                buyer_stub = shopping_pb2_grpc.BuyerServiceStub(buyer_channel)
                response = buyer_stub.NotifyClient(updated_item)
    
    def SearchItem(self, request, context):
        if len(request.itemName)!=0:
            print(f"Search request for Item name: {request.itemName}, Category: {request.category}")
            seller_items = [item for item in self.items if item.name == request.itemName]
            return shopping_pb2.ItemList(items=seller_items)
        elif request.category.upper()=="ANY":
            print(f"Search request for Category: {request.category}")
            seller_items = [item for item in self.items]
            return shopping_pb2.ItemList(items=seller_items)
        else:
            print(f"Search request for Category: {request.category}")
            seller_items = [item for item in self.items if item.category == request.category]
            return shopping_pb2.ItemList(items=seller_items)
    
    def BuyItem(self, request, context):
        print(f"Buy request {request.quantity} of item {request.itemId}, from {request.buyerAddress}")
        for items in self.items:
            if items.id == request.itemId:
                quant = items.quantity-request.quantity
                if quant>0:
                    items.quantity = items.quantity-request.quantity
                    self.notify_seller(items)
                    return shopping_pb2.Notification(message="SUCCESS: Item purchased")
        return shopping_pb2.Notification(message="FAIL")
    
    def AddToWishlist(self, request, context):
        print(f"Wishlist request of item {request.itemId}, from {request.buyerAddress}")
        if request.buyerAddress not in self.buyers_wishlist:
            self.buyers_wishlist[request.buyerAddress] = []
        wishlist = self.buyers_wishlist[request.buyerAddress]
        if request.itemId in wishlist:
            return shopping_pb2.Notification(message="Item already in wishlist")
        wishlist.append(request.itemId)
        self.buyers_wishlist[request.buyerAddress] = wishlist
        return shopping_pb2.Notification(message="SUCCESS: Item added to wishlist")
    
    def RateItem(self, request, context):
        print(f"{request.buyerAddress} rated item {request.itemId} with {request.rating} stars.")
        if request.buyerAddress not in self.items_buyers_rating[request.itemId]:
            self.items_buyers_rating[request.itemId][request.buyerAddress] = request.rating
            for item in self.items:
                if item.id==request.itemId:
                    print(self.items_buyers_rating[request.itemId])
                    sum_rating = sum(list(self.items_buyers_rating[request.itemId].values()))
                    item.rating = sum_rating/len(self.items_buyers_rating[request.itemId])
        return shopping_pb2.Notification(message=f"SUCCESS: Item {request.itemId} rated with {request.rating} stars.")
    

def serve():
    port = str(random.randint(5001, 5999))
    server = grpc.server(ThreadPoolExecutor())
    shopping_pb2_grpc.add_MarketServiceServicer_to_server(MarketServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Market server running on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
