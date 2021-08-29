from PySimpleGUI.PySimpleGUI import InputText
import cv2
import mediapipe as mp
import time

import hand_code as htm
import numpy as np
import pyautogui
from pynput.keyboard import Key, Controller
import autopy
import PySimpleGUI as sg

PALM = 0
THUMB_TIP = 4
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
RING_FINGER_TIP = 16
PINKY_TIP = 20
INDEX_KNUCKLE = 5
MIDDLE_KNUCKLE = 9
RING_KNUCKLE = 13
PINKY_KNUCKLE = 17
INDEX_JOINT = 6
MIDDLE_JOINT = 10
RING_JOINT = 14
PINKY_JOINT = 18

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


def volume_increaser(lmList):
    '''
    Desired hand gesture: "thumbs-up"
    VALUES NEEDED:
    ------------------------------------------------------------------------------------
    1. Acquire locations of thumb tip, index tip, middle tip, ring tip, pinky tip (both x and y)
    2. Acquire locations of index knuckle, middle knuckle, ring knuckle, pinky knuckle
    3. Acquire locations of index joint, middle joint, ring joint, pinky joint
    CONDITIONS:
    ------------------------------------------------------------------------------------
    FIRST: Check thumb is above index finger, middle finger, ring finger, pinky tips
    SECOND: index knuckle location (5) has to be above middle finger knuckle (9), and so on until the
    ring finger knuckle has to be greater than the pinky knuckle location
    THIRD: finger tip x locations have to be located left of the joint locations
    Once all conditions are satisfied, then increase the volume
    '''
    if len(lmList) != 0:
        keyboard = Controller()
        volume_change = True
        #step 1 - Values
        thumb_y = lmList[THUMB_TIP][2]
        index_tip_x = lmList[INDEX_FINGER_TIP][1]
        index_tip_y = lmList[INDEX_FINGER_TIP][2]
        middle_tip_x = lmList[MIDDLE_FINGER_TIP][1]
        middle_tip_y = lmList[MIDDLE_FINGER_TIP][2]
        ring_tip_x = lmList[RING_FINGER_TIP][1]
        ring_tip_y = lmList[RING_FINGER_TIP][2]
        pinky_tip_x = lmList[PINKY_TIP][1]
        pinky_tip_y = lmList[PINKY_TIP][2]
        #step 2 - Values
        index_knuckle_y = lmList[INDEX_KNUCKLE][2]
        middle_knuckle_y = lmList[MIDDLE_KNUCKLE][2]
        ring_knuckle_y = lmList[RING_KNUCKLE][2]
        pinky_knuckle_y = lmList[PINKY_KNUCKLE][2]
        #step 3 - Values
        index_joint_x = lmList[INDEX_JOINT][1]
        middle_joint_x = lmList[MIDDLE_JOINT][1]
        ring_joint_x = lmList[RING_JOINT][1]
        pinky_joint_x = lmList[PINKY_JOINT][1]
        #checking first condition:
        if not(thumb_y < index_tip_y and thumb_y < middle_tip_y and thumb_y < ring_tip_y and thumb_y < pinky_tip_y):
            volume_change = False
        #checking second condition:
        if not(index_knuckle_y < middle_knuckle_y and middle_knuckle_y < ring_knuckle_y and ring_knuckle_y < pinky_knuckle_y):
            volume_change = False
        #checking third condition:
        if not(index_tip_x < index_joint_x and middle_tip_x < middle_joint_x and ring_tip_x < ring_joint_x and pinky_tip_x < pinky_joint_x):
            volume_change = False
        #initiate volume increase
        if volume_change:
            keyboard.press(Key.media_volume_up)

