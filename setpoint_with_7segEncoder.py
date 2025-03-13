import sys
import RPi.GPIO as GPIO
import time
import Encoder
from opcua import Client, ua

# OPC UA Server Details
opcua_url = "opc.tcp://192.168.1.100:4990/FactoryTalkLinxGateway1"
setpoint_tag_id = "ns=13;s=TagGroup03#[HTS_CTRL]HTS_CRTL_Data_From_HMI.SystemState"  
#cur_temp_tag = "ns=13;s=TagGroup03#[HTS_CTRL]HTS_CRTL_Data_From_HMI.PiConfirmation"

# Create OPC UA Client instance
client = Client(opcua_url)

### Set up GPIO pins
GPIO.setmode(GPIO.BOARD) # refer to pins as they are numbered on the header
GPIO.setwarnings(True)   # listed to errors form RPi.GPIO (probaly set false when finished testing)

## GPIO for rotary encoder
encoder_pin_a = 8
encoder_pin_b = 10
GPIO.setup(encoder_pin_a, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_pin_b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

## GPI0 for 7-segment display
# Digits:   1, 2, 3, 4
selDigit = [40,38,36,32]
# Segments ref: A, B, C, D, E, F, G
display_list = [26,24,37,35,33,31,29] # define GPIO ports to use

for pin in display_list:
  GPIO.setup(pin,GPIO.OUT) # setting pins for segments
for pin in selDigit:
  GPIO.setup(pin,GPIO.OUT)   # setting pins for digit selector
  GPIO.output(pin, 0)

# decimal point on pin 23. Stays off always
digitDP = 23
GPIO.setup(digitDP,GPIO.OUT)
GPIO.output(digitDP,1)

## GPIO for switch
sw_pin_a = 16
sw_pin_b = 18
GPIO.setup(sw_pin_a, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw_pin_b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

### Initializing variables
# for the rotary encoder
oldVal = 0
pos = 0

# for the 7-segment display
value_list = [0, 0, 0, 0]
digit_value_index = 0
digit_value = 0
# character map as array of array so that arrSeg[0] shows 0, arrSeg[1] shows 1, etc.
arrSeg = [[0, 0, 0, 0, 0, 0, 1],\
          [1, 0, 0, 1, 1, 1, 1],\
          [0, 0, 1, 0, 0, 1, 0],\
          [0, 0, 0, 0, 1, 1, 0],\
          [1, 0, 0, 1, 1, 0, 0],\
          [0, 1, 0, 0, 1, 0, 0],\
          [0, 1, 0, 0, 0, 0, 0],\
          [0, 0, 0, 1, 1, 1, 1],\
          [0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 1, 0, 0],\
          [1, 1, 1, 1, 1, 1, 1,]] # blank space

delay = 4 # ms delay between digits refresh
old_time = time.time()

# for the switch
old_sw_pos = 0

try:
    if (input("Connecting to HMI server? (y/n) ") == "y"): # only for testing purposes
        print("Connecting to OPC UA Server...")
        client.connect()
        print("Connected to FactoryTalk Linx Gateway OPC UA Server")

        # Get reference to the tag node
        setpoint_tag = client.get_node(setpoint_tag_id)
#         setpoint_value = setpoint_tag.get_value()
#         print(f"setpoint_value: {setpoint_tag_id}")   #Micah Edited
#         print(f"setpoint_value: {setpoint_value}")   #Micah Edited
    
    while True:
        # read in from rotary encoder & determine new position
        A = GPIO.input(encoder_pin_a)
        B = GPIO.input(encoder_pin_b)
        newVal = int(f"{A}{B}", 2)
        if (newVal != oldVal):
            match oldVal:
                case 0:
                    if (newVal == 1): pos += 1
                    else: pos -= 1
                case 1:
                    if (newVal == 3): pos += 1
                    else: pos -= 1
                case 2:
                    if (newVal == 0): pos += 1
                    else: pos -= 1
                case 3:
                    if (newVal == 2): pos += 1
                    else: pos -= 1
            if (pos < 0): pos = 0 # clamp pos greater than 0
            print(pos)
        oldVal = newVal

        # divide pos variable into a list of 4 digits to display. -1 to denote a blank space
        value = pos
        
        for digit_place in range(4):
            value_list[3 - digit_place] = (int(value / 10**digit_place) % 10)
        if(value < 1000): value_list[0] = -1
        if(value < 100): value_list[1] = -1
        if(value < 10): value_list[2] = -1
        
        
        # when "delay" ms have ellasped
        cur_time = time.time()
        ellapsed = ((cur_time - old_time) * 1000) % 10
        if (ellapsed >= delay):
            GPIO.output(selDigit[digit_value_index], 0)
            digit_value_index += 1
            
            if digit_value_index >= 4: digit_value_index = 0;
            digit_value = value_list[digit_value_index]
            GPIO.output(selDigit[digit_value_index], 1)
            
            old_time = cur_time
            ellapsed = 0
        
        for segment in range(7):
            GPIO.output(display_list[segment], arrSeg[digit_value][segment])
        
        # read in position from switch
        if GPIO.input(sw_pin_a) == GPIO.HIGH:
            cur_sw_pos = 1
            setpoint_tag.set_value(ua.Variant(value))
        elif GPIO.input(sw_pin_b) == GPIO.HIGH: cur_sw_pos = -1
        else: cur_sw_pos = 0
            
        if ((cur_sw_pos != old_sw_pos) & (cur_sw_pos != 0)):
            print("Switch position:", cur_sw_pos)
            old_sw_pos = cur_sw_pos

# misc. interput catches for if the script crashes
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
