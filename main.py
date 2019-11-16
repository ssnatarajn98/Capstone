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
# importing local files
import constants
import display

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
def read_pot():2
  return pot.value


# average a few values from the pot
# in case of an anomaly/error
def read_pot_stable():
  reading = 0
  for i in range(10):
    reading += pot.value
    sleep(0.1)
  return reading / 10

def toggle():
  global params
  global param_step

  # ignore button presses after all parameters have been set
  if param_step >= constants.NUM_PARAMS:
    return

  # read from the pot and save the value
  print("Toggled!")
  reading = float(int(read_pot_stable() * 100) / 10.0)
  print("Saved value " + constants.PARAM_NAMES[param_step] + ": " + str(reading))
  params[param_step] = reading

  # ready to read the next parameter
  param_step += 1

  # prevent debounce
  sleep(0.2)

def reset_params():
  global params
  global param_step

  params = [0] * constants.NUM_PARAMS
  param_step = 0

  print("Parameters reset.")

def set_params():
  print("Please enter parameters on the physical interface.\n")
  while param_step < constants.NUM_PARAMS:
    tmp = float(int(read_pot() * 100) / 10.0)
    dotStatus = 2 if (tmp < 10) else None # enable decimal if less than 10
    display.set_dot(dotStatus)
    tmp = 1.0 if (tmp == 10) else tmp
    display.set_display([
      param_step + 1,
      ' ',
      ' ' if (int(tmp) == 0) else int(tmp), # if first digit is zero dont show
      int((tmp - int(tmp)) * 10) # ones place
      ])
  display.clear()

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
