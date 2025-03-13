
from opcua import Client, ua


# OPC UA Server Details
opcua_url = "opc.tcp://192.168.1.100:4990/FactoryTalkLinxGateway"
tag_node_id = "ns=13;s=TagGroup03#[HTS_CTRL]HTS_CRTL_Data_From_HMI.PiConfirmation"
tag_node_id_ret = "ns=13;s=TagGroup03#[HTS_CTRL]HTS_CRTL_Data_From_HMI.SystemState"
tag_node_id_ret1 = "ns=13;s=TagGroup03#[HTS_CTRL]HTS_CRTL_Data_From_HMI.SystemState"


# Create OPC UA Client instance
client = Client(opcua_url)

try:
    print("Connecting to OPC UA Server...")
    client.connect()
    print("Connected to FactoryTalk Linx Gateway OPC UA Server")

    # Get reference to the tag node
    tag_node = client.get_node(tag_node_id)
    sys_st = client.get_node(tag_node_id_ret)
    sys_st1 = client.get_node(tag_node_id_ret1)

    print("Monitoring button state and syncing with OPC UA tag. Press Ctrl+C to exit.")

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
# import client module
# establish opcua url
# call tag node id's
# create opcua client instance
# connect to client
# the way you read/write tag data is "tag_node.get_value" / "tag_node.set_value"