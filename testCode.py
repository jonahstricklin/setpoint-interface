import time
from opcua import Client, ua

# OPC UA Server Details
opcua_url = "opc.tcp://192.168.1.100:4990/FactoryTalkLinxGateway1"
setpoint_tag_id = "ns=14;s=TagGroup01#[HTS_CTRL]HTS_CRTL_Data_From_HMI.SystemState"  
#cur_temp_tag = "ns=13;s=TagGroup03#[HTS_CTRL]HTS_CRTL_Data_From_HMI.PiConfirmation"

# Create OPC UA Client instance
client = Client(opcua_url)

try:
    print("Connecting to OPC UA Server...")
    client.connect()
    print("Connected to FactoryTalk Linx Gateway OPC UA Server")
    tag_node = client.get_node(setpoint_tag_id)
    
    input("proceed to loop...")
    while True:
        value = int(input("type an integer: "))
        tag_node.set_value(ua.Variant(value))
        #server_value = tag_node.get_value()
        #print(server_value)
        time.sleep(0.1)
    
except KeyboardInterrupt:
    print("\nStopping...")

except Exception as e:
    print("Error:", e)

finally:
    try:
        client.disconnect()
        print("Disconnected from OPC UA Server.")
    except Exception as e:
        print("Error disconnecting:", e)