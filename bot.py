from requests import get, codes, post
class hyperTexter:
	__mail = 'http://mailinator.com'
	__vote = 'http://restaurantverkiezing.nl'
	def vote(self, name):
		print ('creating inbox for ' + name)
		if get(self.__mail + '/inbox.jsp',params={'to' : name }).status_code != codes.ok:
			return False
		rep = post(self.__vote + '/state8/flow20551',
				params = {
					'form_id' : 'beoordelen',
					'mField2' : '10',
					'mField3' : '10',
					'mField6' : '10',
					'mField7' : '10',
					'mField40' : '',
					'mField41' : ''
				})
		print(rep.read())
		return True

