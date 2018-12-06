#pip install opencv-python
#pip install numpy

import cv2
import time
import numpy as np
from collections import deque

class CV_input:
	def __init__(self):
		# lower and upper boundaries of colors
		sensitivity = 2 # larger sensitivity -> more shit is classified as green
		self.dist_threshold = 50 # dist threshold :)
		self.greenLower = (70-sensitivity, 100, 20)
		self.greenUpper = (70+sensitivity, 255, 255)
		# red has 2 hue ranges :(
		self.redLower_0 = (0,50,50)
		self.redUpper_0 = (sensitivity,255,255)
		self.redLower_1 = (180-sensitivity,50,50)
		self.redUpper_1 = (180,255,255)
		self.blueLower = (105-sensitivity,50,38)
		self.blueUpper = (105+sensitivity,255,255)
		
		# define default robot positions
		self.num_points_red_robot = 2
		self.num_points_green_robot = 2
		self.num_points_blue_robot = 2
		self.blue_robot = []
		self.red_robot = []
		self.green_robot = []
		self.initialized = 0
		
		# set default offsets
		self.offset_red = 0.
		self.offset_green = 0.
		self.offset_blue = 0.
		
		# grab video capture from webcam
		self.capture = cv2.VideoCapture(0)
		# let camera start up
		time.sleep(2.0)

	def update(self, view_flag = 1):
		# grab a frame
		ret, frame = self.capture.read()
		
		# CV preprocessing
		blurred = cv2.GaussianBlur(frame, (5, 5), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		mask_red = self.__create_mask(hsv, self.redLower_0, self.redUpper_0, self.redLower_1, self.redUpper_1)
		mask_green = self.__create_mask(hsv, self.greenLower, self.greenUpper)
		mask_blue = self.__create_mask(hsv, self.blueLower, self.blueUpper)
		
		# CV mask -> coordinate		
		centers_red = self.__find_centers(mask_red)
		centers_green = self.__find_centers(mask_green)
		centers_blue = self.__find_centers(mask_blue)
		
		# update robot locations
		for center in centers_green:
			min_dist, min_idx = self.__closest_dist(center, self.green_robot)
			if min_dist < self.dist_threshold and min_idx != -1:
				self.green_robot[min_idx] = center
			elif len(self.green_robot) < self.num_points_green_robot:
				self.green_robot.append(center)			
		for center in centers_red:
			min_dist, min_idx = self.__closest_dist(center, self.red_robot)
			if min_dist < self.dist_threshold and min_idx != -1:
				self.red_robot[min_idx] = center
			elif len(self.red_robot) < self.num_points_red_robot:
				self.red_robot.append(center)
		for center in centers_blue:
			min_dist, min_idx = self.__closest_dist(center, self.blue_robot)
			if min_dist < self.dist_threshold and min_idx != -1:
				self.blue_robot[min_idx] = center
			elif len(self.blue_robot) < self.num_points_blue_robot:
				self.blue_robot.append(center)

		# change sensitivity once all the robots are found!
		if (not self.initialized) and len(self.blue_robot) == self.num_points_blue_robot and len(self.red_robot) == self.num_points_red_robot and len(self.green_robot) == self.num_points_green_robot:
			sensitivity = 10 # larger sensitivity -> more shit is classified as green
			self.greenLower = (70-sensitivity, 100, 20)
			self.greenUpper = (70+sensitivity, 255, 255)
			# red has 2 hue ranges :(
			self.redLower_0 = (0,50,50)
			self.redUpper_0 = (sensitivity,255,255)
			self.redLower_1 = (180-sensitivity,50,50)
			self.redUpper_1 = (180,255,255)
			self.blueLower = (105-sensitivity,50,38)
			self.blueUpper = (105+sensitivity,255,255)
			# get all offsets
			self.offset_red = self.__find_offset(self.get_location('red')[1])
			self.offset_green = self.__find_offset(self.get_location('green')[1])
			self.offset_blue = self.__find_offset(self.get_location('blue')[1])		
			self.initialized = 1

		# Let us view the results in real time
		if view_flag:
			# display points on screen
			for center in self.green_robot:
				cX = center[0]
				cY = center[1]
				cv2.circle(frame, (cX, cY), 7, (0, 255, 0), -1)
			for center in self.red_robot:
				cX = center[0]
				cY = center[1]
				cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
			for center in self.blue_robot:
				cX = center[0]
				cY = center[1]
				cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
			cv2.imshow("mask_red", mask_red)
			cv2.imshow("mask_green", mask_green)
			cv2.imshow("mask_blue", mask_blue)
			cv2.imshow("raw", frame)
	
	# Interface: we return the coordinate and theta of the robot :)
	# input: 'red', 'green', or 'blue'
	# output: coordinate (numpy array of length 2) and angle (float) of robot
	def get_location(self, robot_id):
		if robot_id == 'red':
			if len(self.red_robot) != 2:
				return None
			vec_1 = self.red_robot[0]-self.red_robot[1]
			vec_2 = self.red_robot[0]+self.red_robot[1]
			theta = self.offset_red
		elif robot_id == 'green':
			if len(self.green_robot) != 2:
				return None
			vec_1 = self.green_robot[0]-self.green_robot[1]
			vec_2 = self.green_robot[0]+self.green_robot[1]
			theta = self.offset_green
		elif robot_id == 'blue':
			if len(self.blue_robot) != 2:
				return None
			vec_1 = self.blue_robot[0]-self.blue_robot[1]
			vec_2 = self.blue_robot[0]+self.blue_robot[1]
			theta = self.offset_blue
		theta += np.arctan2(vec_1[0],vec_1[1])*180/np.pi
		if theta < -180:
			theta += 360
		if theta > 180:
			theta -= 360
		coord = vec_2/2
		return [coord, theta]
	
	def delet(self):
		self.capture.release()

	# threshold based on color
	def __create_mask(self, hsv, colorLower, colorUpper, cL_2 = None, cU_2 = None):
		mask = cv2.inRange(hsv, colorLower, colorUpper)
		if cL_2 != None:
			mask_2 = cv2.inRange(hsv, cL_2, cU_2)
			mask = mask + mask_2
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		return mask
	
	'''
	Note there is lots of ways of doing this...
	Here are the possibilities:
		Hough Circles - Our thresholding isn't accurate enough for this. (See below implementation)
		K-Means/DBSCAN/GMM - Needs manual implementation (native support clusters based on color not pixels)
		Partition - Must port code to C++ to use this (https://stackoverflow.com/questions/19114287/c-and-opencv-clustering-white-pixels-algorithm)
	'''
	# BELOW IS CONTOUR IMPLEMENTATION
	# THIS IMPLEMENTATION HAS THE BEST PERFORMANCE
	def __find_centers(self, mask):
		'''
		# BELOW IS HOUGH CIRCLES IMPLEMENTATION.
		# THIS IMPLEMENTATION HAS POOR PERFORMANCE :^(
		circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT,1,minDist=20,param1=50,param2=10,minRadius=0,maxRadius=0)
			print('cars detected!')
		if circles is not None:
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
		'''
		centers = []
		min_size = 2
		max_size = 5000
		img, contours, hier = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			if min_size < cv2.contourArea(cnt) < max_size:
				M = cv2.moments(cnt)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				centers.append(np.array([cX,cY]))
		return centers

	# find the closest point_ in points to point and return the index of that point_ and the distance
	def __closest_dist(self, point, points):
		if len(points) == 0:
			return float('inf'), -1
		min_dist = float('inf')
		min_idx = -1
		for i, point_ in enumerate(points):
			dist = np.linalg.norm(point - point_)
			if dist < min_dist:
				min_dist = dist
				min_idx = i
		return min_dist, min_idx
	
	def __find_offset(self, theta):
		if theta >= 45 and theta < 135:
			offset = 90
		elif theta >= -45 and theta < 45:
			offset = 0
		elif theta >= -135 and theta < -45:
			offset = -90
		else:
			offset = 180
		return offset


def main():
	H = CV_input()
	while True:
		H.update()
		out = H.get_location('red')
		if out is not None:
			coord, theta = out[0], out[1]
			print("coord: (" + str(coord[0]) + ",\t" + str(coord[1]) + ")")
			print("theta: " + str(theta))
		
		# exit the program using 'esc'
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			H.delet()
			break

if __name__ == "__main__":
	main()
