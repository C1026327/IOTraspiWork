##################################################################################

# base library
import random
from datetime import datetime
from time import sleep

# sense & sqlalchemy functionality
from sense_hat import SenseHat
from sqlalchemy import create_engine
from sqlalchemy import (Column, DateTime, Double, ForeignKey, Integer, String, Unicode)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# mqtt
import paho.mqtt.client as mqtt

# crypto  -  block chain / encryption libraries
from ast import Dict
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii
from datetime import datetime
import collections
import hashlib
from Crypto.Hash import SHA256
# from blockchainUtill import *
import base64,json
from flask import Flask, jsonify, request #sudo apt-get install python3-flask

##################################################################################

# Pre Definitives
Base = declarative_base()

def sha256(message):
    return hashlib.sha256(message.encode('ascii')).hexdigest()


class IoTNodeTransaction:
    def __init__(self, source, destination, data):
        self.data = data
        self.source = source
        self.destination = destination
        self.timestamp = datetime.now()

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key = True, index = True)
    tag = Column(Unicode(40), nullable = False)
    status = Column(String, nullable = False)
    version = Column(Integer, nullable = False)
    lastUpdated = Column(DateTime, nullable = False)

    def __init__(self, deviceID, tag, status, version, lastUpdated):
        self.deviceID=deviceID
        self.tag=tag
        self.status=status
        self.version=version
        self.lastUpdated=lastUpdated
        
    def reg_device(self,device,engine):
        Session = sessionmaker(engine)
        with Session() as session:
            session.add(device)
            session.commit()

class StreamingData(Base):
    __tablename__ = 'streaming_data'
    id = Column(Integer, primary_key=True, index=True)
    data = Column(Double,nullable=False)
    sensingTime = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, default=func.now())

    def __init__(self,id,deviceId,data,sensingTime,timestamp):
        self.id = id
        self.data=data
        self.deviceId=deviceId
        self.sensingTime=sensingTime
        self.timestamp=timestamp

    def add_data(self,data_metadata,engine):
        Session=sessionmaker(engine)
        with Session() as session:
            session.add(data_metadata)
            session.commit()

##################################################################################

# Main Program Start

def show_menu(menu):
    for i, function in menu.items():
        print(i,function.__name__)

def register_device_menu():
    print("\n This is the device registration menu.")
    deviceTag=input("Please enter the tag for a device: ")
    status = input("Please enter the status of the device: ")
    version = input("Please enter the device version: ")
    device = Device(None,deviceTag,status,version,datetime.now())
    device.reg_device(device,engine)
    print ("Your device was registered successfully.\n")

def device_to_sense_menu():
    print("\n This is reading data from a sensor menu")
    print(" P - Sense current pressure: ")
    print(" T - Sense current temperature: ")
    print(" H - Sense current humidity: ")
    print(" A - Sense current momentum: ")
    print(" X - Any other key to exist from sensing menu: ")
    to_sense=input("Input your sensor choice: ")
    idForDevice = input("Input the device id that you have already registered: ")
    sense = SenseHat()

    if to_sense == "P":
        pressure_sensor = round(sense.get_pressure(),2)
        streamingData=StreamingData(None, idForDevice, pressure_sensor,datetime.now(),None)
        streamingData.add_data(streamingData,engine)
        print("Pressure: %s Millibars" % pressure_sensor)
        sense.clear()
        sense.show_message("%sMillibars" % pressure_sensor, scroll_speed=0.2, text_colour=[0,0,255])
        sleep(3)
        sense.clear()

    elif to_sense=="T":
        temperature_sensor = round(sense.get_temperature(),2)
        streamingData2 = StreamingData(None,idForDevice, temperature_sensor,datetime.now(), None)
        streamingData2.add_data(streamingData2, engine)
        print("Temperature: %s C" % temperature_sensor)
        sense.clear()
        sense.show_message("%.1f C" % temperature_sensor, scroll_speed=0.1, text_colour=[255,0,255])
        sleep(3)
        sense.clear()

    elif to_sense == "H":
        humidity_sensor = round(sense.get_humidity(),2)
        streamingData2 = StreamingData(None,idForDevice, humidity_sensor,datetime.now(), None)
        streamingData2.add_data(streamingData2, engine)
        print("Humidity:  ", humidity_sensor)
        sense.clear()
        sense.show_message("%.1f  " % humidity_sensor, scroll_speed=0.1, text_colour=[125,175,255])
        sleep(3)
        sense.clear()

    elif to_sense == "A":
        acceleration=sense.get_accelerometer_raw()
        x = round(acceleration['x'],2)
        y = round(acceleration['y'],2)
        z = round(acceleration['z'],2)
        streamingData3=StreamingData(None, idForDevice, round(x,2), datetime.now(), None)
        streamingData3.add_data(streamingData3,engine)
        print("x={0}, y={1}, z={2}".format(x, y, z))
        sense.clear()
        sense.show_message("x={0}, y={1}, z={2}".format(x, y, z), scroll_speed=0.1, text_colour=[255,130,130])
    
    else:
        print("something else")

def show_all_sensed_data():
    sense=SenseHat()
    temperature_sensor = round(sense.get_temperature(),2)
    pressure_sensor = round(sense.get_pressure(),2)
    acceleration=sense.get_accelerometer_raw()
    x = round(acceleration['x'],2)
    y = round(acceleration['y'],2)
    z = round(acceleration['z'],2)
    humidity_sensor = round(sense.get_humidity(),2)

    print("Pressure: %s Millibars" % pressure_sensor)
    print("Temperature: %s C" % temperature_sensor)
    print("Humidity:  ", humidity_sensor)
    print("Momentum: ","x={0}, y={1}, z={2}".format(x, y, z))
    sleep(10)

