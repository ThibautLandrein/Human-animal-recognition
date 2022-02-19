# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 18:10:22 2022

@author: Thibaut Landrein
"""

#Greatly inspired by http://www.robindavid.fr/opencv-tutorial/motion-detection-with-opencv.html

import cv2.cv as cv
import datetime

class MotionDetectorContour:
    def __init__(self,  login, mdp, ceil=15):
        self.ceil = ceil
        self.cv.VideoCapture("rtsp://login:mdp@IP:port/videoMain")
        cv.NamedWindow("Target", 1)

    def run(self):
        # Capture first frame to get size
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)

        width = frame.width
        height = frame.height
        surface = width * height #Surface area of the image
        cursurface = 0 #Hold the current surface that have changed

        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
        difference = None

        while True:
            color_image = cv.QueryFrame(self.capture)

            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0) #Remove false positives

            if not difference: #For the first time put values in difference, temp and moving_average
                difference = cv.CloneImage(color_image)
                temp = cv.CloneImage(color_image)
                cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
            else:
                cv.RunningAvg(color_image, moving_average, 0.020, None) #Compute the average

            # Convert the scale of the moving average.
            cv.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.AbsDiff(color_image, temp, difference)

            #Convert the image so that it can be thresholded
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)
            cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

            cv.Dilate(grey_image, grey_image, None, 18) #to get object blobs
            cv.Erode(grey_image, grey_image, None, 10)

            # Find contours
            storage = cv.CreateMemStorage(0)
            contours = cv.FindContours(grey_image, storage, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)

            backcontours = contours #Save contours

            while contours: #For all contours compute the area
                cursurface += cv.ContourArea(contours)
                contours = contours.h_next()

            avg = (cursurface*100)/surface #Calculate the average of contour area on the total size
            if avg > self.ceil:
                print("Something is moving !")
            #print avg,"%"
            cursurface = 0 #Put back the current surface to 0

            #Draw the contours on the image
            _red =  (0, 0, 255); #Red for external contours
            _green =  (0, 255, 0);# Gren internal contours
            levels=1 #1 contours drawn, 2 internal contours as well, 3 ...
            cv.DrawContours (color_image, backcontours,  _red, _green, levels, 2, cv.CV_FILLED)

            cv.ShowImage("Target", color_image)

            # Listen for ESC or ENTER key
            c = cv.WaitKey(7) % 0x100
            if c == 27 or c == 10:
                break
    
    def initRecorder(self): #Create the recorder
        codec = cv.CV_FOURCC('D', 'I', 'V', 'X')
        #codec = cv.CV_FOURCC("D", "I", "B", " ")
        self.writer=cv.CreateVideoWriter(datetime.now().strftime("%b-%d_%H:%M:%S")+".avi", codec, 15, cv.GetSize(self.frame), 1)
        #FPS set at 15 because it seems to be the fps of my cam but should be ajusted to your needs
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 2, 8) #Creates a font

if __name__=="__main__":
    t = MotionDetectorContour()
    t.run()