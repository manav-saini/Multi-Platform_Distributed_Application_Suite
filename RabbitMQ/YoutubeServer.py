import pika
import json

class YoutubeServer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='youtuber_requests')
        self.channel.queue_declare(queue='notifications')

    def consume_user_requests(self, ch, method, properties, body):
        user_request = json.loads(body)
        user_name = user_request["user"]
        if "subscribe" in user_request:
            action = "subscribed" if user_request["subscribe"] else "unsubscribed"
            youtuber_name = user_request["youtuber"]
            print(f"{user_name} {action} to {youtuber_name}")
        else:
            print(f"{user_name} logged in")

    def consume_youtuber_requests(self, ch, method, properties, body):
        youtuber_request = json.loads(body)
        youtuber_name = youtuber_request["youtuber"]
        video_name = youtuber_request["videoName"]
        print(f"{youtuber_name} uploaded {video_name}")

    def notify_users(self):
        # Assuming you have a data structure to keep track of user subscriptions and their corresponding YouTubers
        user_subscriptions = {
            "user1": ["youtuber1", "youtuber2"],
            "user2": ["youtuber1", "youtuber3"]
            # Add more users and subscriptions as needed
        }

        # Simulating notifications for demonstration purposes
        for user, subscribed_youtubers in user_subscriptions.items():
            for youtuber in subscribed_youtubers:
                notification = f"{youtuber} uploaded a new video!"
                self.channel.basic_publish(exchange='', routing_key='notifications', body=notification)
                print(f"Notification sent to {user}: {notification}")

    def start_consuming(self):
        self.channel.basic_consume(queue='user_requests', on_message_callback=self.consume_user_requests, auto_ack=True)
        self.channel.basic_consume(queue='youtuber_requests', on_message_callback=self.consume_youtuber_requests, auto_ack=True)
        self.notify_users()
        print('Server is waiting for requests. To exit press CTRL+C')
        self.channel.start_consuming()

if __name__ == '__main__':
    server = YoutubeServer()
    server.start_consuming()
