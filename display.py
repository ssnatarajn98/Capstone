from time import sleep
import constants
import gpiozero

''' SEGMENT CONSTANTS '''
pins_segments =  [
  constants.SEGMENT_A,
  constants.SEGMENT_B,
  constants.SEGMENT_C,
  constants.SEGMENT_D,
  constants.SEGMENT_E,
  constants.SEGMENT_F,
  constants.SEGMENT_G,
]
pins_digits = [
  constants.SEGMENT_D1,
  constants.SEGMENT_D2,
  constants.SEGMENT_D3,
  constants.SEGMENT_D4
]
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
display = [0,0,0,0]

# Using LED to make turning on/off the pins easy
segments = []
for i in range(len(pins_segments)):
  segments.append(gpiozero.LED(pins_segments[i]))
digits = []
for i in range(len(pins_digits)):
  digits.append(gpiozero.LED(pins_digits[i]))

# Setting up the dot
dotStatus = None
dot = gpiozero.LED(constants.SEGMENT_DOT)
def set_dot(val):
  '''
  USAGE: pass in 0, 1, 2, or 3 to indicate which
  dot on the 7-segment to enable
  '''
  global dot
  if val == None:
    dotStatus = None
  if val > 3 or val < 0:
    dot = None
    print("Error: display.py / set_dot(" + str(val) + ")")
    return
  dotStatus = val

def set_individual(digit, val):
  '''
  set digit 0, 1, 2, or 3 to a number
  '''
  # which LEDs to enable
  leds = num[str(val)]
  # disable all digits
  for d in range(len(digits)):
    digits[d].on()
  # enable/disable corresponding segments
  for j in range(len(segments)):
    if leds[j]:
      segments[j].on()
    else:
      segments[j].off()
  # enable/disable decimal dot
  if digit == dotStatus:
    dot.on()
  else:
    dot.off()
  # enable specific digit
  digits[digit].off()

def set_display(vals):
  '''
  set the display to a certain set of values, ex: ['1',' ','2','4']
  '''
  for i, val in enumerate(vals):
    set_individual(i, val)
    sleep(0.001)

def clear():
  set_display([' '] * 4)