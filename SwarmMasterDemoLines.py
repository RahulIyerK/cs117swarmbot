from Robots import Robot
from CV_script_with_classes import CV_input

def main():
	
	# setup camera
	camera = CV_input()

	# setup robots
	
	Robot r1 = Robot('arjun',0,0,0, camera)

	Robot r2 = Robot('debby',1,0,0, camera)

	Robot r3 = Robot('qianu',2,0,0, camera)

	# run command loop
	while True:
		# update positions
		camera.update()
		r1.move(1,0,0)
		r2.move(1,0,0)
		r3.move(1,0,0)

		# wait for command to finish	
		r1.wait()
		r2.wait()
		r3.wait()

if __name__ == "__main__":
	main()
