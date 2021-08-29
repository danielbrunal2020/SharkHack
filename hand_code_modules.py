import cv2
import mediapipe as mp
import time
import hand_code as htm
import numpy as np
import pyautogui
from pynput.keyboard import Key, Controller
import autopy

PALM = 0
THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16
PINKY_TIP = 20

wCam, hCam = 640, 480
wScreen, hScreen = autopy.screen.size()
frameRed = 100
smooth = 5

def left_click(lmList):
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
            cv2.putText(img, "Left Click", (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (170, 0, 200), 3)
            pyautogui.click()
            time.sleep(0.25)

def right_click(lmList):
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
            cv2.putText(img, "Right Click", (10, 120), cv2.FONT_HERSHEY_PLAIN, 3, (170, 0, 200), 3)
            pyautogui.click(button='right')
            time.sleep(0.25)

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
        autopy.mouse.move(curr_x, curr_y)
        prev_x = curr_x
        prev_y = curr_y

def scroll(lmList):
    '''
    find distance of pinky(location 20) and ring finger(location 16) to palm (location 0)
    then, find distance of index finger(location 8) and middle finger(location 12) to palm (location 0)
    4 conditions:
        -index finger has to be triple distance of pinky and ring finger to palm
        -ring finger has to be triple distance of pinky and ring finger to palm
    once four conditions are met, initiate scroll
    '''
    if len(lmList) != 0:
        MIN_DISTANCE_FACTOR = 3
        #palm coordinates
        palm_x = lmList[PALM][1]
        palm_y = lmList[PALM][2]
        #index finger coordinates
        index_x = lmList[INDEX_FINGER_TIP][1]
        index_y = lmList[INDEX_FINGER_TIP][2]
        #middle finger coordinates
        middle_x = lmList[MIDDLE_FINGER_TIP][1]
        middle_y = lmList[MIDDLE_FINGER_TIP][2]
        #ring finger coordinates
        ring_x = lmList[RING_FINGER_TIP][1]
        ring_y = lmList[RING_FINGER_TIP][2]
        #pinky finger coordinates
        pinky_x = lmList[PINKY_TIP][1]
        pinky_y = lmList[PINKY_TIP][2]
        #distances
        distance_index = np.hypot(index_x - palm_x, index_y - palm_y)
        distance_middle = np.hypot(middle_x - palm_x, middle_y - palm_y)
        distance_ring = np.hypot(ring_x - palm_x, ring_y - palm_y)
        distance_pinky = np.hypot(pinky_x - palm_x, pinky_y - palm_y)

        #checking conditions
        if distance_index > MIN_DISTANCE_FACTOR * distance_ring and distance_index > MIN_DISTANCE_FACTOR * distance_pinky and distance_middle > MIN_DISTANCE_FACTOR * distance_ring and distance_middle > MIN_DISTANCE_FACTOR * distance_pinky:
            #initiate scroll
            pyautogui.click(button='middle')
            time.sleep(0.25)



def BackButton(lmList):
    keyboard = Controller()
    if len(lmList) != 0:
        index_x = lmList[INDEX_FINGER_TIP][1]
        index_y = lmList[INDEX_FINGER_TIP][2]
        middle_x = lmList[MIDDLE_FINGER_TIP][1]
        middle_y = lmList[MIDDLE_FINGER_TIP][2]
        palm_x = lmList[PALM][1]
        palm_y = lmList[PALM][2]
        distance_index = np.hypot(index_x - palm_x, index_y - palm_y)
        distance_middle = np.hypot(middle_x - palm_x, middle_y - palm_y)
        backButton = False
        if lmList[8][2] < lmList[5][2] and lmList[12][2] > lmList[9][2] and lmList[16][2] > lmList[13][2] \
                and lmList[20][2] < lmList[17][2] and distance_index > 2.5 * distance_middle:
            # go back
            keyboard.press(Key.alt_l)
            keyboard.press(Key.left)
            time.sleep(0.5)
            keyboard.release(Key.alt_l)
            keyboard.release(Key.left)
            time.sleep(0.5)

def ForwardButton(lmList):
    keyboard = Controller()
    if len(lmList) != 0:
        index_x = lmList[INDEX_FINGER_TIP][1]
        index_y = lmList[INDEX_FINGER_TIP][2]
        middle_x = lmList[MIDDLE_FINGER_TIP][1]
        middle_y = lmList[MIDDLE_FINGER_TIP][2]
        palm_x = lmList[PALM][1]
        palm_y = lmList[PALM][2]
        distance_index = np.hypot(index_x - palm_x, index_y - palm_y)
        distance_middle = np.hypot(middle_x - palm_x, middle_y - palm_y)
        backButton = False
        if lmList[8][2] < lmList[5][2] and lmList[12][2] > lmList[9][2] and lmList[16][2] > lmList[13][2] \
                and lmList[20][2] < lmList[17][2] and distance_index > 2.5 * distance_middle:
            # go back
            keyboard.press(Key.alt_l)
            keyboard.press(Key.right)
            time.sleep(0.5)
            keyboard.release(Key.alt_l)
            keyboard.release(Key.right)
            time.sleep(0.5)

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetection(detectionCon=0.7)
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)


    lmListRight = detector.findRightPos(img)
    lmListLeft = detector.findLeftPos(img)

    left_click(lmListLeft)
    right_click(lmListRight)
    scroll(lmListRight)
    BackButton(lmListLeft)
    ForwardButton(lmListRight)
    rightCursor(lmListRight)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)