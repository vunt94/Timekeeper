import RPi.GPIO as GPIO
from signal import pause

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# GPIO.output(26, 1)
GPIO.output(19, 0)

status = 0

while True:  # Run forever
    if GPIO.input(26) == GPIO.HIGH and status == 0:
        print("Button was pushed!")
        status = 1
    else:
        if GPIO.input(26) == GPIO.LOW:
            status = 0
