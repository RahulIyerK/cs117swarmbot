from Commands import Robot
from CV_script_with_classes import CV_input
import cv2

def main():
	
	# setup camera
	camera = CV_input()

	# setup robots
	
	r1 = Robot('arjun',0,0,0, camera)

	r2 = Robot('debby',1,0,0, camera)

	r3 = Robot('qianru',2,0,0, camera)

	# run command loop
	while camera.initialized != 1:
		camera.update()
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			camera.delet()
			break
	while True:
		# update positions
		camera.update()

		r1.move(1,0,0)
		r2.move(1,0,0)
		r3.move(1,0,0)

		# wait for command to finish	
		r1.wait()
		#r2.wait()
		#r3.wait()
		intrrpt = cv2.waitKey(30) & 0xff
		if intrrpt == 27:
			camera.delet()
			break

if __name__ == "__main__":
	main()
