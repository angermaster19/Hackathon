import cv2
import mediapipe
import Hands
import time

cap = cv2.VideoCapture(0)

ptime = 0
ctime = 0
while True:
    _,img = cap.read()
    # rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    # cv2.putText(img,str(int(c)),(10,400),cv2.FONT_HERSHEY_PLAIN,10,(255,50,255),3)
    cv2.imshow("Frame",img)
    
    cv2.waitKey(1)

