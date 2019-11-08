'''
CSCE 483 Capstone
Training Cones Team
Fall 2019
'''

print("Hello, world!\n\n")

''' IMPORTS '''
# general packages
from time import sleep
from signal import pause
# raspberry pi packages
import gpiozero # uses BCM numbering by default
# importing files
import constants

''' GLOBAL VARIABLES '''
# buttons
toggleButton = gpiozero.Button(constants.TOGGLE_BUTTON)
resetButton = gpiozero.Button(constants.RESET_BUTTON, hold_time=2)
# knob
pot = gpiozero.MCP3008(channel=0)
# parameter selection
params = [0] * constants.NUM_PARAMS # initialize to zero
param_step = 0

''' AUXILIARY FUNCTIONS '''
# average a few values from the pot
# in case of an anomaly/error
def read_pot():
  reading = 0
  for i in range(10):
    reading += pot.value
    sleep(0.001)
  return reading / 10

def toggle():
  global params
  global param_step

  # ignore button presses after all parameters have been set
  if param_step >= constants.NUM_PARAMS:
    return

  # read from the pot and save the value
  print("Toggled!")
  reading = read_pot()
  print("Saved value " + constants.PARAM_NAMES[param_step] + ": " + str(reading))
  params[param_step] = reading

  # ready to read the next parameter
  param_step += 1

  # prevent debounce
  sleep(0.5)

def reset_params():
  global params
  global param_step

  params = [0] * constants.NUM_PARAMS
  param_step = 0

  print("Parameters reset.")

def set_params():
  print("Please enter parameters on the physical interface.\n")
  while param_step < constants.NUM_PARAMS:
    sleep(0.001)

def button_reset():
  print("\nDevice reset triggered!\n")
  reset_params()
  set_params()

''' SIGNAL CALLBACKS '''
toggleButton.when_pressed = toggle
resetButton.when_held = button_reset

''' BEGIN SCRIPT '''

set_params()

pause()
