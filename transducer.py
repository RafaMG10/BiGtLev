

class transducer:
	# "order - num of the transducer"
	# rectification - rectication of the phase, this has to be depend on one transducer
	# phase is the phase of the transducer
	# position - real position of the transducer (x,y,z) in metres

	def __init__(self,order, rectification, phase, position):
		self.order = order
		self.rectification = rectification
		self.phase = phase
		self.position = position

	# getter and setter
	def getOrder(self):
		return self.order
	def getRectification(self):
		return self.rectification
	def getPhase(self):
		return self.phase
	def getPosition(self):
		return self.position
	def setOrder(self,order):
		self.order = order
	def setRectification(self, rectification):
		seft.rectification = rectification
	def setPhase(self, phase):
		self.phase = phase
	def setPosition(self,position):
		self.position = position


def arrayPosition(position):
	for i in range(3):
		for j in range(3):
			x = (j) 
			y = (i) 
			position.append([x,y])
def translateNewPosition(vector,positions):
	pos = 0
	for i in positions:
		positions[pos] = [i[0] + vector[0], i[1] + vector[1]] 
		pos = pos + 1

if __name__ == '__main__':

	transd = transducer(0,1,0.2,[0.002,0.003,0.004])

	print transd.getOrder()
	print transd.getRectification()
	print transd.getPhase()
	print transd.getPosition()

	position = []

	x = (16.5 * 7) + 0.25
	x = 2
	newPos = [x,-x]
	arrayPosition(position)
	print position
	translateNewPosition(newPos,position)
	print 'new position'
	print position
