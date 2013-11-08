from requests import get, codes, post
from structure import site, page
class hyperTexter:
	__mail = site('http://mailinator.com')
	__vote = site('http://restaurantverkiezing.nl')
	def vote(self, name):
		print ('creating inbox for ' + name)
		self.__mail.add(page('/inbox.jsp'))
		if get(str(self.__mail),params={'to' : name }).status_code != codes.ok:
			return False
		self.__vote.add(page('/state8/flow20551'))
		cookieAcces = get(self.__vote)
		rep = post(str(self.__vote),
				params = {
					'form_id' : 'beoordelen',
					'mField2' : '10',
					'mField3' : '10',
					'mField6' : '10',
					'mField7' : '10',
					'mField40' : '',
					'mField41' : ''
				})
		print(rep.status_code, rep.headers)
		return True
