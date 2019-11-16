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
# raspberry pi packages
import gpiozero # uses BCM numbering by default
# importing local files
import constants
import display
import os
from picamera import PiCamera

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
  else:
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
  else:
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
      if tmp == 100:
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
      tmp = 1.0 if tmp == 10 else tmp
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
  set_params()

def setup_width_storage_dir(heightName,widthName):
    finalDirName = "/home/pi/Desktop/ImageTestFolder/height-" + dirName + "/" + widthName + "/"
    if not os.path.exists(finalDirName):
        os.makedirs(finalDirName)

def setup_height_storage_dir(heightName):
    ''' creating folders for each height if they do not exsist'''
    finalDirName = "/home/pi/Desktop/ImageTestFolder/height-" + dirName + "/"
    if not os.path.exists(finalDirName):
        os.makedirs(finalDirName)

def picture_setup():
    for i in range(0,15):
        setup_height_storage_dir(str(i))
        for j in range(0,15):
            setup_width_storage_dir(i,j)

def take_picture():
    

def store_picture():



''' SIGNAL CALLBACKS '''
toggleButton.when_pressed = toggle
resetButton.when_held = button_reset_cb

''' BEGIN SCRIPT '''

set_params()

pause() # wait indefinitely