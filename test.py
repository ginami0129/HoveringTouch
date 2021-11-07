import cv2
import time
import mediapipe as mp
import pyautogui as gui
import HandTrackingModule as htm
import random


w, h = gui.size()
fingers = -1
clickCnt = 1
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
detector = htm.handDetector()
isGestureMode = False
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        if isGestureMode==False and abs(lmList[12][3]) >= 0.11 and abs(lmList[12][2] - lmList[0][2]) <= 0.1: 
          print("gesture mode detected!", random.random())
          isGestureMode = True
          fingerInfo = lmList[12]
        if isGestureMode == False:
          x, y = (lmList[9][1] * w , lmList[9][2] * h)
          gui.moveTo(x, y)
          temp = detector.countFinger()
          if fingers != temp:
            fingers = temp
            if (fingers == 1):
              gui.click(x, y, button='left')
              print("Click!", clickCnt)
              clickCnt = clickCnt + 1
        else:
          if fingerInfo[1] - lmList[12][1] > 0.2:
            print("left gesture")
            gui.press('a')
            isGestureMode = False
          elif fingerInfo[1] - lmList[12][1] < -0.2:
            print("right gesture")
            gui.press('d')
            isGestureMode = False
          elif fingerInfo[2] - lmList[12][2] > 0.33:
            print("up gesture")
            gui.press('pageup')
            isGestureMode = False
          elif fingerInfo[2] - lmList[12][2] < -0.33:
            print("down gesture")
            gui.press('pagedown')
            isGestureMode = False
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255), 2);
    cv2.imshow("Image", img)
    cv2.waitKey(1)