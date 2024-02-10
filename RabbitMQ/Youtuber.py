import pika
import sys
import json

class Youtuber:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()

    def publish_video(self, youtuber_name, video_name):
        request = {
            "youtuber": youtuber_name,
            "videoName": video_name
        }

        message = json.dumps(request)
        self.channel.basic_publish(exchange='', routing_key='youtuber_requests', body=message)
        print(f"Published Video: {youtuber_name} uploaded {video_name}")
        self.connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)

    youtuber_name = sys.argv[1]
    video_name = sys.argv[2]

    youtuber = Youtuber()
    youtuber.publish_video(youtuber_name, video_name)
