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
		self.__vote.add('/state9/flow20551')
		self.__vote.add('/emaillogin/state9/flow20551')

	def vote(self, name):
		vote = self.__vote
		mail = self.__mail
		print ('creating inbox for ' + name, mail.page())
		if get(mail.page(),params={'to' : name }).status_code != codes.ok:
			return False

		print ('getting cookie', vote.page())
		cookieAcces = get(vote.page())
		if cookieAcces.status_code != codes.ok:
			return False
		vote.cookie = dict(PHPSESSID = cookieAcces.cookies["PHPSESSID"])
		vote.nxt()

		print('selecting the restaurant',vote.page())
		if get(vote.page(), cookies=vote.cookie).status_code != codes.ok:
			return False
		vote.nxt()
		if not self.simpleGet(vote):
			return False

		print('putting in score fields', vote.page())
		if post(vote.page(),
				params = {
					'form_id' : 'beoordelen',
					'mField2' : '10',
					'mField3' : '10',
					'mField6' : '10',
					'mField7' : '10',
					'mField40' : '',
					'mField41' : ''
				},
				cookies=vote.cookie
			).status_code != codes.ok:
			return False
		vote.nxt()

		print('\'chosing\' mail', vote.page())
		if not self.simpleGet(vote):
			return False
		vote.nxt()

		print('\'opening\' registery page', vote.page())
		if not self.simpleGet(vote):
			return False
		vote.nxt()
		return True

	def simpleGet(self, page):
		return get(page.page(), cookies=page.cookie).status_code == codes.ok

