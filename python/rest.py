import requests

class Rest:

	url = "http://localhost:8181/update"

	def wc1_free(self):
		payload = {"id" : "wc1", "state": "free"}
		print 'wc1 is free: '
		self.send_update(payload)

	def wc2_free(self):
		payload = {"id" : "wc2", "state": "free"}
		print 'wc2 is free: '
		self.send_update(payload)

	def urinal_free(self):
		payload = {"id" : "urinal", "state": "free"}
		print 'urinal is free: '
		self.send_update(payload)

	def wc1_occupied(self):
		payload = {"id" : "wc1", "state": "occupied"}
		print 'wc1 is occupied: '
		self.send_update(payload)

	def wc2_occupied(self):
		payload = {"id" : "wc2", "state": "occupied"}
		print 'wc2 is occupied: '
		self.send_update(payload)

	def urinal_occupied(self):
		payload = {"id" : "urinal", "state": "occupied"}
		print 'urinal is occupied: '
		self.send_update(payload)

	def send_update(self, msg):
		requests.put(self.url, json=msg)
		print 'send_update()'


# Tests 
#rest = Rest()

#rest.wc1_free()
#rest.wc2_free()
#rest.urinal_free()

#rest.wc1_occupied()
#rest.wc2_occupied()
#rest.urinal_occupied()
