import RPi.GPIO as GPIO

a = 16
b = 18

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(a, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(a) == GPIO.HIGH:
        print("a")
    if GPIO.input(b) == GPIO.HIGH:
        print("b")