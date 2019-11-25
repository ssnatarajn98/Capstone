from PIL import Image
import math
import os.path
from os import path
import csv
import constants
import check

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

def writeToText():
    global rightEdge
    global leftEdge     
    getBoundaryTriangle("C:\Users\Sriram\Desktop\capstone\LowQualityRefined\OutdoorTestImages\height-40\width-40\low-1.jpg")
    File_object = open(r"C:\\Users\\Sriram\\Desktop\\final\\Capstone\\distance.txt","w+")
    
    for h in range(480):
        s = str(int(h))+"\t"+str(int(leftEdge[h])) + "\t" + str(int(rightEdge[h])) +"\n"
        File_object.write(s)
    File_object.close()