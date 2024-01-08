# Library
import asyncio
from azure.iot.device import IoTHubSession
import time
# import constant
from sense_hat import SenseHat
# Constants - N/A NO CONSTANT FILE
CONNECTION_STRING_TEMP = ''
# DATA_TO_CLOUD = True

# async def send_data_to_Azure(connection_string, data_to_send):
#     sense=SenseHat()
#     try:
#         print("Connecting to IoT Hub...")
#         async with IoTHubSession.from_connection_string(connection_string) as session
#         if(session.connected):
#             print("Connected successfully with device ID: ", session.device_id)
#             print("Data transmission started...")
#         else:
#             print("Could not connect with the desired device.")
#             return;
#         await session.send_message(data_to_send)
#         print("Transmission Complete")
#         sense.set_pixels(constant.smiley_face)
#         await asyncio.sleep(5)
#         sense.clear

#     except Exception:
#         # Connection has been lost.
#         print("Dropped Connection. Exiting.")
#     finally:
#         sense.clear()

def cloud_messages_receiving_service():
    asyncio.run(data_from_clouds())

async def data_from_clouds():
    print("This is the cloud to device data receiving menu \n")
    time.sleep(3)
    device_connection=
    print("Starting Messaging from cloud service...")
    try:
        print("Press CTRL + C to exit.")
        async with IoTHubSession.from_connection_string(device_connection) as session:
            print("Waiting for cloud device: {0} messages ".format(session.device_id))
            async for message_from_clouds in message_from_clouds:
                print("The Data in the Message Recieved is: {0}".format(message_from_clouds.payload))
                print("The Custom Properties are {0}".format(message_from_clouds.custom_properties))
                sense=SenseHat()
                sense.clear()
                sense.show_message("%.1f "% message_from_clouds.payload, scroll_speed=0.1, text_colour = [200,0,0])
                time.sleep(3)

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
        return
    
    except KeyboardInterrupt:
        print("IoT Hub C2D Messaging Service: Stopped.")

cloud_messages_receiving_service()