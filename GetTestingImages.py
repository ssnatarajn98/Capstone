import os
from picamera import PiCamera
from time import sleep
import gpiozero
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

  if paramStep > constants.NUM_PARAMS:
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

  # ignore button presses after all parameters have been set
  if paramStep >= constants.NUM_PARAMS:
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
  paramStep += 1

def reset_params():
  ''' resets all parameters to zero '''
  global params
  global paramStep
  global initialPotValues

  params = [0] * constants.NUM_PARAMS
  paramStep = 0
  initialPotValues = []

  print("\tParameters reset.")

def allTestPictures():
    if not os.path.exists('/home/pi/Desktop/OutdoorTestImages/'):
        os.makedirs('/home/pi/Desktop/OutdoorTestImages/')

def setupHeightFolder(height):
    allTestPictures()
    currDir = "/home/pi/Desktop/OutdoorTestImages/height-" + str(height)+"/"
    print(currDir)
    if not os.path.exists(currDir):
        os.makedirs(currDir)

def setupWidthFolder(height, width):
    setupHeightFolder(height)
    currDir = "/home/pi/Desktop/OutdoorTestImages/height-" + str(height)+"/"+"width-"+str(width)+"/"
    if not os.path.exists(currDir):
        os.makedirs(currDir)

def setupCamera():
    camera = PiCamera()
    camera.start_preview()

def setupFolder():
    for i in range(30, 120, 5):
        #print(i)
        setupHeightFolder(i)
        for j in range(30,120,5):
            #print(j)
            setupWidthFolder(i,j)

def reset_params():
  ''' resets all parameters to zero '''
  global params
  global paramStep
  global initialPotValues

  params = [0] * constants.NUM_PARAMS
  paramStep = 0
  initialPotValues = []

  print("\tParameters reset.")

def set_params():
  ''' prompts user to set all parameters on the physical interface '''
  global initialPotValues
  print("Please enter parameters on the physical interface.\n")
  # set initial pot value for first param
  initialPotValues.append([read_pot(), False]) # [val, changed?]
  while paramStep < constants.NUM_PARAMS:
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

def button_reset_cb():
  ''' callback function to allow user to set parameters again '''
  print("\nDevice reset triggered!\n")
  reset_params()
  set_from_cached_params()
  set_params()
  
toggleButton.when_pressed = toggle_cb
resetButton.when_held = button_reset_cb

setupFolder()

set_params()
pause()



