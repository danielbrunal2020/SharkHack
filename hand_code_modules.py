import cv2
import mediapipe as mp
import time
import hand_code as htm
import numpy as np
import pyautogui
import json

def findSharkSign(lmList):
    if len(lmList) != 0:
        shark_sign = True
        i = 4
        while shark_sign and i < len(lmList):
            comparison_x = lmList[i][1]
            comparison_y = lmList[i][2]
            for j in range(i + 4, len(lmList), 4):
                current_x = lmList[j][1]
                current_y = lmList[j][2]
                distance = np.hypot(current_x-comparison_x, current_y - comparison_y)
                if(distance > 25):
                    shark_sign = False
                    break
            i = i + 4
        if shark_sign:
            #we have the shark sign at this frame
            cv2.putText(img, "Shark sign found!", (50, 150), cv2.FONT_HERSHEY_PLAIN, 3,
                        (170, 0, 200), 3)
            pyautogui.click()
            time.sleep(0.5)


pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetection(detectionCon=0.7)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmListRight = detector.findRightPos(img)
    lmListLeft = detector.findLeftPos(img)

    findSharkSign(lmListLeft)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)