import pika
import sys
import json

class User:
    def __init__(self, user_name):
        self.user_name = user_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='notifications')

    def update_subscription(self, youtuber_name, subscribe):
        request = {
            "user": self.user_name,
            "youtuber": youtuber_name,
            "subscribe": subscribe
        }
        message = json.dumps(request)
        self.channel.basic_publish(exchange='', routing_key='user_requests', body=message)
        action = "subscribed" if subscribe else "unsubscribed"
        print(f"SUCCESS: {self.user_name} {action} to {youtuber_name}")

    def receive_notifications(self, ch, method, properties, body):
        notification = body.decode('utf-8')
        print(f"New Notification: {notification}")

    def start_consuming(self):
        self.channel.basic_consume(queue='notifications', on_message_callback=self.receive_notifications, auto_ack=True)
        print(f"{self.user_name} is now receiving notifications.")
        self.channel.start_consuming()

if __name__ == '__main__':
    user_name = sys.argv[1]

    if len(sys.argv) == 4:
        action = sys.argv[2].lower()
        youtuber_name = sys.argv[3]
        subscribe = action == 's'
        user = User(user_name)
        user.update_subscription(youtuber_name, subscribe)
        user.start_consuming()
    elif len(sys.argv) == 2:
        user = User(user_name)
        user.start_consuming()
    else:
        print("Usage: User.py <UserName> [s/u <YoutuberName>]")
        sys.exit(1)