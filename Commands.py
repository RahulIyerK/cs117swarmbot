import serial

class Robot:

	# serial port communication
	ser = serial.Serial('/dev/tty15');
	
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
		coord, angle = camera.get_location(self.type)
		self.theta = angle
		self.lastX = coord[0]
		self.lasty = coord[1]
	
	# write a move command to serial
	def move(self, dx, dy, dtheta):	
		self.ser.write(bytes('< '+str(self.rID)+' '+str(dx)+' '+str(dy)+str(dtheta)+' >','utf-8'))

	# wait until a done signal is received, update position
	def wait(self):
		self.ser.read_until('< done >')
