from CV_script import get_location
import serial

class Robot:

	# serial port communication
	ser = serial.Serial('/dev/ttyUSB0');
	
	# colors available - three available, must be unique for every instance
	types = ['red', 'green', 'blue']

	def __init__(self, rID, xInit, yInit):
		self.rID = rID
		self.lastX = xInit
		self.lastY = yInit
		self.theta = 0
		self.type = self.types.pop()

	# use opencv code to get current position of the robot
	def get_position(self):
		coord, angle = get_location(self.type)
		self.theta = angle
		self.lastX = coord[0]
		self.lasty = coord[1]
	
	# write a move command to serial
	def move(self, dx, dy):	
		self.ser.write(bytes('<'+str(self.rID)+','+str(dx)+','+str(dy)+str(self.theta)'>\n','utf-8'))

	# wait until a done signal is received, update position
	def wait(self):
		ser.read_until('<done>')
		self.get_position()
