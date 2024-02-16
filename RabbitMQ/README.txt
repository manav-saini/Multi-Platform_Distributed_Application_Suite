YOUTUBE SERVER:
Initialisation:
-Connection Setup: 
Establishes a connection to the RabbitMQ server running on 'localhost'. This is done using pika.BlockingConnection which is 
a synchronous connection method to RabbitMQ.
-Channel Creation: 
Creates a channel on the established connection. Channels are where most of the API for getting things done resides.
-Queue Declaration: 
Declares three queues named 'user_requests', 'youtuber_requests', and 'notifications'. 
Declaring a queue ensures it exists; if it already exists, this operation has no effect. 
These queues are used to handle different types of messages: user subscription actions, YouTuber video upload actions, and notifications to users, respectively.
-User Subscriptions Dictionary: 
Initializes an empty dictionary self.user_subscriptions to keep track of user subscriptions to different YouTubers.

consume_user_requests:
This method is a callback function for consuming messages from the 'user_requests' queue. 
It processes messages related to user actions such as subscribing or unsubscribing to YouTubers.

consume_youtuber_requests Method
This method is a callback function for consuming messages from the 'youtuber_requests' queue. 
It processes messages related to YouTubers uploading new videos.

notify_users Method
This method sends notifications to users who are subscribed to a YouTuber when a new video is uploaded.

start_consuming: 
Enters a loop that waits for messages from the queues and processes them using the registered callback functions. 
This runs indefinitely until interrupted (e.g., via CTRL+C).

TO RUN: python YoutubeServer.py

YOUTUBER:

Class Initialization:
Credentials Setup: 
Sets up the credentials for RabbitMQ using pika.PlainCredentials, where 'nj246' is used as both the username and password. 
This is important for RabbitMQ servers that require authentication.
Connection Setup: 
Establishes a connection to the RabbitMQ server located at the given host address using the specified credentials. 
This is done using pika.BlockingConnection, which is a synchronous connection method to RabbitMQ.
Channel Creation: 
Creates a channel on the established connection. In RabbitMQ, channels are virtual connections inside a connection and are where most of the API for getting things done resides.

publish_video:
This method allows a Youtuber to publish a video by sending a message to the 'youtuber_requests' queue.

TO RUN: python Youtuber.py "YoutuberName" "VideoName"

USER:
Class Initialization:
Credentials and Connection: 
Establishes a connection to the RabbitMQ server at the specified host ('34.28.175.156') using pika.PlainCredentials with the provided username ('nj26') and password ('nj246'). 
This connection is established using pika.BlockingConnection, which provides a synchronous way to interact with RabbitMQ.
User Information: 
Stores the user_name provided during the instantiation of the class.
Channel Setup: 
Creates a channel on the established connection, which is used to perform most RabbitMQ operations like declaring queues or publishing messages.
Queue Declaration: 
Declares two queues, 'user_requests' and 'notifications'. The 'user_requests' queue is used for sending subscription updates, and the 'notifications' queue is for receiving video upload notifications.

update_subscription:
This method allows the user to subscribe or unsubscribe from a Youtuber's channel.

receive_notifications:
This is a callback function that handles incoming notifications from the 'notifications' queue.

TO RUN:
python User.py UserName s YoutuberName
or
python User.py UserName