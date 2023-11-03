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

def main():
    functions_names = [register_device_menu]
        #, device_to_sense_menu, show_all_sensed_data, exit_menu]
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
