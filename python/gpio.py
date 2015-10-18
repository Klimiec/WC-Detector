
class GPIO:
	def __init__(self):
		print 'run constructor'

	def isDoorWc1Closed(self):
		return True
	def isMoveDetectedInWc1(self):
		return True

	def isDoorWc2Closed(self):
		return True
	def isMoveDetectedInWc2(self):
		return True

	def turnOnLedWc1(self):
		print 'LED in WC1 is turned on'

	def turnOffLedWc1(self):
		print 'LED in WC1 is turned off'

	def turnOnLedWc2(self):
		print 'LED in WC2 is turned on'
		
	def turnOffLedWc2(self):
		print 'LED in WC2 is turned off'

	def turnOnLedUrinal(self):
		print 'LED in Urinal is turned on'
		
	def turnOffLedUrinal(self):
		print 'LED in Urinal is turned off'

	def turnOnFun(self):
		print 'Fun in wc1 is turned on'

	def turnOffFun(self):
		print 'Fun in wc1 is turned off'

	def getDistance(self):
		return 40