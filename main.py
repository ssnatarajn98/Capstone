'''
CSCE 483 Capstone
Training Cones Team
Fall 2019
'''

print("Hello, world!\n\n")
print("Importing packages...")

''' IMPORTS '''
# general packages
from time import sleep
from signal import pause
import os.path
from os import path
# raspberry pi packages
import gpiozero # uses BCM numbering by default
# importing local files
import constants
import display

print("Configuring Pi...")

''' GLOBAL VARIABLES '''
# buttons
toggleButton = gpiozero.Button(constants.TOGGLE_BUTTON)
resetButton = gpiozero.Button(constants.RESET_BUTTON, hold_time=2)
# knob
pot = gpiozero.MCP3008(channel=0)
initialPotValues = []
# parameter selection
params = [0] * constants.NUM_PARAMS # initialize to zero
paramStep = 0
currentlyToggling = True

''' AUXILIARY FUNCTIONS '''
def set_from_cached_params():
  ''' sets params to previous params saved in cache file
      if file doesn't exist, sets all to zero
  '''
  global params

  print("Pulling cached parameters...")

  # see if file exists first
  if not path.exists(constants.CACHE_FILENAME):
    print("\tParameter cache file does not exist. Defaulting to zeros.")
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
      print("\t" + str(i) + ": Ignoring erroneous cached parameter " + str(val))
    else:
      # parameter is valid, save it
      params[i] = val
      print("\t" + str(i) + ": " + str(val))
    i += 1

  f.close()

def set_params_to_cache():
  global params

  print("\nSaving parameters to cache...")

  f = open(constants.CACHE_FILENAME, "w") # will create if nonexistant
  for val in params:
    f.write(str(val) + "\n")
  f.close()

  print("\tSaved.\n")

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
  global paramStep

  if paramStep >= constants.NUM_PARAMS:
    return 0
  
  # takes a value from 0 to 100
  reading = read_pot() * 100
  if constants.PARAM_TYPES[paramStep] == 0:
    # want a value from 0.0 to 10.0
    return float(int(reading) / 10.0)
  elif constants.PARAM_TYPES[paramStep] == 1:
    return int(reading)

def take_param_reading_stable():
  ''' take a stable reading from the pot based on the current parameter type
      (to be used to save the value to memory)
  '''
  global paramStep
  
  # takes a value from 0 to 100
  reading = read_pot_stable() * 100
  if constants.PARAM_TYPES[paramStep] == 0:
    # want a value from 0.0 to 10.0
    return float(int(reading) / 10.0)
  elif constants.PARAM_TYPES[paramStep] == 1:
    if int(reading) > constants.PARAM_ACCEPTABLE_RANGES[paramStep][1]:
      return -1 # means infinity
    return int(reading)

def toggle_cb():
  ''' saves the parameter value and toggles to the next parameter to be entered '''
  global params
  global paramStep
  global currentlyToggling

  # ignore button presses after all parameters have been set
  if paramStep >= constants.NUM_PARAMS or not currentlyToggling:
    return

  # read from the pot and save the value
  print("\tToggled!")
  if initialPotValues[paramStep][1]:
    reading = take_param_reading_stable()
    print("\tSaved value " + constants.PARAM_NAMES[paramStep] + ": " + str(reading))
    params[paramStep] = reading
  else:
    # do nothing, param already has the correct value
    print("\tUsed previous value for " + constants.PARAM_NAMES[paramStep] + ": " + str(params[paramStep]))

  # save next initial pot value for overriding defaults
  initialPotValues.append([read_pot(), False]) # [val, changed?]

  # prevent debounce
  sleep(0.2)

  # ready to read the next parameter
  if paramStep == constants.NUM_PARAMS - 1:
    currentlyToggling = False
  else:
    paramStep += 1

def reset_params():
  ''' resets all parameters to zero '''
  global params
  global paramStep
  global initialPotValues
  global currentlyToggling

  params = [0] * constants.NUM_PARAMS
  paramStep = 0
  initialPotValues = []
  currentlyToggling = True

  print("\tParameters reset.")

def set_params():
  ''' prompts user to set all parameters on the physical interface '''
  global initialPotValues
  print("\nPlease enter parameters on the physical interface.\n")
  # set initial pot value for first param
  initialPotValues.append([read_pot(), False]) # [val, changed?]
  while currentlyToggling:
    #print(read_pot())
    if not initialPotValues[paramStep][1]:
      if abs(read_pot() - initialPotValues[paramStep][0]) < constants.POT_MOVEMENT_TOLERANCE:
        # significant movement has not been detected
        # keep showing default value
        tmp = params[paramStep]
      else:
        # we've moved! let the user change the value now
        initialPotValues[paramStep][1] = True
        tmp = take_param_reading()
    else:
      # user doesn't want to use the default; take actual pot value
      tmp = take_param_reading()
    if isinstance(tmp, int):
      # if value is 0-100
      display.set_dot(None)
      if tmp > constants.PARAM_ACCEPTABLE_RANGES[paramStep][1]:
        # set to inf
        display.set_display([
          paramStep + 1,
          ' ',
          'inf',
          'inf'
        ])
      else:
        display.set_display([
          paramStep + 1,
          ' ',
          ' ' if tmp < 10 else int(tmp / 10),
          int(tmp - (int(tmp / 10) * 10))
        ])
    else:
      # if value is 0.0-10.0
      display.set_dot(2 if tmp < 10 else None)
      tmp = 1.0 if tmp == 10 else tmp
      # in case of concurrency issues causing floating point to be disregarded
      tmp = float(tmp / 10) if tmp > 10 else tmp
      display.set_display([
        paramStep + 1,
        ' ',
        ' ' if (int(tmp) == 0) else int(tmp), # if first digit is zero dont show
        int((tmp - int(tmp)) * 10) # ones place
      ])

  display.clear()
  set_params_to_cache()

def button_reset_cb():
  ''' callback function to allow user to set parameters again '''
  print("\nDevice reset triggered!\n")
  reset_params()
  set_from_cached_params()
  set_params()

''' SIGNAL CALLBACKS '''
toggleButton.when_pressed = toggle_cb
resetButton.when_held = button_reset_cb

print("Configuration complete.")

''' BEGIN SCRIPT '''
set_from_cached_params()
set_params()

pause() # wait indefinitely
