import paho.mqtt.client as mqtt

from datetime import datetime
from time import sleep

class Subscriber_Client:
    mqtt_broker="mqtt.eclipseprojects.io"
    mqtt_broker_port=1883
    keepalive=60
    mqtt_client=None
    topic_interested=None
    def __init__(self, client_name, location, topic_interested):
        self.subscriber_client_name=client_name
        self.subscriber_client_location=location
        self.topic_interested=topic_interested

    def mydatetime(self):
        return datetime.now().strftime("%Y.%m.%d %H%M%S")
    
    def on_connect(self,client,userdata,flags,rc):
        print(self.mydatetime(),": result code "+str(rc))
        self.mqtt_client.subscribe(self.topic_interested)
        print(self.mydatetime(),": Subscription completed, Waiting for message....")
        sleep(10)

    def on_message(self, client, userdata, msg):
        print(self.mydatetime(), ":", msg.topic+ " : "+ str(msg.payload))

if __name__ == '__main__':
    name = input("Please enter the name of the subscriber client: ")
    topic = "aslam/house/r1/s1"
    location = input ("The location of the subscriber (i.e. postcode, city): ") #"Sheffield"
    cc = Subscriber_Client(name,location,topic)
    cc.mqtt_client=mqtt.Client()
    cc.mqtt_client.on_connect = cc.on_connect
    cc.mqtt_client.on_message = cc.on_message
    cc.mqtt_client.connect(cc.mqtt_broker, cc.mqtt_broker_port, cc.keepalive)
    cc.mqtt_client.loop_forever()