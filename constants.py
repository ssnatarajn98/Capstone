'''
Constant values used across all files
'''

''' GPIO PINS '''
# Buttons
TOGGLE_BUTTON = 24
RESET_BUTTON = 7

# Motor driver
MOTOR_DIRECTION = 16
MOTOR_STEP = 20
MOTOR_ENABLE = 21

# 7-segment
SEGMENT_TYPE = "COMMON ANODE" # COMMON CATHODE | COMMON ANODE
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

''' PARAMETER SELECTION '''
NUM_PARAMS = 3
TEST_PARAMS = 2
PARAM_NAMES = [
  "Flight altitude",
  "Lateral distance",
  "Time delay"
]
FLIGHT_TEST_NAMES = [
  "Height",
  "Width"
]
# 0: 0.0-10 or 1: 0 to 99
PARAM_TYPES = [
  0,
  0,
  1
]
PARAM_ACCEPTABLE_RANGES = [
  [0,10],
  [0,10],
  [-1,90]
]
''' FILES '''
CACHE_FILENAME = "cached_parameters.txt"
# amount pot can move before program decides that the user
# is trying to override the default value
POT_MOVEMENT_TOLERANCE = 0.05