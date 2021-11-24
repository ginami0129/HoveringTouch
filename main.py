import cv2
import mediapipe as mp
import pyautogui as gui
import HandTrackingModule as htm
import random


w, h = gui.size()
fingers = -1
clickCnt = 1
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
isGestureMode = False
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        if isGestureMode==False and abs(lmList[12][3]) >= 0.11 and abs(lmList[12][2] - lmList[0][2]) <= 0.1: 
          print("Gesture mode is detected!", random.random())
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
            print("Left gesture")
            gui.press('a')
            isGestureMode = False
          elif fingerInfo[1] - lmList[12][1] < -0.2:
            print("Right gesture")
            gui.press('d')
            isGestureMode = False
          elif fingerInfo[2] - lmList[12][2] > 0.33:
            print("Up gesture")
            gui.press('pageup')
            isGestureMode = False
          elif fingerInfo[2] - lmList[12][2] < -0.33:
            print("Down gesture")
            gui.press('pagedown')
            isGestureMode = False
    cv2.imshow("Image", img)
    cv2.waitKey(1)