import RPi.GPIO
import Encoder

a = 8
b = 10

RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(a, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)
RPi.GPIO.setup(b, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)

#enc = Encoder.Encoder(3, 5)
oldVal = 0
pos = 0
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
    print(pos)
    oldVal = newVal

D1 = 37
A = 35
F = 33
D2 = 31
D3 = 29
B = 27
E = 40
D = 38
DP = 36
C = 32
G = 28
D4 = 26
'''

int('00') 0
int('01') 1
int('11') 3
int('10') 2
00
'''