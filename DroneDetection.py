from PIL import Image
import math
import os.path
from os import path
import csv
import constants
from picamera import PiCamera


#checkWidth ----------------
class dataset:
    def __init__(self, height, data):
        self.height = height
        self.data = data

# Data found from analyzing spreadsheet
c = [dataset(40,[[30, 182], [50, 238]]),
             dataset(50,[[30, 117], [60, 233]]),
             dataset(60,[[30, 142], [50, 210], [70, 248]]),
             dataset(70,[[30, 120], [40, 155], [80, 239]]),
             dataset(80,[[30,  38], [40, 133], [60, 183]]),
             dataset(90,[[30,  66], [40, 119], [50, 164], [70, 199]]),
             dataset(100,[[30, 74], [60, 161], [80, 197]])]

# Given distance from center (pixels) and height (dm), returns width (dm)
def getWidth(distance, height):
    def getWidth2(distance, height):
        for i in c:
            if i.height == height:
                length = len(i.data)
                if distance < i.data[0][1]:
                    return distance / i.data[0][1] * i.data[0][0]
                if distance > i.data[length-1][1]:
                    return distance / i.data[length-1][1] * i.data[length-1][0]
                for j in range(1, length):
                    if distance < i.data[j][1]:
                        return (distance - i.data[j-1][1]) / (i.data[j][1] - i.data[j-1][1]) * (i.data[j][0] - i.data[j-1][0]) + i.data[j-1][0]
                return -1
    for i in range(1, len(c)):
        if height <= c[i].height:
            widthLow = getWidth2(distance, c[i-1].height)
            widthHigh = getWidth2(distance, c[i].height)
            return (height - c[i-1].height) / 10 * (widthHigh - widthLow) + widthLow
#-------------
rightEdge = {}
leftEdge = {}
camera = PiCamera()
camera.resolution =  (640, 480)

#get boundary with image without drone


def isRed(pVal):
    return pVal[0]==255 and pVal[1] == 0 and pVal[2] == 0

def isBlack(pVal):
    return pVal[0] < 10 and pVal[1] < 10 and pVal[2] < 10

def Average(lst):
    return sum(lst) / len(lst)

def detectDrone(p):
    rightEdge = constants.RIGHT_EDGE
    leftEdge = constants.LEFT_EDGE
    im = Image.open(p,"r")
    width, height = im.size
    px = im.load()
    black_y = []
    black_x = []
    for h in range(5,height-5):
        for w in range( (int(leftEdge[h])+1) , (int(rightEdge[h])-1)  ):
            r,g,b = px[w,h]
            if isBlack([r,g,b]):
                im.putpixel((w,h),(255,0,0,255))
                black_y.append(h)
                black_x.append(w)
    output = []
    xCord = -1
    yCord = -1
    if len(black_y) != 0:
        xCord = Average(black_x)
        yCord = Average(black_y)
    output.append(xCord)
    output.append(yCord)
    im.show()
    return output



def takePicture():
    global camera
    camera.start_preview()
    currImage = constants.IMAGE_FILENAME
    camera.capture(currImage)
    camera.stop_preview()

def getDistance(loc):
    return math.sqrt((loc[0] - 320)**2 + (loc[1] - 240)**2)

def isInRange(height,width):
    takePicture()
    return detectDroneDemo(constants.IMAGE_FILENAME)

