import pika
import json

class YoutubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='youtuber_requests')
        self.channel.queue_declare(queue='notifications')

        # Dynamic dictionary to store user subscriptions
        self.user_subscriptions = {}

    def consume_user_requests(self, ch, method, properties, body):
        user_request = json.loads(body)
        user_name = user_request["user"]

        if "subscribe" in user_request:
            action = "subscribed" if user_request["subscribe"] else "unsubscribed"
            youtuber_name = user_request["youtuber"]

            if user_name not in self.user_subscriptions:
                self.user_subscriptions[user_name] = []

            if action == "subscribed" and youtuber_name not in self.user_subscriptions[user_name]:
                self.user_subscriptions[user_name].append(youtuber_name)
            elif action == "unsubscribed" and youtuber_name in self.user_subscriptions[user_name]:
                self.user_subscriptions[user_name].remove(youtuber_name)

            print(f"{user_name} {action} to {youtuber_name}")

        else:
            print(f"{user_name} logged in")

    def consume_youtuber_requests(self, ch, method, properties, body):
        youtuber_request = json.loads(body)
        youtuber_name = youtuber_request["youtuber"]
        video_name = youtuber_request["videoName"]
        print(f"{youtuber_name} uploaded {video_name}")
        self.notify_users(youtuber_name, video_name)

    def notify_users(self, youtuber_name, video_name):
        # Send notifications to all users subscribed to the given YouTuber
        for user, subscriptions in self.user_subscriptions.items():
            if youtuber_name in subscriptions:
                notification = f"{youtuber_name} uploaded a new video: {video_name}"
                self.channel.basic_publish(exchange='', routing_key='notifications', body=notification)
                print(f"Notification sent to {user}: {notification}")

    def start_consuming(self):
        self.channel.basic_consume(queue='user_requests', on_message_callback=self.consume_user_requests, auto_ack=True)
        self.channel.basic_consume(queue='youtuber_requests', on_message_callback=self.consume_youtuber_requests, auto_ack=True)
        print('Server is waiting for requests. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    server = YoutubeServer()
    server.start_consuming()