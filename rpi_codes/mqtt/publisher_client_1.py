import paho.mqtt.client as mqtt

from datetime import datetime
from time import sleep

class Publisher_Client:
    mqtt_broker="mqtt.eclipseprojects.io"
    mqtt_broker_port=1883
    keepalive=60
    mqtt_client=None
    data_context=None
    connection_rc_flag=None
    
    def __init__(self, client_device, location, data_context):
        self.publisher_client_device=client_device
        self.publisher_client_location=location
        self.data_context=data_context

    def mydatetime(self):
        return datetime.now().strftime("%Y.%m.%d %H%M%S")
    
    def on_connect(self,client,userdata, flags, rc):
        print(self.mydatetime()," :  result code "+str(rc))
        self.connection_rc_flag=rc
        sleep(10)

    def event_publish(self,data):
        self.mqtt_client.publish(self.data_context,data)
        sleep(3)
        print(self.mydatetime(), ": Message published!")

if __name__ == '__main__':
    device = input("Please enter the name of the device:  ")
    topic = "aslam/house/r1/s1"
    data = "Hello from publisher"
    location = input("The location of the subscriber (i.e. postcode, city) : ")
    pc = Publisher_Client(device,location,topic)
    pc.mqtt_client=mqtt.Client()
    pc.mqtt_client.on_connect = pc.on_connect
    pc.mqtt_client.connect(pc.mqtt_broker, pc.mqtt_broker_port)
    pc.event_publish(data)
