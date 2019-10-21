# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 20:22:41 2019

@author: Xingguang Zhang
"""

import imutils
import cv2
import sys
from random import randint

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
 # Create a tracker based on tracker name
 if trackerType == trackerTypes[0]:
   tracker = cv2.TrackerBoosting_create()
 elif trackerType == trackerTypes[1]: 
   tracker = cv2.TrackerMIL_create()
 elif trackerType == trackerTypes[2]:
   tracker = cv2.TrackerKCF_create()
 elif trackerType == trackerTypes[3]:
   tracker = cv2.TrackerTLD_create()
 elif trackerType == trackerTypes[4]:
   tracker = cv2.TrackerMedianFlow_create()
 elif trackerType == trackerTypes[5]:
   tracker = cv2.TrackerGOTURN_create()
 elif trackerType == trackerTypes[6]:
   tracker = cv2.TrackerMOSSE_create()
 elif trackerType == trackerTypes[7]:
   tracker = cv2.TrackerCSRT_create()
 else:
   tracker = None
   print('Incorrect tracker name')
   print('Available trackers are:')
   for t in trackerTypes:
     print(t)
   
 return tracker

cap = cv2.VideoCapture('./S1_T1_color.avi')
ret, frame = cap.read()
if not ret:
    print('Failed to read video')
    sys.exit(1)
#frame = imutils.resize(frame, height = 500)
bboxes = []
colors = [] 
for i in range(3):
    bbox = cv2.selectROI('MultiTracker', frame, showCrosshair = False)
    print(bbox)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    
    print("Press ‘enter’ key to select next object")
    if i == 2:
        cv2.destroyAllWindows()
    
print('Selected bounding boxes {}'.format(bboxes))
# Specify the tracker type
trackerType = "CSRT"   
# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()
# Initialize MultiTracker 
for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox)
    
while(cap.isOpened()):
    success, frame = cap.read()
    if not success:
        break
    #frame = imutils.resize(frame, height = 500)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)
    
    # draw tracked objects
    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
    cv2.imshow('MultiTracker', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('Selected bounding boxes {}'.format(bboxes))
