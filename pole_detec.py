# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 23:06:49 2019

@author: Xingguang Zhang
"""

import numpy as np
import cv2
from collections import Counter

def reSizeImage(image, height):
    (pH, pW) = image.shape[:2]
    r = height / float(pH)
    dim = (int(pW * r), height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized

def Center(cnt):
    '''
    input: contour of cv2.findContours
    output: center of this contours
    '''
    M = cv2.moments(cnt)
    cx = M['m10']/M['m00']
    cy = M['m01']/M['m00']
    return (cx,cy)

def UpdateDict(Dict, element):
    '''
    input: Dictionary of the centers (keys: coordinates, values: the frequence number) and
           element: a new coordinate to be determined whether or not is in the dictionary
           if it is already existed (the distance is less than 2 from any value in the Dict),
           the existing key + 1; if not, add the element as a new key
    output: updated dictionary
    '''
    Keys = np.asarray([_ for _ in Dict.keys()])
    Element_array = np.asarray(element)
    # find the mininal distance between the element and other points in the dictionary keys.
    Distance = np.linalg.norm(Keys-Element_array, axis = 1)
    MinIndex = np.argmin(Distance)
    if Distance[MinIndex] <= 2:
        ca, cb = Keys[MinIndex]
        Dict[(ca, cb)] += 1
    else:
        Dict[element] = 1
    
    return Dict

def FindPole(ImgList, pole_num = 12):
    ImgList = np.asarray(ImgList)
    # Average image
    ImgAve = np.average(ImgList, axis = 0)
    ImgSqr = (ImgList - ImgAve) ** 2
    ImgCor = np.average(ImgSqr, axis = 0)
    ImgCor = 1 - ImgCor / np.max(ImgCor) 
    ImgCor[np.where(ImgCor < 0.95)] = 0
    Img = ImgCor * ImgAve
    NewImg = Img.astype('uint8')
    cent, _ = LP(Img.astype('uint8'))
    cent_dict = {}
    pos_list = []
    for c in cent:
        cent_dict[c] = 5
    for Image in ImgList:
        cent, _ = LP(Image.astype('uint8'))
        for c in cent:
            cent_dict = UpdateDict(cent_dict, c)
    print(Counter(cent_dict).most_common(pole_num))
    for (pos, freq) in Counter(cent_dict).most_common(pole_num):
        pos_list.append(pos)
        (a, b) = pos
        a = int(a)
        b = int(b)
        NewImg = cv2.circle(NewImg, (a,b), 5, color = 255, thickness=1, lineType=8, shift=0)
    
    return Img.astype('uint8'), NewImg, pos_list
        
def LP(img, LowerBound = 40, UpperBound = 180):
    img = cv2.medianBlur(img, 5)
    img = cv2.GaussianBlur(img, (5,5), 0);
    th = cv2.adaptiveThreshold(img,220,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,13,10)
    kernel = np.ones((3,3),np.uint8)    
  #  th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel) 
    th = cv2.erode(th,kernel,iterations = 1)
    th = cv2.dilate(th,kernel,iterations = 1)
    th = cv2.erode(th,kernel,iterations = 1)
    
    contours, hierarchy = cv2.findContours(th.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areaList = []
    #PosList = []

    for cont in contours:
        if cv2.contourArea(cont) <= UpperBound and cv2.contourArea(cont) >= LowerBound:
            areaList.append(Center(cont))
            x,y,w,h = cv2.boundingRect(cont)
            
            cv2.rectangle(th,(x,y),(x+w,y+h),(0,255,0),2)

    return areaList, th
    

if __name__ == '__main__':
    cap = cv2.VideoCapture('./S3_T2_depth.avi')
    cap.set(cv2.CAP_PROP_POS_FRAMES, 3)
    im_num = 0
    Im_list = []
    while(cap.isOpened()):   
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if im_num < 30:
            Im_list.append(frame)
            im_num += 1
        else:
            Img, NewImg, pos_list = FindPole(Im_list, 12)
            concatResult = np.concatenate((Img, NewImg), axis=1)
            print(pos_list)
            cap.release()
            break
    while(1):    
        cv2.imshow('frame',concatResult)

        if cv2.waitKey(1) & 0xFF == ord('q'):    
            cv2.destroyAllWindows()
            break