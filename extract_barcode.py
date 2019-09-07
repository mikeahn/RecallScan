#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:19:03 2019

@author: Nigel
"""

import numpy as np
import imutils
import cv2
from skimage.io import imread, imsave
from scipy.signal import convolve2d as conv2
from os.path import normpath as fn 
from pyzbar.pyzbar import decode
import scipy
from scipy import ndimage
import re

# placeholder
#img_path = "/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/caviar.jpeg"

def extract_barcode(img_path):
    # image = cv2.imread("/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/udis.jpeg")
#    image = cv2.imread("/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/caviar.jpeg")
    # image = cv2.imread("/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/QQ_fish.jpeg")
    # image = cv2.imread("/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/barcode_02.jpg")
    #image = cv2.imread("/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/test.png")
    image = cv2.imread(img_path)

    # display(image.shape)
    image_rotated = imutils.rotate_bound(image, 90)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(decode(gray))!=0:
        barcode = re.sub('[^0-9]','', str(decode(gray)[0][0]))
        print(barcode)
    else:
        # compute the Scharr gradient magnitude representation of the images in both the x and y direction 
        # CV_8U is unsigned 8bit/pixel - ie a pixel can have values 0-255, this is the normal range for most image and video formats.
        # CV_32F is float - the pixel can have any value between 0-1.0, this is useful for some sets of calculations on data - but it has to be converted into 8bits to save or display by multiplying each pixel by 255.
        
        # ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
        # Sobel operators is a joint Gausssian smoothing plus differentiation operation, so it is more resistant to noise.
        # If ksize = -1, a 3x3 Scharr filter is used which gives better results than 3x3 Sobel filter.
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
        # gradX = cv2.Scharr(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
        # gradY = cv2.Scharr(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
        
        # Dx=np.array([[1,0,-1],[2,0,-2],[1,0,-1]])
        # Dy=np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
        # gradX=conv2(gray,Dx,mode='same',boundary='symm')
        # gradY=conv2(gray,Dy,mode='same',boundary='symm')
        
        # subtract the y-gradient from the x-gradient to keep vertical gradient information
        gradient = cv2.subtract(gradX, gradY)
        # Scales, calculates absolute values, and converts the result to 8-bit.
        gradient = cv2.convertScaleAbs(gradient)
        imsave(fn('images/output.jpg'),gradient)
        
        # blur and threshold the image
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 215, 255, cv2.THRESH_BINARY)
        
        # construct a closing kernel and apply it to the thresholded image
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        # close: dilation then erosion. fills holes.
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # perform a series of erosions and dilations
        closed = cv2.erode(closed, None, iterations = 4)
        closed = cv2.dilate(closed, None, iterations = 4)
        
        # find the contours in the thresholded image, then sort the contours
        # by their area, keeping only the largest one
        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
        	cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        contours = sorted(cnts, key = cv2.contourArea, reverse = True)
        
        imsave(fn('images/blurred.jpg'),blurred)
        imsave(fn('images/closed.jpg'),closed)
        
        image_original = image.copy()
        count = 1
        for c in contours[:3]:
            # compute the rotated bounding box of the largest contour
            rect = cv2.minAreaRect(c)
            # BoxPoints returns 4 corner coordinates from bottom-right and clockwise(CW).
            # opencv points are plotted as (x,y) not (row,column), and the y axis is positive downward.
            box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
            box = np.int0(box)
            # crop contours(potential barcode regions) and save
            crop_img = image_original[max(min(box[2][1],box[3][1])-50,0):max(box[0][1], box[1][1])+50, max(min(box[1][0],box[2][0])-50, 0):max(box[0][0], box[-1][0])+50]
        #     display(crop_img)
            imsave(fn('images/barcode_cropped'+str(count)+'.jpg'),crop_img)
            count += 1
            # draw a bounding box arounded the detected barcode and display the
            cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        #     display(box)
        #     scanner = zbar.Scanner()
            gray_crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        #     results = scanner.scan(gray_crop_img)
        #     if len(results)==0:
        #         print('No barcode detected')
        #     for result in results:
        #         print(result.type, result.data, result.quality, result.position)
            print(decode(gray_crop_img))
            if len(decode(gray_crop_img))!=0:
                barcode = re.sub('[^0-9]','', str(decode(gray)[0][0]))
                print(barcode)
        # cv2.imshow("Image", image)
        imsave(fn('images/final.jpg'),image)
        
        cv2.imshow("Blurred", blurred)
        cv2.imshow("Closed", closed)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        
        
