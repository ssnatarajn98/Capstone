import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Motor:
    # change to actual pins later
    pin_enable = 9
    pin_direction = 10
    status = "neutral"
    def __init__():
        GPIO.setup(pin_enable, GPIO.OUT)
        GPIO.output(pin_enable, 0)
        GPIO.setup(pin_direction, GPIO.OUT)
    def setDirection(i):
        GPIO.output(pin_direction, i)
    def rotate(degrees):
        GPIO.output(pin_enable, 1)
        # adjust degrees to time relation after testing
        time.sleep(degrees * 0.001)
        GPIO.output(pin_enable, 0)
    def moveTo(pos):
        if pos == "red":
            if status == "red":
                # do nothing
            elif status == "green":
                setDirection(1)
                rotate(180)
            elif status == "neutral":
                setDirection(1)
                rotate(90)
        elif pos == "green":
            if status == "red":
                setDirection(0)
                rotate(180)
            elif status == "green":
                # do nothing
            elif status == "neutral":
                setDirection(0)
                rotate(90)
        elif pos == "neutral":
            if status == "red":
                setDirection(0)
                rotate(90)
            elif status == "green":
                setDirection(1)
                rotate(90)
            elif status == "neutral":
                # do nothing

# Code below is to test
try:
    motor = Motor()
    motor.moveTo("red")
    time.sleep(5)
    motor.moveTo("green")
    time.sleep(5)
    motor.moveTo("neutral")
    time.sleep(5)
    motor.moveTo("green")
    time.sleep(5)
    motor.moveTo("red")
    time.sleep(5)
    motor.moveTo("neutral")
finally:
    GPIO.cleanup()
