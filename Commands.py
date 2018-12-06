import serial
import time

class Robot:

	# serial port communication
	ser = serial.Serial('COM4', 9600);
	
	# colors available - three available, must be unique for every instance
	types = ['red', 'blue', 'green']

	def __init__(self, rID, xInit, yInit, theta, camera):
		self.rID = rID
		self.lastX = xInit
		self.lastY = yInit
		self.theta = theta
		self.camera = camera
		self.type = self.types.pop()

	# use opencv code to get current position of the robot
	def update_position(self):
		out = self.camera.get_location(self.type)
		coord, angle = out[0], out[1]
		self.theta = angle
		self.lastX = coord[0]
		self.lasty = coord[1]
	
	# write a move command to serial
	def move(self, dx, dy, dtheta):
		print('< '+str(self.rID)+' '+str(dx)+' '+str(dy) + ' ' +str(dtheta)+' >')
		self.ser.write(bytes('< '+str(self.rID)+' '+str(dx)+' '+str(dy) + ' ' +str(dtheta)+' >','ascii'))

	# wait until a done signal is received, update position
	def wait(self):
		print('start wait')
		while(self.ser.inWaiting() < 1):
			# update camera position to preserve averages
			self.camera.update()
			time.sleep(0.5)
		self.ser.read_until(b'< done >')
		print('end wait')
		self.update_position()
