import cv2
import numpy as np
frameWidth = 720
frameHeight = 400
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 50)
myColours = [
    [90, 100, 100, 130, 255, 255],  # First color range (Hue: 90-130, Saturation: 50-255, Value: 50-255)
    [60, 50, 50, 120, 255, 255],  # Second color range (Hue: 35-85, Saturation: 50-255, Value: 50-255)
    [0, 100, 100, 10, 255, 255]  # Third color range (Hue: 0-179, Saturation: 185-255, Value: 50-255)
    # Third color range (Hue: 0-179, Saturation: 185-255, Value: 50-255)
]
myColourValue=[
    [205,0,0],
    [51,255,51],
    [0,0,204]]
myPoints = []
def findColour(img,myColours,myColourValue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for Colours in myColours:
        lower=np.array(Colours[0:3])
        upper=np.array(Colours[3:6])
        mask=cv2.inRange(imgHSV,lower,upper)
        # cv2.imshow("img",mask)
        x,y=  getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColourValue[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
    return newPoints

def getContours(img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x,y,w,h=0,0,0,0
        for cnt in contours:
            area = cv2.contourArea(cnt)

            if area > 500:
                cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                # print(peri)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)


                x, y, w, h = cv2.boundingRect(approx)
        return x+w//2,y

def drawonCanvas(myPoints,myColourValue):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColourValue[point[2]],cv2.FILLED)
while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints= findColour(img, myColours,myColourValue)
    if len(newPoints)!=0:
       for newP in newPoints:
           myPoints.append(newP)

    if len(myPoints)!=0:
        drawonCanvas(myPoints,myColourValue)


    cv2.imshow("output", imgResult)
    if  cv2.waitKey(1) & 0xFF == ord('q'):
        break
