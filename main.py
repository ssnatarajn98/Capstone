'''
CSCE 483 Capstone
Training Cones Team
Fall 2019
'''

print("Hello, world!")

''' IMPORTS '''
# general packages
from time import sleep
from signal import pause
# raspberry pi packages
import gpiozero # uses BCM numbering by default
# importing files
import constants

''' GLOBAL VARIABLES '''
#toggleButton = gpiozero.Button(constants.TOGGLE_BUTTON)
resetButton = gpiozero.Button(constants.RESET_BUTTON, hold_time=3)

''' AUXILIARY FUNCTIONS '''
def toggle():
  # TODO
  print("Button pressed!")

def button_reset():
  # TODO
  print("Device reset triggered!")

''' SETUP '''
#toggleButton.when_pressed = toggle
resetButton.when_held = button_reset

led = gpiozero.LED(constants.TOGGLE_BUTTON)
led.on()

while True:
  i = 0
