from Commands import Robot
from CV_script_with_classes import CV_input

def main():
	
	# setup camera
	camera = CV_input()

	# setup robots
	
	r1 = Robot('arjun',0,0,0, camera)

	r2 = Robot('debby',1,0,0, camera)

	r3 = Robot('qianru',2,0,0, camera)

	# end flag and distance
	forwardFlag = True
	width = 400
	startX = 150

	# run command loop
	while camera.initialized != 1:
		camera.update()
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			camera.delet()
			break

	# run command loop
	while True:

		# move forward
		r1.move(10,0,0)
		r2.move(10,0,0)
		r3.move(10,0,0)

		# wait for command to finish	
		r1.wait()
		r2.wait()
		r3.wait()

		# update position
		camera.update()
		# update robot position
		r1.update_position()
		r2.update_position()
		r3.update_position()

		# check for end of slalom, and turn if necessary
		if((r1.lastX >= width and r2.lastX >= width and r3.lastX >= width)||(r1.lastX <= startX and r2.lastX <= startX and r3.lastX <= startX))

		# camera interrupt, necessary fr cv
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			camera.delet()
			break

if __name__ == "__main__":
	main()
