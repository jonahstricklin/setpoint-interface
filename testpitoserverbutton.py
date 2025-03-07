from opcua import Client, ua
import time
import RPi.GPIO as GPIO

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time

lcd_columns = 16
lcd_rows = 2

# Initialize pins for LCD
lcd_rs = digitalio.DigitalInOut(board.D22)  # GPIO22
lcd_en = digitalio.DigitalInOut(board.D10)  # GPIO10
lcd_d4 = digitalio.DigitalInOut(board.D9)   # GPIO9
lcd_d5 = digitalio.DigitalInOut(board.D11)  # GPIO11
lcd_d6 = digitalio.DigitalInOut(board.D5)   # GPIO5
lcd_d7 = digitalio.DigitalInOut(board.D6)   # GPIO6

# Initialize RGB backlight pins
red = digitalio.DigitalInOut(board.D13)    # GPIO13
green = digitalio.DigitalInOut(board.D19)  # GPIO19
blue = digitalio.DigitalInOut(board.D26)   # GPIO26

# Set RGB pins as outputs
red.direction = digitalio.Direction.OUTPUT
green.direction = digitalio.Direction.OUTPUT
blue.direction = digitalio.Direction.OUTPUT

# Initialize the LCD
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
    lcd_columns, lcd_rows
)
# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)  # Button input
GPIO.setup(14, GPIO.OUT) # LED output

# OPC UA Server Details (from the first script)
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

    previous_button_state = None

    while True:
        # Read physical button state
        physical_button = GPIO.input(15)
        state = 0

        # Read OPC UA tag value
        server_value = tag_node.get_value()
        # temp_value = temp_tag.get_value()
        GPIO.output(14, server_value)  # Update LED based on server value

        # Only update OPC UA if the button state has changed
        if physical_button != previous_button_state:
            tag_node.set_value(ua.Variant(physical_button, ua.VariantType.Boolean))
            print(f"Updated OPC UA tag: {physical_button}")
        
            
        if tag_node == 1:
            lcd.message = "no "
        else:
             lcd.message = "yes"
             
        
 #        sys_st.set_value(ua.Variant(state, ua.VariantType.integer))
        sys_st.set_value(ua.Variant(state))
      #  print(f": {state}")
        statecheck = sys_st.get_value()
      #  print(f"state: {statecheck}")
#          lcd.message = "{temp_value}"
        # ^	this should display the value of the TemperatureTag on the HTS_CTRL Studio 5000 file.
        
        previous_button_state = physical_button
        time.sleep(0.1)  # Small delay to prevent excessive updates

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
    GPIO.cleanup()
