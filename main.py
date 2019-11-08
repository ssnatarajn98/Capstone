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
toggleButton = gpiozero.Button(constants.TOGGLE_BUTTON)
resetButton = gpiozero.Button(constants.RESET_BUTTON, hold_time=2)
pot = gpiozero.MCP3008(channel=0)

''' AUXILIARY FUNCTIONS '''
def toggle():
  # TODO
  print("Button pressed!")

def button_reset():
  # TODO
  print("Device reset triggered!")

''' SIGNAL CALLBACKS '''
toggleButton.when_pressed = toggle
resetButton.when_held = button_reset

avg = 0
while True:
  for i in range(10):
    avg += pot.value
    sleep(0.05)
  print(avg / 10)
  avg = 0

pause()