def volume_decreaser(lmList):
    '''
    Desired hand gesture: "thumbs-down"
    VALUES NEEDED:
    ------------------------------------------------------------------------------------
    1. Acquire locations of thumb tip, index tip, middle tip, ring tip, pinky tip (both x and y)
    2. Acquire locations of index knuckle, middle knuckle, ring knuckle, pinky knuckle
    3. Acquire locations of index joint, middle joint, ring joint, pinky joint
    CONDITIONS:
    ------------------------------------------------------------------------------------
    FIRST: Check thumb is below index finger, middle finger, ring finger, pinky tips
    SECOND: index knuckle location (5) has to be below middle finger knuckle (9), and so on until the
    ring finger knuckle has to be below the pinky knuckle location
    THIRD: finger tip x locations have to be located left of the joint locations
    Once all conditions are satisfied, then decrease the volume
    '''
    if len(lmList) != 0:
        keyboard = Controller()
        volume_change = True
        #step 1 - Values
        thumb_y = lmList[THUMB_TIP][2]
        index_tip_x = lmList[INDEX_FINGER_TIP][1]
        index_tip_y = lmList[INDEX_FINGER_TIP][2]
        middle_tip_x = lmList[MIDDLE_FINGER_TIP][1]
        middle_tip_y = lmList[MIDDLE_FINGER_TIP][2]
        ring_tip_x = lmList[RING_FINGER_TIP][1]
        ring_tip_y = lmList[RING_FINGER_TIP][2]
        pinky_tip_x = lmList[PINKY_TIP][1]
        pinky_tip_y = lmList[PINKY_TIP][2]
        #step 2 - Values
        index_knuckle_y = lmList[INDEX_KNUCKLE][2]
        middle_knuckle_y = lmList[MIDDLE_KNUCKLE][2]
        ring_knuckle_y = lmList[RING_KNUCKLE][2]
        pinky_knuckle_y = lmList[PINKY_KNUCKLE][2]
        #step 3 - Values
        index_joint_x = lmList[INDEX_JOINT][1]
        middle_joint_x = lmList[MIDDLE_JOINT][1]
        ring_joint_x = lmList[RING_JOINT][1]
        pinky_joint_x = lmList[PINKY_JOINT][1]
        #checking first condition:
        if not(thumb_y > index_tip_y and thumb_y > middle_tip_y and thumb_y > ring_tip_y and thumb_y > pinky_tip_y):
            volume_change = False
        #checking second condition:
        if not(index_knuckle_y > middle_knuckle_y and middle_knuckle_y > ring_knuckle_y and ring_knuckle_y > pinky_knuckle_y):
            volume_change = False
        #checking third condition:
        if not(index_tip_x < index_joint_x and middle_tip_x < middle_joint_x and ring_tip_x < ring_joint_x and pinky_tip_x < pinky_joint_x):
            volume_change = False
        #initiate volume decrease
        if volume_change:
            keyboard.press(Key.media_volume_down)



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

def make_instruction_window():
    SPACING = 60
    layout_instructions = [
        [sg.Text("Hi, Welcome to the Instructions Page! Here you'll find a list of all functionality offered by Click Bait with their corresponding hand motions. Have fun!", justification = 'center', size = (2 * SPACING + 3, 1))],
        [sg.Text("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")],
        [sg.Text("FUNCTIONALITY", justification='center', size=(SPACING,1)), sg.Text("ACTION REQUIRED", justification='center', size=(SPACING,1))],
        [sg.Text("Move cursor around", justification='center', size=(SPACING,1)), sg.Text("Drag Right Hand Around Frame", justification='center', size=(SPACING,1))],
        [sg.Text('Left Click', justification='center', size=(SPACING,1)), sg.Text("Left Chomp", justification='center', size=(SPACING,1))],
        [sg.Text('Right Click', justification='center', size=(SPACING,1)), sg.Text("Right Chomp", justification='center', size=(SPACING,1))],
        [sg.Text('Scroll (Middle Click)', justification='center', size=(SPACING,1)), sg.Text("Harpoon", justification='center', size=(SPACING,1))],
        [sg.Text('Volume Up', justification='center', size=(SPACING,1)), sg.Text("Dorsal Fin", justification='center', size=(SPACING,1))],
        [sg.Text('Volume Down', justification='center', size=(SPACING,1)), sg.Text("Pectoral Fin", justification='center', size=(SPACING,1))],
        [sg.Text('Back Button', justification='center', size=(SPACING,1)), sg.Text("Left Hammerhead", justification='center', size=(SPACING,1))],
        [sg.Text('Forward Button', justification='center', size=(SPACING,1)), sg.Text("Right Hammerhead", justification='center', size=(SPACING,1))]
    ]
    window_instructions = sg.Window('Instructions', layout_instructions)
    while True:
        event, values = window_instructions.read()
        if event == sg.WIN_CLOSED:
            break
    window_instructions.close()

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetection(detectionCon=0.7)
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

sg.theme('DarkBlue13')
layout = [
    [sg.Text('Welcome to Click Bait!', font='100', justification='center', size = (80, 1))],
    [sg.Text('')],
    [sg.Button('Hand Gestures', size = (100, 1))],
    [sg.Text('')],
    [sg.Button('Click here to begin using Click Bait!', size = (100, 1))],
    [sg.Text('')]
]
menu_window = sg.Window('Main Menu', layout, finalize = True)
while True:
    event, values = menu_window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Click here to begin using Click Bait!':
        menu_window.Hide()
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
            volume_increaser(lmListLeft)
            volume_decreaser(lmListLeft)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)


            cv2.imshow("Image", img)
            cv2.waitKey(1)
            if cv2.getWindowProperty("Image", 0) < 0:
                exit()
    elif event == 'Hand Gestures':
        menu_window.Hide()
        make_instruction_window()
        menu_window.UnHide()
menu_window.close()
        

