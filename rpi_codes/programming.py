import random
from datetime import datetime as dt
from time import sleep

from sense_hat import SenseHat
from sqlalchemy import create_engine
from sqlalchemy import (Column, DateTime, Double, ForeignKey, Integer, String, Unicode)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

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

def show_menu(menu):
    for i, function in menu.items():
        print(i,function.__name__)

def register_device_menu():
    print("\n This is the device registration menu.")
    deviceTag=input("Please enter the tag for a device: ")
    status = input("Please enter the status of the device: ")
    version = input("Please enter the device version: ")
    device = Device(None,deviceTag,status,version,dt.now())
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
        streamingData=StreamingData(None, idForDevice, pressure_sensor,dt.now(),None)
        streamingData.add_data(streamingData,engine)
        print("Pressure: %s Millibars" % pressure_sensor)
        sense.clear()
        sense.show_message("%sMillibars" % pressure_sensor, scroll_speed=0.2, text_colour=[0,0,255])
        sleep(3)
        sense.clear()

    elif to_sense=="T":
        temperature_sensor = round(sense.get_temperature(),2)
        streamingData2 = StreamingData(None,idForDevice, temperature_sensor,dt.now(), None)
        streamingData2.add_data(streamingData2, engine)
        print("Temperature: %s C" % temperature_sensor)
        sense.clear()
        sense.show_message("%.1f C" % temperature_sensor, scroll_speed=0.1, text_colour=[255,0,255])
        sleep(3)
        sense.clear()

    elif to_sense == "H":
        humidity_sensor = round(sense.get_humidity(),2)
        streamingData2 = StreamingData(None,idForDevice, humidity_sensor,dt.now(), None)
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
        streamingData3=StreamingData(None, idForDevice, round(x,2), dt.now(), None)
        streamingData3.add_data(streamingData3,engine)
        print("x={0}, y={1}, z={2}".format(x, y, z))
        sense.clear()
        sense.show_message("x={0}, y={1}, z={2}".format(x, y, z), scroll_speed=0.1, text_colour=[255,130,130])
    
    else:
        print("something else")

def exit_menu():
    exit()

def main():
    functions_names = [register_device_menu, device_to_sense_menu, exit_menu] #, show_all_sensed_data
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
#     deviceTag=''.join((random.choice('environment') for i in range(5)))
#     status="enabled"
#     version="1.0"
#     device=Device(None,deviceTag,status,version,dt.now())
#     device.reg_device(device,engine)
#     sense=SenseHat()
#     temp=sense.get_temperature()
#     temp_sensor=StreamingData(None,10,temp,dt.now(),None)
#     temp_sensor.add_data(temp_sensor,engine)
#     print(temp)
