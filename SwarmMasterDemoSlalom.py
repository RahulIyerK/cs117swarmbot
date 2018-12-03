from Commands import Robot
from CV_script_with_classes import CV_input

def main():
	
	# setup camera
	camera = CV_input()

	# setup robots
	
	r1 = Robot('arjun',0,0,0, camera)

	r2 = Robot('debby',1,0,0, camera)

	r3 = Robot('qianu',2,0,0, camera)

	# end flag and distance
	forwardFlag = True
	width = 400
	startX = 150

	# run command loop
	while True:
		# update positions
		camera.update()

		# find all initial positions
		while(not (camera.initialized == 1)):
			camera.update()

		# check flag
		if(forwardFlag):
			# move forward
			r1.move(width/2,0,0)
			r2.move(width/2,0,0)
			r3.move(width/2,0,0)
		else:	
			# move backward
			r1.move(-width/2,0,0)
			r2.move(-width/2,0,0)
			r3.move(-width/2,0,0)

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

		# check for end of slalom
		if(r1.lastX >= width and r2.lastX >= width and r3.lastX >= width)
			forwardFlag = False
		if(r1.lastX <= startX and r2.lastX <= startX and r3.lastX <= startX)
			forwardFlag = True

if __name__ == "__main__":
	main()
