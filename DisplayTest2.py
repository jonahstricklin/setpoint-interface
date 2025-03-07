import sys
import RPi.GPIO as GPIO
import time

toDisplay="1630" # numbers and digits to display

delay = 0.005 # delay between digits refresh

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
  GPIO.output(selDigit[0], 0)
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

value = 34875
value_list = [int(digit) for digit in str(value % 10000)]
while True:
    for digit in range(4):
        GPIO.output(selDigit[digit], 1)
        digit_value = value_list[digit]
        for segment in range(7):
            GPIO.output(display_list[segment], arrSeg[digit_value][segment])
        time.sleep(delay)
        GPIO.output(selDigit[digit], 0)
        
