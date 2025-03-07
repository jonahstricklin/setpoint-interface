#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: May 5th, 2020
# Version: 1.0

# Import required libraries
import sys
import RPi.GPIO as GPIO
import time

toDisplay="1630" # numbers and digits to display

delay = 0.005 # delay between digits refresh

# --------------------------------------------------------------------
# PINS MAPPING AND SETUP
# selDigit activates the 4 digits to be showed (0 is active, 1 is unactive)
# display_list maps segments to be activated to display a specific number inside the digit
# digitDP activates Dot led
# --------------------------------------------------------------------

selDigit = [40,38,36,32]
# Digits:   1, 2, 3, 4

display_list = [26,24,37,35,33,31,29] # define GPIO ports to use
#disp.List ref: A ,B ,C ,D ,E ,F ,G

digitDP = 23
#DOT = GPIO 20

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)



#RPi.GPIO.setmode(RPi.GPIO.BOARD)
#RPi.GPIO.setup(a, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)
#RPi.GPIO.setup(b, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)



# Set all pins as output
'''
GPIO.setup(40,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)


GPIO.setup(26,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
'''
for pin in display_list:
  GPIO.setup(pin,GPIO.OUT) # setting pins for segments

for pin in selDigit:
  GPIO.setup(pin,GPIO.OUT) # setting pins for digit selector
GPIO.setup(digitDP,GPIO.OUT) # setting dot pin
GPIO.setwarnings(True)

# DIGIT map as array of array ,
#so that arrSeg[0] shows 0, arrSeg[1] shows 1, etc
arrSeg = [[1,1,1,1,1,1,0],\
          [0,1,1,0,0,0,0],\
          [1,1,0,1,1,0,1],\
          [1,1,1,1,0,0,1],\
          [0,1,1,0,0,1,1],\
          [1,0,1,1,0,1,1],\
          [1,0,1,1,1,1,1],\
          [1,1,1,0,0,0,0],\
          [1,1,1,1,1,1,1],\
          [1,1,1,1,0,1,1]]

GPIO.output(digitDP,0) # DOT pin

# --------------------------------------------------------------------
# MAIN FUNCTIONS
# splitToDisplay(string) split a string containing numbers and dots in
#   an array to be showed
# showDisplay(array) activates DIGITS according to array. An array
#   element to space means digit deactivation
# --------------------------------------------------------------------

def showDisplay(digit):
 for i in range(0, 4): #loop on 4 digits selectors (from 0 to 3 included)
  sel = [1,1,1,1]
  sel[i] = 0
  GPIO.output(selDigit, sel) # activates selected digit
  if digit[i].replace(".", "") == " ": # space disables digit
   GPIO.output(display_list,0)
   continue
  numDisplay = int(digit[i].replace(".", ""))
  GPIO.output(display_list, arrSeg[numDisplay]) # segments are activated according to digit mapping
  if digit[i].count(".") == 1:
   GPIO.output(digitDP,1)
  else:
   GPIO.output(digitDP,0)
  time.sleep(delay)

def splitToDisplay (toDisplay): # splits string to digits to display
 arrToDisplay=list(toDisplay)
 for i in range(len(arrToDisplay)):
  if arrToDisplay[i] == ".": arrToDisplay[(i-1)] = arrToDisplay[(i-1)] + arrToDisplay[i] # dots are concatenated to previous array element
 while "." in arrToDisplay: arrToDisplay.remove(".") # array items containing dot char alone are removed
 return arrToDisplay

# --------------------------------------------------------------------
# MAIN LOOP
# persistence of vision principle requires that digits are powered
#   on and off at a specific speed. So main loop continuously calls
#   showDisplay function in an infinite loop to let it appear as
#   stable numbers display
# --------------------------------------------------------------------

try:
 while True:
  showDisplay(splitToDisplay(toDisplay))
except KeyboardInterrupt:
 print('interrupted!')
 GPIO.cleanup()
sys.exit()

