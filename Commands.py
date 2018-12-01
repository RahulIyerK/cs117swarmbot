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
		self.type = self.types.pop()

	# use opencv code to get current position of the robot
	def get_position(self):
		return get_location(self.type)
	
	# write a move command to serial
	def move(self, dx, dy):	
		self.ser.write(bytes(''+str(self.rID)+' '+str(dx)+' '+str(dy)+'\n','utf-8'))
