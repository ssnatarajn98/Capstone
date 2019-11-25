from PIL import Image
import math
import os.path
from os import path
import csv

rightEdge = {}
leftEdge = {}
backgroundImagePath = ""

#get boundary with image without drone
def isBlack(pVal):
    return pVal[0] < 100 and pVal[1] < 100 and pVal[2] < 100
def isRed(pVal):
    return pVal[0]==255 and pVal[1] == 0 and pVal[2] == 0
    

def getBoundary(path):
    global rightEdge
    global leftEdge
    im = Image.open(path,"r")
    width, height = im.size
    print(width)
    print(height)
    px = im.load()
    for h in range(height):
        w = math.floor(width/2)
        while w < width - 1:
            r,g,b = px[w,h]
            if(isBlack(r+g+b)):
                break;
            w = w + 1
        rightEdge[h] = w
        w = math.floor(width/2)
        while w > 0 :
            r,g,b = px[w,h]
            if(isBlack(r+g+b)):
                break;
            w = w - 1 
        leftEdge[h] = w
        
def getBoundaryTriangle(path):
    global rightEdge
    global leftEdge    
  
    print("called")
    im = Image.open(path,"r")
    width, height = im.size
    print(width)
    print(height)      
    px = im.load()
    x0 = 20
    y0 = 150
    x1 = 220
    y1  = 0
    tmpy = 200
    cnt = 0
    for x in range(x0,x1):
        cnt = cnt + 1
        im.putpixel((x,tmpy),(255,0,0,255))
        tmpy = tmpy - 1
    for y in range(0,480):
            im.putpixel((20,y),(255,0,0,255))
    x0 = 450
    y0 = 0
    x1 = 600
    y1  = 150
    tmpy = 0
    cnt = 0
    for x in range(x0,x1):
        im.putpixel((x,tmpy),(255,0,0,255))
        tmpy = tmpy + 1
    for y in range(0,480):
        im.putpixel((600,y),(255,0,0,255))    
    x0 = 20
    y0 = 400
    x1 = 100
    y1  = 480
    tmpy = 400
    cnt = 0
    for x in range(x0,x1):
        im.putpixel((x,tmpy),(255,0,0,255))
        tmpy = tmpy + 1             
    im.show()
    for h in range(height):
        w = math.floor(width/2)
        while w < width - 1:
            r,g,b = px[w,h]
            if(isRed([r,g,b])):
                break;
            w = w + 1
        rightEdge[h] = w
        w = math.floor(width/2)
        while w > 0 :
            r,g,b = px[w,h]
            if(isRed([r,g,b])):
                break;
            w = w - 1 
        leftEdge[h] = w    
    

def Average(lst):
    return sum(lst) / len(lst)

def detectDrone(p):
    global rightEdge
    global leftEdge
    im = Image.open(p,"r")
    width, height = im.size
    px = im.load()    
    black_y = []
    black_x = []
    for h in range(5,height-5):
        for w in range(int(leftEdge[h]+1),int(rightEdge[h]-1)):
            '''if w == int(leftEdge[h] + 1) or w == int(rightEdge[h] - 2):
                im.putpixel((w,h),(0,255,0,255))'''
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

def getAllData():
    getBoundaryTriangle("C:\Users\Sriram\Desktop\capstone\LowQualityRefined\OutdoorTestImages\height-40\width-40\low-1.jpg")
    with open('C:\\Users\\Sriram\\Desktop\\final\\Testing2.csv', 'w') as csvfile:
        fieldnames = ['height', '30','40','50','60','70','80','90','100']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
        writer.writeheader()
        for i in range(30,110,10):
            WR = {}
            WR["height"] = str(i)         
            for j in range(30,110,10):
                p = "C:\\Users\Sriram\\Desktop\\capstone\\LowQualityRefined\OutdoorTestImages\\height-" + str(i) + "\\"+"width-" + str(j) + "\\low-1.jpg"
                point = [-2,-2]
                if (path.isfile(p)):
                    print(p)
                    point = detectDrone(p)
                stringPoint = "(" + str(point[0]) + ","+ str(point[1]) + ")"
                WR[str(j)] = stringPoint
            writer.writerow(WR)
        csvfile.close()


def isInRange(height,width):
    return false
    
    
