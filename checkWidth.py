# Basic data structure
class dataset:
    def __init__(self, height, data):
        self.height = height
        self.data = data

# Data found from analyzing spreadsheet
constants = [dataset(40,[[30, 182], [50, 238]]),
             dataset(50,[[30, 117], [60, 233]]),
             dataset(60,[[30, 142], [50, 210], [70, 248]]),
             dataset(70,[[30, 120], [40, 155], [80, 239]]),
             dataset(80,[[30,  38], [40, 133], [60, 183]]),
             dataset(90,[[30,  66], [40, 119], [50, 164], [70, 199]]),
             dataset(100,[[30, 74], [60, 161], [80, 197]])]

# Given distance from center (pixels) and height (dm), returns width (dm)
def getWidth(distance, height):
    def getWidth2(distance, height):
        for i in constants:
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
    for i in range(1, len(constants)):
        if height <= constants[i].height:
            widthLow = getWidth2(distance, constants[i-1].height)
            widthHigh = getWidth2(distance, constants[i].height)
            return (height - constants[i-1].height) / 10 * (widthHigh - widthLow) + widthLow
    
    

# Basic function call for testing
print(getWidth(150, 45))
