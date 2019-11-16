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
SEGMENT_TYPE = "COMMON CATHODE" # COMMON CATHODE | COMMON ANODE
SEGMENT_D1 = 5
SEGMENT_D2 = 6
SEGMENT_D3 = 13
SEGMENT_D4 = 19
SEGMENT_A = 26
SEGMENT_B = 4
SEGMENT_C = 17
SEGMENT_D = 27
SEGMENT_E = 23
SEGMENT_F = 25
SEGMENT_G = 12
SEGMENT_DOT = 18

''' PARAMETER SELECTION '''
NUM_PARAMS = 3
PARAM_NAMES = [
  "Flight altitude",
  "Lateral distance",
  "Time delay"
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