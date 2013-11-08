from requests import get, codes, post
from structure import site
class hyperTexter:
	__mail = site('http://mailinator.com')
	__vote = site('http://restaurantverkiezing.nl')

	def __init__(self):
		self.__mail.add('/inbox.jsp')
		self.__vote.add('/')
		self.__vote.add('/selecteer/dv/restaurantdegrillerije')
		self.__vote.add('/state8/flow20551')

	def vote(self, name):
		vote = self.__vote
		mail = self.__mail
		print ('creating inbox for ' + name)
		if get(mail.page(),params={'to' : name }).status_code != codes.ok:
			return False

		print ('getting cookie')
		cookieAcces = get(vote.page())
		if cookieAcces.status_code != codes.ok:
			return False
		vote.cookie = cookieAcces.cookies["PHPSESSID"]
		vote.nxt()

		print('selecting the restaurant')
		if get(vote.page(), cookies=vote.cookie).status_code != codes.ok:
			return False
		vote.nxt()

		print('putting in score fields')
		rep = post(vote.page(),
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
