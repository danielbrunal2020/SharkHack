import cv2
import mediapipe as mp
import time
import math
import numpy as np



class handDetection():
    def __init__(self, mode=False, maxHands = 2, detectionCon = 0.7, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, handNum = 0, draw = True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]
            for id, landmark in enumerate(myHand.landmark):
                h, w, c = img.shape
                center_x, center_y = int(landmark.x * w), int(landmark.y * h)
                lmList.append([id, center_x, center_y])
                if draw:
                    if id == 4:
                        cv2.circle(img, (center_x, center_y), 15, (255, 0, 255), cv2.FILLED)

        return lmList


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetection()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPos(img)
        if len(lmList) != 0:
            print(lmList[4]) #the number in [] represents the desired point (landmark) on hand

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()