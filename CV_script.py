#pip install opencv-python
#pip install numpy

import cv2
import time
import numpy as np
from collections import deque

def main():
	#lower and upper boundaries of green
	sensitivity = 25 # larger sensitivity -> more shit is classified as green
	greenLower = (60-sensitivity, 100, 50)
	greenUpper = (60+sensitivity, 255, 255)
	
    # grab video capture from webcam
	capture = cv2.VideoCapture(0)
	# let camera start up
	time.sleep(2.0)
	while True:
		# grab a frame
		ret, frame = capture.read()
		
		# CV preprocessing
		blurred = cv2.GaussianBlur(frame, (5, 5), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		
		# CV mask -> coordinate
		'''
		Note there is lots of ways of doing this...
		Here are the possibilities:
			Hough Circles - Our thresholding isn't accurate enough for this. (See below implementation)
			K-Means/DBSCAN/GMM - Needs manual implementation (native support clusters based on color not pixels)
			Partition - Must port code to C++ to use this (https://stackoverflow.com/questions/19114287/c-and-opencv-clustering-white-pixels-algorithm)
		'''
		# BELOW IS CONTOUR IMPLEMENTATION
		# THIS IMPLEMENTATION HAS THE BEST PERFORMANCE
		img, contours, hier = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			if 500<cv2.contourArea(cnt)<5000:
				M = cv2.moments(cnt)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
		'''
		# BELOW IS HOUGH CIRCLES IMPLEMENTATION.
		# THIS IMPLEMENTATION HAS POOR PERFORMANCE :^(
		circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT,1,minDist=20,param1=50,param2=10,minRadius=0,maxRadius=0)
		if circles is not None:
			print('cars detected!')
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
		'''
		
		# Let us view the results in real time
		cv2.imshow("raw", frame)
		cv2.imshow("mask", mask)
		
		# exit the program using 'esc'
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			capture.release()
			break

if __name__ == "__main__":
	main()