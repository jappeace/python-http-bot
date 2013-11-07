from requests import get, codes
class hyperTexter:
	def __init__(self):
		self.mail = str('http://mailinator.com')
	def vote(self, name):
		print ('creating inbox for ' + name)
		if get(self.mail + '/inbox.jsp',params={'to' : name }).status_code != codes.ok:
			return False
		print('succes')
		return True

