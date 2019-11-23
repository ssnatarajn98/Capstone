from PIL import Image
import math
import os.path
from os import path
import csv

rightEdge = {}
leftEdge = {}

#get boundary with image without drone
def isBlack(pVal):
    return pVal < 150

def getBoundary(path):
    global rightEdge
    global leftEdge
    im = Image.open(path,"r")
    width, height = im.size
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
    '''for h in range(height):
        im.putpixel((int(leftEdge[h]),int(h)),(255,0,0,255))
        im.putpixel((int(rightEdge[h]),int(h)),(255,0,0,255))
    im.show()'''
        
def getBoundaryTriangle(path):
    print("called")
    im = Image.open(path,"r")
    width, height = im.size
    px = im.load()
    x0 = 200.0
    x1 = 10
    y0 = 0.0
    y1 = 200.0
    im.putpixel( ( int(x0),int(y0) ) ,(255,0,0,255) )
    im.putpixel( (int(x1),int(y1) ) , (255,0,0,255) )
    im.show()
    dx =  x1 - x0
    dy = y1 - y0
    de = abs(dy/dx)
    e = 0.0
    tmpY = y1
    cnt = -1
    for ych in range(0,480):
        im.putpixel((20,ych),(255,0,0,255))
    tmpX = x1
    while tmpX < x0:
        tmpX = tmpX + 1
        im.putpixel((tmpX,int(tmpY)),(255,0,0,255))
        if(cnt==-1):
            tmpY = tmpY-1
        else:
            tmpY = tmpY - 2
        cnt = cnt * -1
    im.show()
    

def Average(lst):
    return sum(lst) / len(lst)

def detectDrone(p):
    global rightEdge
    global leftEdge
    im = Image.open(p,"r")
    width, height = im.size
    px = im.load()    
    black_y = -1
    black_x = -1
    mn = 1000
    for h in range(height):
        for w in range(int(leftEdge[h]+80),int(rightEdge[h]-80)):
            r,g,b = px[w,h]
            if r+g+b < mn:
                mn = r+g+b
                #im.putpixel((w,h),(255,0,0,255))
                black_y = h
                black_x = w
    output = []
    '''xCord = -1
    yCord = -1
    if len(black_y) != 0:
        xCord = Average(black_x)
        yCord = Average(black_y)'''
    output.append(black_x)
    output.append(black_y)
    #im.show()
    return output

def getAllData():
    getBoundary("C:\Users\Sriram\Desktop\capstone\OutdoorTestImagesHighQuality\OutdoorTestImagesHighQuality\height-30\width-10\high-1.jpg")
    
    with open('C:\Users\Sriram\Desktop\capstone\Capstone\Testing3.csv', 'w') as csvfile:
        fieldnames = ['height', '30','40','50','60','70','80','90','100']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
        writer.writeheader()
        for i in range(30,110,10):
            WR = {}
            WR["height"] = str(i)         
            for j in range(30,110,10):
                p = "C:\Users\Sriram\Desktop\capstone\OutdoorTestImagesHighQuality\OutdoorTestImagesHighQuality\height-" + str(i) + "\\"+"width-" + str(j) + "\\high-1.jpg"
                #print(p)
                point = [-2,-2]
                if (path.isfile(p)):
                    print(p)
                    point = detectDrone(p)
                stringPoint = "(" + str(point[0]) + ","+ str(point[1]) + ")"
                WR[str(j)] = stringPoint
            writer.writerow(WR)
        csvfile.close()
getBoundaryTriangle("C:\Users\Sriram\Desktop\capstone\LowQualityRefined\OutdoorTestImages\height-40\width-40\low-1.jpg")
'''print(rightEdge)
print(leftEdge)
o = detectDrone("C:\Users\Sriram\Desktop\capstone\OutdoorTestImages\OutdoorTestImages\height-50\width-30\low-1.jpg")
print(o)
getAllData()
print("done")'''
