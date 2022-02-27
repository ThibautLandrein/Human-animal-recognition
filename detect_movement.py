# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 16:28:55 2021

@author: Thibaut
"""

import cv2 as cv
from datetime import datetime
#This depends on the camera you have. You might need to do some research and testing on how to get your IP camera stream
cap = cv.VideoCapture("rtsp://login:mdp@IP:port/videoMain")
while True:
    ret, frame = cap.read()
    ret, frame2 = cap.read()

    diff = cv.absdiff(frame, frame2)

    diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)

    dilated = cv.dilate(thresh, None, iterations=3)

    contours, _ = cv.findContours(
        dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    if contours:
        cv.imwrite('E:\movement_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.jpg', frame2)
    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)
        if cv.contourArea(contour) < 900:
            continue
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv.putText(frame, "Status: {}".format('Movement'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,
                   1, (255, 0, 0), 3)

    cv.imshow("Video", frame)
    frame = frame2
    ret, frame2 = cap.read()
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
