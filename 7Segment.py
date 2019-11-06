import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Display:
    pins_segments =  (11,4,23,8,7,10,18,25)
    pins_digits = (22,27,17,24)
    num = {' ':(0,0,0,0,0,0,0),
        '0':(1,1,1,1,1,1,0),
        '1':(0,1,1,0,0,0,0),
        '2':(1,1,0,1,1,0,1),
        '3':(1,1,1,1,0,0,1),
        '4':(0,1,1,0,0,1,1),
        '5':(1,0,1,1,0,1,1),
        '6':(1,0,1,1,1,1,1),
        '7':(1,1,1,0,0,0,0),
        '8':(1,1,1,1,1,1,1),
        '9':(1,1,1,1,0,1,1)}
    display = (0,0,0,0)
    def __init__():
        for segment in pins_segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)
        for digit in pins_digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
    def setStep(i):
        display[0] = i
    def setValue(d):
        display[1] = int(d // 10 % 10)
        display[2] = int(d // 1 % 10)
        display[3] = int(d // 0.1 % 10)
    def getSegmentStatus(digit, segment):
        return num[display[digit]][segment]
    def getPinsSegments(i):
        return pins_segments[i]
    def getPinsDigits(i):
        return pins_digits[i]

# Code below is to test. Should display <hour.minutes>
try:
    display = Display()
    while True:
        display.setStep(str(time.gmtime()[3])[0])
        display.setValue(str(time.gmtime()[3])[1] + str(time.gmtime()[4]))
        for digit in range(4):
            for segment in range(7):
                GPIO.output(display.getPinsSegments(segment), display.getSegmentStatus(digit, segment))
            if digit == 1:
                GPIO.output(display.getPinsSegments(7), 1)
            else:
                GPIO.output(display.getPinsSegments(7), 0)
            GPIO.output(display.getPinsDigits(digit), 0)
            time.sleep(0.001)
            GPIO.output(display.getPinsDigits(digit), 1)
finally:
    GPIO.cleanup()
