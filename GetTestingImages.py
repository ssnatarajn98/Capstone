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

def allTestPictures():
    if not os.path.exists('/home/pi/Desktop/OutdoorTestImages/'):
        os.makedirs('/home/pi/Desktop/OutdoorTestImages/')

def setupHeightFolder(height):
    allTestPictures()
    currDir = "/home/pi/Desktop/ImageTestFolder/height-" + str(height)+"/"
    if not os.path.exists(currDir):
        os.makedirs(currDir)

def setupWidthFolder(height, width):
    setupHeightFolder(height)
    currDir = "/home/pi/Desktop/ImageTestFolder/height-" + str(height)+"/"+"width-"+str(width)+"/"
    if not os.path.exists(currDir):
        os.makedirs(currDir)

def setupCamera():
    camera = PiCamera()
    camera.start_preview()

def setupFolder():
    for i in range(30, 120, 5):
        print(i)
        setupHeightFolder(i)
        for j in range(30,120,5):
            print(j)
            setupWidthFolder(i,j)
setupFolder()



