import cv2
import time
import numpy as np
from collections import deque

# threshold based on color
def create_mask(hsv, greenLower, greenUpper):
	mask = cv2.inRange(hsv, greenLower, greenUpper)
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
def find_centers(mask):
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
	min_size = 10
	max_size = 500
	img, contours, hier = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		if min_size < cv2.contourArea(cnt) < max_size:
			M = cv2.moments(cnt)
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			centers.append(np.array([cX,cY]))
	return centers

# find the closest point_ in points to point and return the index of that point_ and the distance
def closest_dist(point, points):
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

# Interface: we return the coordinate and theta of the robot :)
# input: 'red', 'green', or 'blue'
# output: coordinate (numpy array of length 2) and angle (float) of robot
def get_location(robot_id):
	# lower and upper boundaries of colors
	sensitivity = 10 # larger sensitivity -> more shit is classified as green
	dist_threshold = 50 # dist threshold :)
	greenLower = (60-sensitivity, 100, 50)
	greenUpper = (60+sensitivity, 255, 255)
	redLower = (175-sensitivity,20,70)
	redUpper = (175+sensitivity,255,255)
	blueLower = (105-sensitivity,50,38)
	blueUpper = (105+sensitivity,255,255)
	
	# define default robot positions
	num_points_red_robot = 2
	num_points_green_robot = 0
	num_points_blue_robot = 1
	blue_robot = []
	red_robot = []
	green_robot = []
    	# grab video capture from webcam
	capture = cv2.VideoCapture(0)
	# let camera start up
	time.sleep(2.0)

	# look for relevant points until we find it
	while not(len(blue_robot) == num_points_blue_robot and len(red_robot) == num_points_red_robot and len(green_robot) == num_points_green_robot):
		# grab a frame
		ret, frame = capture.read()
		
		# CV preprocessing
		blurred = cv2.GaussianBlur(frame, (5, 5), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		mask_red = create_mask(hsv, redLower, redUpper)
		mask_green = create_mask(hsv, greenLower, greenUpper)
		mask_blue = create_mask(hsv, blueLower, blueUpper)
		
		# CV mask -> coordinate		
		centers_red = find_centers(mask_red)
		centers_green = find_centers(mask_green)
		centers_blue = find_centers(mask_blue)
		
		# update robot locations
		for center in centers_green:
			min_dist, min_idx = closest_dist(center, green_robot)
			if min_dist < dist_threshold and min_idx != -1:
				green_robot[min_idx] = center
			elif len(green_robot) < num_points_green_robot:
				green_robot.append(center)			
		for center in centers_red:
			min_dist, min_idx = closest_dist(center, red_robot)
			if min_dist < dist_threshold and min_idx != -1:
				red_robot[min_idx] = center
			elif len(red_robot) < num_points_red_robot:
				red_robot.append(center)
		for center in centers_blue:
			min_dist, min_idx = closest_dist(center, blue_robot)
			if min_dist < dist_threshold and min_idx != -1:
				blue_robot[min_idx] = center
			elif len(blue_robot) < num_points_blue_robot:
				blue_robot.append(center)

	if robot_id == 'red':
		vec = red_robot[0]+red_robot[1]
	elif robot_id == 'green':
		vec = green_robot[0]+green_robot[1]
	elif robot_id == 'blue':
		vec = blue_robot[0]+blue_robot[1]
	theta = np.arctan(vec[0],vec[1])
	coord = vec/2
	return coord, theta

def main():
	# lower and upper boundaries of colors
	sensitivity = 10 # larger sensitivity -> more shit is classified as green
	dist_threshold = 50 # dist threshold :)
	greenLower = (60-sensitivity, 100, 50)
	greenUpper = (60+sensitivity, 255, 255)
	redLower = (175-sensitivity,20,70)
	redUpper = (175+sensitivity,255,255)
	blueLower = (105-sensitivity,50,38)
	blueUpper = (105+sensitivity,255,255)
	
	# define default robot positions
	num_points_red_robot = 2
	num_points_green_robot = 0
	num_points_blue_robot = 1
	blue_robot = []
	red_robot = []
	green_robot = []
	
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
		mask_red = create_mask(hsv, redLower, redUpper)
		mask_green = create_mask(hsv, greenLower, greenUpper)
		mask_blue = create_mask(hsv, blueLower, blueUpper)
		
		# CV mask -> coordinate		
		centers_red = find_centers(mask_red)
		centers_green = find_centers(mask_green)
		centers_blue = find_centers(mask_blue)
		
		# update robot locations
		for center in centers_green:
			min_dist, min_idx = closest_dist(center, green_robot)
			if min_dist < dist_threshold and min_idx != -1:
				green_robot[min_idx] = center
			elif len(green_robot) < num_points_green_robot:
				green_robot.append(center)			
		for center in centers_red:
			min_dist, min_idx = closest_dist(center, red_robot)
			if min_dist < dist_threshold and min_idx != -1:
				red_robot[min_idx] = center
			elif len(red_robot) < num_points_red_robot:
				red_robot.append(center)
		for center in centers_blue:
			min_dist, min_idx = closest_dist(center, blue_robot)
			if min_dist < dist_threshold and min_idx != -1:
				blue_robot[min_idx] = center
			elif len(blue_robot) < num_points_blue_robot:
				blue_robot.append(center)

		# change sensitivity once all the robots are found!
		if len(blue_robot) == num_points_blue_robot and len(red_robot) == num_points_red_robot and len(green_robot) == num_points_green_robot:
			sensitivity = 35 # larger sensitivity -> more shit is classified as green
			greenLower = (60-sensitivity, 100, 50)
			greenUpper = (60+sensitivity, 255, 255)
			redLower = (175-sensitivity,20,70)
			redUpper = (175+sensitivity,255,255)
			blueLower = (105-sensitivity,50,38)
			blueUpper = (105+sensitivity,255,255)
		
		# display points on screen
		for center in green_robot:
			cX = center[0]
			cY = center[1]
			cv2.circle(frame, (cX, cY), 7, (0, 255, 0), -1)
		for center in red_robot:
			cX = center[0]
			cY = center[1]
			cv2.circle(frame, (cX, cY), 7, (0, 0, 255), -1)
		for center in blue_robot:
			cX = center[0]
			cY = center[1]
			cv2.circle(frame, (cX, cY), 7, (255, 0, 0), -1)
		
		# Let us view the results in real time
		cv2.imshow("mask_red", mask_red)
		cv2.imshow("mask_green", mask_green)
		cv2.imshow("mask_blue", mask_blue)
		cv2.imshow("raw", frame)
		
		# exit the program using 'esc'
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			capture.release()
			break

if __name__ == "__main__":
	main()