def publish_mqtt():
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

def subscribe_mqtt():
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

def blockchain():
    class IoTnode:
    def __init__(self):
        r_value=Random.new().read
        key= RSA.generate(2048,r_value)
        self.publicKey=key.public_key().export_key()
        self.private_key=key.export_key()
        self.hostName=""


class IoTNodeTransaction:
    def __init__(self, source, destination, data):
        self.data = data
        self.source = source
        self.destination = destination
        self.timestamp = datetime.now()


    def encrypt_transaction(self):
        encrypted_transaction=""
        private_key=iot_node.private_key
        file_out = open("private.pem", "wb")
        file_out.write(private_key)
        file_out.close()
        public_key=iot_node.publicKey
        file_out = open("public.pem", "wb")
        file_out.write(public_key)
        file_out.close()
        public_key = RSA.import_key(open("public.pem").read())
        session_key = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(public_key) # Encrypt the Session Key with the public RSA key.
        enc_session_key = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        encoded_dict = str(self.compose_transaction()).encode('utf-8')
        cipherdata = cipher_aes.encrypt(encoded_dict)
        msg_to_sent = {"data": cipherdata,
                       "enc_session_key":enc_session_key,
                       "nonce":cipher_aes.nonce}
        encrypted_transaction=base64.b64encode(str(msg_to_sent).encode('utf-8'))
        return encrypted_transaction
    
    def decrypt_transaction(self,data):
        x=base64.b64decode(data)
        x=x.decode('utf-8')
        x=eval(x)
        data=x.get("data")
        enc_session_key=x.get("enc_session_key")
        nonce=x.get("nonce")
        private_key=RSA.import_key(open("private.pem").read())
        cipher_rsa= PKCS1_OAEP.new(private_key)
        session_key=cipher_rsa.decrypt(enc_session_key)
        cipher_aes=AES.new(session_key, AES.MODE_EAX, nonce)
        data=cipher_aes.decrypt(data)
        return data



    def compose_transaction(self):
        transaction_dic=""
        transaction_dic=collections.OrderedDict({
            "source":self.source,
            "destination":self.destination,
            "data":self.data,
            "timeStamp":self.timestamp
        })
        return transaction_dic


class BlockChain:
    def __init__(self):
        self.v_transactions = []
        self.previous_block_hash=""
        self.Nonce=""
    
    def create_block(self):
        global last_transaction_index,last_block_hash
        temp_transaction=iot_transactions[last_transaction_index]
        self.v_transactions.append(temp_transaction)
        last_transaction_index += 1
        self.previous_block_hash=last_block_hash
        self.Nonce=self.mine(self, 2)
        digest = hash(self)
        blocks.append(self)
        last_block_hash=digest
    
    def mine(self,block,mine_difficulty=1):
        assert mine_difficulty >=1
        prefix = '1' * mine_difficulty
        for c in range(1000):
            digest = sha256(str(hash(block)) + str(c))
            if digest.startswith(prefix):
                print("after " + str(c) + " iterations found nonce:  " + digest)
        return digest
    
    def fetch_blocks(self):
        out=[]
        print("Number of blocks in the chain:  ", len(blocks))
        for i in range (len(blocks)):
            block_temp = blocks[i]
            print ("block # ", i)
            res = {"block # ": i}
        
            for t in block_temp.v_transactions:
                count=0;
                count+=1
                print("Transaction no   ",count)
                res["transaction_no"]=count
                print("IoT source node        : ", iot_node.hostName)
                res["iot_source_node"]=iot_node.hostName





            out.append(res)
        jsonData=json.dumps(out)
        return jsonData
        
    #region Flask
    app = Flask(__name__)

    iot_transactions=[]
    blocks=[]
    last_transaction_index = 0
    last_block_hash=""

    iot_node=IoTnode()
    block= BlockChain()

    @app.route('/send', methods=['GET'])
    def send_encrypt_transaction():
        iot_node.hostName="aj9394@shu.ac.uk"
        humidity=14.0
        t=IoTNodeTransaction(source=iot_node.hostName, destination="IoTServer", data=humidity)
        encrypted_data=t.encrypt_transaction()
        iot_transactions.append(t)
        block.create_block()
        return jsonify(encrypted_data), 200

    @app.route('/list_blocks', methods=['GET'])
    def list_blocks():
        response=block.fetch_blocks()
        return response, 200


    @app.route('/test',methods=['GET'])
    def hello_world():
        msg="Blockchain.py is running on the Flask Framework"
        return jsonify(msg), 200

    app.run(host='127.0.0.1', port=5009)
    #endregion

def exit_menu():
    exit()

def main():
    functions_names = [register_device_menu, device_to_sense_menu, show_all_sensed_data, publish_mqtt, subscribe_mqtt, exit_menu]
    menu_items = dict(enumerate(functions_names, start=1))
    while True:
        show_menu(menu_items)
        selection = int(
            input("Please enter your desired function number: "))
        selected_value = menu_items[selection]
        selected_value()

if __name__ == "__main__":
    engine = create_engine('sqlite:///iot.db', echo=True)
    Base.metadata.create_all(engine)
    main()

##################################################################################