import serial

class Robot:

	# serial port communication
	ser = serial.Serial('/dev/ttyS0');
	
	# colors available - three available, must be unique for every instance
	types = ['red', 'green', 'blue']

	def __init__(self, rID, xInit, yInit):
		self.rID = rID
		self.lastX = xInit
		self.lastY = yInit
		self.type = self.types.pop()

	#def get_position(self):
		
	
	# write a move command to serial
	#def move(self, dx, dy):	
