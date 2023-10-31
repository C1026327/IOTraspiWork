from datetime import datetime as dt 
from sense_hat import SenseHat 
import random
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, DateTime, Double
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# class Device(Base):
#     __tablename__ = 'devices'
#     id = Column(Integer, primary_key = True, index = True)
#     tag = Column(Unicode(40), nullable = False)
#     status = Column(String, nullable = False)
#     version = Column(Integer, nullable = False)
#     lastUpdated = Column(DateTime, nullable = False)

# def __init__(self, deviceID, tag, status, version, lastUpdated):
#     self.deviceID=deviceID
#     self.tag=tag
#     self.status=status
#     self.version=version
#     self.lastUpdated=lastUpdated


class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, index=True)      # Device ID
    tag = Column(Unicode(40), nullable=False) # unique=True # Device Name/Tag
    status = Column(String, nullable=False)                 # Status (enabled/disabled - set in main method )
    version = Column(Integer, nullable=False)               # Version (eg: 1.0 - set in main method)
    lastUpdated = Column(DateTime, nullable=False)          # When Device was reistered

    # Constructor (used to assign values to the class attributes)
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

if __name__ == "__main__":
    engine = create_engine('sqlite:///iot.db', echo=True)
    Base.metadata.create_all(engine)
    deviceTag=''.join((random.choice('environment') for i in range(5)))
    status="enabled"
    version="1.0"
    # device=Device(deviceTag,status,version,dt.now())
    # device.reg_device(device,engine)
    device = Device(None, deviceTag, status, version, dt.now())  
    device.reg_device(device, engine)
    sense=SenseHat()
    temp=sense.get_temperature()
    temp_sensor=StreamingData(None,10,temp,dt.now(),None)
    temp_sensor.add_data(temp_sensor,engine)
    print(temp)