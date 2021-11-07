import cv2
import time
import mediapipe as mp
import pyautogui as gui
import HandTrackingModule as htm

w, h = gui.size()
fingers = -1
clickCnt = 1
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        x, y = (lmList[8][1] * w , lmList[8][2] * h)
        gui.moveTo(x, y)
        temp = detector.countFinger()
        if fingers != temp:
          fingers = temp
          if (fingers == 2):
            gui.click(x, y, button='left')
            print("Click!", clickCnt)
            clickCnt = clickCnt + 1
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255), 2);
    cv2.imshow("Image", img)
    cv2.waitKey(1)