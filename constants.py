'''
Constant values used across all files
'''

''' GPIO PINS '''
# Buttons
TOGGLE_BUTTON = 24
RESET_BUTTON = 7

# LED
LED_PORT = 22

# Motor driver
MOTOR_DIRECTION = 16
MOTOR_STEP = 20
MOTOR_ENABLE = 21

# 7-segment
SEGMENT_TYPE = None # 0: COMMON CATHODE | 1: COMMON ANODE
SEGMENT_D1 = 18
SEGMENT_D2 = 12
SEGMENT_D3 = 25
SEGMENT_D4 = 23
SEGMENT_A = 27
SEGMENT_B = 17
SEGMENT_C = 4
SEGMENT_D = 26
SEGMENT_E = 19
SEGMENT_F = 13
SEGMENT_G = 6
SEGMENT_DOT = 5

RIGHT_EDGE = {}
LEFT_EDGE = {}

''' PARAMETER SELECTION '''
NUM_PARAMS = 3
TEST_PARAMS = 2
PARAM_NAMES = [
  "Flight altitude",
  "Lateral distance",
  "Time delay"
]
PARAM_HEIGHT_INDEX = 0
PARAM_WIDTH_INDEX = 1
# 0: 0.0-10 or 1: 0 to 99
PARAM_TYPES = [
  0,
  0,
  1
]
PARAM_ACCEPTABLE_RANGES = [
  [0.5,10.0],
  [4.0,10.0],
  [-1,90]
]
''' FILES '''
CACHE_FILENAME = "cached_parameters.txt"
# amount pot can move before program decides that the user
# is trying to override the default value
POT_MOVEMENT_TOLERANCE = 0.05
DISTANCE_FILENAME = "/home/pi/Desktop/distance.txt"
IMAGE_FILENAME = "/home/pi/Desktop/im.jpg"

def readText():
    global RIGHT_EDGE
    global LEFT_EDGE 
    global DISTANCE_FILENAME
    f = open(DISTANCE_FILENAME,"r+")  
    line = f.readline()
    while line:
        words = line.split('\t')
        words[2] = words[:-2]
        LEFT_EDGE[int(words[0])] = int(words[1])
        RIGHT_EDGE[int(words[0])] = int(words[2][0])
        line = f.readline()
    f.close()
readText()