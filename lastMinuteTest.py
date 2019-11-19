import os
from picamera import PiCamera
from time import sleep
import gpiozero
import constants
import display

lowCamera = PiCamera()
lowCamera.resolution =  (640, 480)
#lowCamera.resolution = (2592,1944)
#lowCamera.resolution = (1280,960)



def allTestPictures():
    if not os.path.exists('/home/pi/Desktop/OutdoorTestImages/'):
        os.makedirs('/home/pi/Desktop/OutdoorTestImages/')

def setupHeightFolder(height):
    allTestPictures()
    currDir = "/home/pi/Desktop/OutdoorTestImages/height-" + str(height)+"/"
    if not os.path.exists(currDir):
        os.makedirs(currDir)

def setupWidthFolder(height, width):
    setupHeightFolder(height)
    currDir = "/home/pi/Desktop/OutdoorTestImages/height-" + str(height)+"/"+"width-"+str(width)+"/"
    if not os.path.exists(currDir):
        os.makedirs(currDir)

def setupFolder():
    for i in range(30, 120, 5):
        #print(i)
        setupHeightFolder(i)
        for j in range(30,120,5):
            #print(j)
            setupWidthFolder(i,j)

def adjustedValue(val):
    val = val * 10
    intVal = int(val)
    valRange = intVal % 10
    newVal = 0
    if(valRange<=2):
        newVal = intVal - valRange
    elif(valRange>2 and valRange <=7):
        newVal = intVal - valRange + 5
    else:
        newVal = intVal - valRange + 10
    print(newVal)
    return newVal

def takePictures(height, width):
    global lowCamera
    normHeight = adjustedValue(height)
    normWidth = adjustedValue(width)
    lowCamera.start_preview()
    cnt = 0
    while(cnt<3):
        cnt = cnt + 1
        currImage = "/home/pi/Desktop/OutdoorTestImages/height-" + str(normHeight)+"/"+"width-"+str(normWidth)+"/low-"+str(cnt)+".jpg"
        lowCamera.capture(currImage)
    lowCamera.stop_preview()
    print("\t finished photo")

def mainFunction():
    setupFolder()
    while(1):
        height = input("\t height: ")
        width = input("\t  width: ")
        takePictures(height,width)

mainFunction()


