import requests

class Rest:

	url = "http://localhost:8181/update"

	def wc1_free(self):
		payload = {"id" : "wc1", "state": "Free"}
		print 'wc1 is free: '
		self.send_update(payload)

	def wc2_free(self):
		payload = {"id" : "wc2", "state": "Free"}
		print 'wc2 is free: '
		self.send_update(payload)

	def urinal_free(self):
		payload = {"id" : "urinal", "state": "Free"}
		print 'urinal is free: '
		self.send_update(payload)

	def wc1_occupied(self):
		payload = {"id" : "wc1", "state": "Occupied"}
		print 'wc1 is occupied: '
		self.send_update(payload)

	def wc2_occupied(self):
		payload = {"id" : "wc2", "state": "Occupied"}
		print 'wc2 is occupied: '
		self.send_update(payload)

	def urinal_occupied(self):
		payload = {"id" : "urinal", "state": "Occupied"}
		print 'urinal is occupied: '
		self.send_update(payload)

	def send_update(self, msg):
		requests.put(self.url, json=msg)
		print 'send_update()'

