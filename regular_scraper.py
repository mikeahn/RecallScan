# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:19:03 2019

@author: Nigel, Jeong Min
"""

import PIL
from PIL import Image
import csv
from bs4 import BeautifulSoup
import requests
import re
import time
import calendar
import numpy as np
import cv2
import imutils
# import cv2
from skimage.io import imread, imsave
from scipy.signal import convolve2d as conv2
from os.path import normpath as fn, basename
from pyzbar.pyzbar import decode
import os
import scipy
from scipy import ndimage

# This will run as a cron job daily to get the latest recall information and add to the database.

# constants
# category of interest
COI = "Food & Beverages"
title_header = ["upc", "announcement_date_timestamp", "brand_val", "company_value", "description_val", "recall_reason_val", "url"]
FDA_URL = "https://www.fda.gov"



# Function to extract barcode from image

# placeholder
# img_path = "/Users/Nigel/Desktop/Wash U/2019 MS Fall/PennApps/images/caviar.jpeg"

def extract_barcode(img_path):
    image = cv2.imread(img_path)
    # response = requests.get(img_path)
    # image = Image.open(BytesIO(response.content))

    # display(image.shape)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(decode(gray)) != 0:
        barcode = re.sub('[^0-9]', '', str(decode(gray)[0][0]))
        # print(barcode)
        return barcode
    else:
        # computing the Scharr gradient magnitude representation of the images in both the x and y direction
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

        # subtract y-gradient from the x-gradient to only keep vertical gradient
        gradient = cv2.subtract(gradX, gradY)
        # Scales, calculates absolute values, and converts the result to 8-bit.
        gradient = cv2.convertScaleAbs(gradient)
        # imsave(fn('images/output.jpg'), gradient)

        # blur and threshold the image
        # blur will make the barcode region brighter while making the other regions darker
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 215, 255, cv2.THRESH_BINARY)

        # construct a closing kernel and apply it to the thresholded image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        # close: dilation then erosion. fills holes.
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # perform a series of erosions and dilations
        closed = cv2.erode(closed, None, iterations=5)
        closed = cv2.dilate(closed, None, iterations=5)

        # find the largest components in the thresholded image, and keep the
        # top 3 largest components
        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        contours = sorted(cnts, key=cv2.contourArea, reverse=True)

        # imsave(fn('images/blurred.jpg'), blurred)
        # imsave(fn('images/closed.jpg'), closed)

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
            crop_img = image_original[max(min(box[2][1], box[3][1]) - 50, 0):max(box[0][1], box[1][1]) + 50,
                       max(min(box[1][0], box[2][0]) - 50, 0):max(box[0][0], box[-1][0]) + 50]
            #     display(crop_img)
            imsave(fn('images/barcode_cropped' + str(count) + '.jpg'), crop_img)
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
            # print(decode(gray_crop_img))
            if len(decode(gray_crop_img)) != 0:
                barcode = re.sub('[^0-9]', '', str(decode(gray)[0][0]))
                # print(barcode)
                return barcode
            else:
                pass
        # cv2.imshow("Image", image)
        imsave(fn('images/final.jpg'), image)

        # cv2.imshow("Blurred", blurred)
        # cv2.imshow("Closed", closed)
        # cv2.imshow("Image", image)
        cv2.waitKey(0)
    return -1


source_url = "https://www.recalls.gov/rrfda.aspx"
r = requests.get(source_url)

data = r.text
soup = BeautifulSoup(data, "html.parser")
all_links = soup.find_all("a")
recall_gov_urls = [x.get('href') for x in all_links]

with open('/var/www/html/upc-lookup/api/latest.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    filewriter.writerow(title_header)
    for index, url in enumerate(recall_gov_urls[1:]):

        subR = requests.get(url)
        subData = subR.text
        subSoup = BeautifulSoup(subData, "html.parser")

        # type (check once again)
        type_label = subSoup.find(text="Product Type:")
        try:
            type_value = type_label.findNext("dd").contents[0]
            if not str(type_value).find(COI):
                pass
        except:
            pass

        # timestamp
        announcement_date_label = subSoup.find(text="Company Announcement Date:")
        announcement_date_value = announcement_date_label.findNext("dd").contents[0].contents[0]
        announcement_date_timestamp = calendar.timegm(time.strptime(announcement_date_value, '%B %d, %Y'))

        # brand
        brand_label = subSoup.find(text="Brand Name:")
        brand_val = brand_label.findNext("dd").find(class_="field--item").contents[0]

        # company
        company_label = subSoup.find(text="Company Name:")
        company_value = company_label.findNext("dd").contents[  0]

        # description
        description_label = subSoup.find(text="Product Description:")
        description_val = description_label.findNext("dd").find(class_="field--item").contents[0]

        # recallReason
        recall_reason_label = subSoup.find(text="Reason for Announcement:")
        recall_reason_val = recall_reason_label.findNext("dd").find(class_="field--item").contents[0]

        bodyText = str(subSoup.find(class_="col-md-8 col-md-push-2")).replace('-', '')
        # print(bodyText)
        upc_matches = re.findall('[0-9]{12,16}', bodyText)

        # image to nigel function and find upc from the image
        # append upc to upc_matches
        # download any images


        image_array = [(FDA_URL + x.get('src')) for x in subSoup.find_all(class_="img-responsive")]
        for img_url in image_array:
            img = Image.open(requests.get(img_url, stream=True).raw)

            try:
                path = "/var/www/html/media/" + img_url.split("?")[0].split("public/")[1];
            except:
                pass

            try:
                img.save(path)
            except:
                pass

            try:
                imread_upc = extract_barcode(path)
                if imread_upc != -1:
                    upc_matches.append(imread_upc)
            except:
                pass

        if len(upc_matches) == 0:
            upc_matches.append("UNAVAILABLE")

        row_list = []
        for upc in upc_matches:
            row_list = [upc, announcement_date_timestamp, brand_val, company_value, description_val, recall_reason_val, url]
            filewriter.writerow(row_list)

    csvfile.close()

