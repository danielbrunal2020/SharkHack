import cv2
import mediapipe as mp
import time
import hand_code as htm
import numpy as np
import pyautogui
from pynput.keyboard import Key, Controller
import autopy
import wx

wCam, hCam = 640, 480
wScreen, hScreen = autopy.screen.size()
frameRed = 100
smooth = 5

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
            # we have the shark sign at this frame
            cv2.putText(img, "Shark sign found!", (50, 150), cv2.FONT_HERSHEY_PLAIN, 3,
                        (170, 0, 200), 3)
            pyautogui.click()
            time.sleep(0.5)

def rightCursor(lmList):
    if len(lmList) != 0:
        global prev_x
        global prev_y
        global curr_x
        global curr_y
        pointer_x = lmList[8][1]
        pointer_y = lmList[8][2]
        convert_x = np.interp(pointer_x, (frameRed,wCam-frameRed), (0, wScreen))
        convert_y = np.interp(pointer_y, (frameRed, hCam-frameRed), (0, hScreen))
        curr_x = prev_x + (convert_x - prev_x) / smooth
        curr_y = prev_y + (convert_y - prev_y) / smooth
        autopy.mouse.move(wScreen - curr_x, curr_y)
        prev_x = curr_x
        prev_y = curr_y


def BackButton(lmList):
    keyboard = Controller()
    if len(lmList) != 0:
        backButton = False
        if lmList[8][2] > lmList[5][2] and lmList[12][2] > lmList[9][2] and lmList[16][2] > lmList[13][2] \
                                                                        and lmList[20][2] < lmList[17][2]:
            # go back
            keyboard.press(Key.caps_lock)
        else:
            # nothing
            keyboard.release(Key.caps_lock)


pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetection(detectionCon=0.7)
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)


    lmListRight = detector.findRightPos(img)
    lmListLeft = detector.findLeftPos(img)

    findSharkSign(lmListLeft)
    BackButton(lmListLeft)

    rightCursor(lmListRight)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)