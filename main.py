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
from math import ceil
import os.path
from os import path
# raspberry pi packages
import gpiozero # uses BCM numbering by default
# importing local files
import constants
import display

print("Configuring...")

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
def set_from_cached_params():
  ''' sets params to previous params saved in cache file
      if file doesn't exist, sets all to zero
  '''
  global params

  print("Pulling cached parameters...")

  # see if file exists first
  if not path.exists(constants.CACHE_FILENAME):
    print("Parameter cache file does not exist. Defaulting to zeros.")
    return

  f = open(constants.CACHE_FILENAME, "r")
  i = 0
  for val in f:
    if i > constants.NUM_PARAMS - 1:
      break
    val = val[:-1] # truncate newline char
    if '.' in val: # check if float or int
      val = float(val)
    else:
      val = int(val)
    if (val < constants.PARAM_ACCEPTABLE_RANGES[i][0] or
        val > constants.PARAM_ACCEPTABLE_RANGES[i][1]):
      print(str(i) + ": Ignoring erroneous cached parameter " + str(val))
    else:
      # parameter is valid, save it
      params[i] = val
      print(str(i) + ": " + str(val))
    i += 1

  f.close()

def set_params_to_cache():
  global params

  print("Saving parameters to cache...")

  f = open(constants.CACHE_FILENAME, "w") # will create if nonexistant
  for val in params:
    f.write(val + str("\n"))
  f.close()

  print("Saved.")

def read_pot():
  ''' reads potentiometer value from ADC '''
  return pot.value

def read_pot_stable():
  ''' average a few values from the pot in case of an anomaly/error '''
  reading = 0
  for i in range(10):
    reading += pot.value
    sleep(0.1)
  return reading / 10

def take_param_reading():
  ''' take a reading from the pot based on the current parameter type
      (to be used to update the 7 segment display)
  '''
  global param_step

  if param_step > constants.NUM_PARAMS:
    return 0
  
  # takes a value from 0 to 100
  reading = read_pot() * 100
  if constants.PARAM_TYPES[param_step] == 0:
    # want a value from 0.0 to 10.0
    return float(int(reading) / 10.0)
  elif constants.PARAM_TYPES[param_step] == 1:
    return ceil(reading)

def take_param_reading_stable():
  ''' take a stable reading from the pot based on the current parameter type
      (to be used to save the value to memory)
  '''
  global param_step
  
  # takes a value from 0 to 100
  reading = read_pot_stable() * 100
  if constants.PARAM_TYPES[param_step] == 0:
    # want a value from 0.0 to 10.0
    return float(int(reading) / 10.0)
  elif constants.PARAM_TYPES[param_step] == 1:
    if ceil(reading) > constants.PARAM_ACCEPTABLE_RANGES[1][1]:
      return -1 # means infinity
    return ceil(reading)

def toggle():
  ''' saves the parameter value and toggles to the next parameter to be entered '''
  global params
  global param_step

  # ignore button presses after all parameters have been set
  if param_step >= constants.NUM_PARAMS:
    return

  # read from the pot and save the value
  print("Toggled!")
  reading = take_param_reading_stable()
  print("Saved value " + constants.PARAM_NAMES[param_step] + ": " + str(reading))
  params[param_step] = reading

  # ready to read the next parameter
  param_step += 1

  # prevent debounce
  sleep(0.2)

def reset_params():
  ''' resets all parameters to zero '''
  global params
  global param_step

  params = [0] * constants.NUM_PARAMS
  param_step = 0

  print("Parameters reset.")

def set_params():
  ''' prompts user to set all parameters on the physical interface '''
  print("Please enter parameters on the physical interface.\n")
  while param_step < constants.NUM_PARAMS:
    tmp = take_param_reading()
    if isinstance(tmp, int):
      # if value is 0-100
      display.set_dot(None)
      if tmp > constants.PARAM_ACCEPTABLE_RANGES[1][1]:
        # set to inf
        display.set_display([
          param_step + 1,
          ' ',
          'inf',
          'inf'
        ])
      else:
        display.set_display([
          param_step + 1,
          ' ',
          ' ' if tmp < 10 else int(tmp / 10),
          int(tmp - (int(tmp / 10) * 10))
        ])
    else:
      # if value is 0.0-10.0
      display.set_dot(2 if tmp < 10 else None)
      tmp = 1.0 if tmp == 10 else tmp / 10
      display.set_display([
        param_step + 1,
        ' ',
        ' ' if (int(tmp) == 0) else int(tmp), # if first digit is zero dont show
        int((tmp - int(tmp)) * 10) # ones place
      ])

  display.clear()

def button_reset_cb():
  ''' callback function to allow user to set parameters again '''
  print("\nDevice reset triggered!\n")
  reset_params()
  set_from_cached_params()
  set_params()

''' SIGNAL CALLBACKS '''
toggleButton.when_pressed = toggle
resetButton.when_held = button_reset_cb

print("Configuration complete.")

''' BEGIN SCRIPT '''
set_from_cached_params()
set_params()

pause() # wait indefinitely
