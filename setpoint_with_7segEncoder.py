import sys
import RPi.GPIO as GPIO
import RPi.GPIO
import time
import Encoder

a = 8
b = 10

RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(a, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(b, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)

#enc = Encoder.Encoder(3, 5)
oldVal = 0
pos = 0

delay = 5 # ms delay between digits refresh

selDigit = [40,38,36,32]
# Digits:   1, 2, 3, 4

display_list = [26,24,37,35,33,31,29] # define GPIO ports to use
#disp.List ref: A ,B ,C ,D ,E ,F ,G

digitDP = 23
#DOT = GPIO 20

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)

for pin in display_list:
  GPIO.setup(pin,GPIO.OUT) # setting pins for segments

for pin in selDigit:
  GPIO.setup(pin,GPIO.OUT)   # setting pins for digit selector
  GPIO.output(pin, 0)
GPIO.setup(digitDP,GPIO.OUT) # setting dot pin
GPIO.setwarnings(True)

# DIGIT map as array of array ,
# so that arrSeg[0] shows 0, arrSeg[1] shows 1, etc
arrSeg = [[0, 0, 0, 0, 0, 0, 1],\
          [1, 0, 0, 1, 1, 1, 1],\
          [0, 0, 1, 0, 0, 1, 0],\
          [0, 0, 0, 0, 1, 1, 0],\
          [1, 0, 0, 1, 1, 0, 0],\
          [0, 1, 0, 0, 1, 0, 0],\
          [0, 1, 0, 0, 0, 0, 0],\
          [0, 0, 0, 1, 1, 1, 1],\
          [0, 0, 0, 0, 0, 0, 0],\
          [0, 0, 0, 0, 1, 0, 0]]
GPIO.output(digitDP,1) # decimal point always off
value_list = [0, 0, 0, 0]
digit_value_index = 0
digit_value = 0
old_time = time.time()
while True:

    A = RPi.GPIO.input(a)
    B = RPi.GPIO.input(b)
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
        print(str(pos), str(value_list))
    oldVal = newVal


    value = pos
    for digit_place in range(4):
        value_list[3 - digit_place] = (int(value / 10**digit_place) % 10)
    if(value < 1000): value_list[0] = -1
    if(value < 100): value_list[1] = -1
    if(value < 10): value_list[2] = -1
    
    for segment in range(7):
        GPIO.output(display_list[segment], arrSeg[digit_value][segment])
    
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
        
        
        
        
        
    
