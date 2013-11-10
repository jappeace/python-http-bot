from requests import get, codes, post, exceptions
from structure import site
from subprocess import call

class hyperTexter:
	__mail = site('http://mailinator.com')
	__vote = site('http://restaurantverkiezing.nl')

	def __init__(self):
		self.__mail.add('/inbox.jsp')
		self.__vote.addAll([
				'/',
				'/selecteer/dv/restaurantdegrillerije',
				'/state8/flow20551',
				'/state9/flow20551',
				'/emaillogin/state9/flow20551',
				'/state10/flow20551',
				'/state11/flow20551',
				'/state12/flow20551', #no pink ribbon crap
				'/state13/flow20551', # serverside rederict
				'/state14/flow20551' #final page
			])
		self.counter = 0

	def start(self, name):
		try:
			return self.cycle(name)
		except exceptions.ConnectionError:
			return False
	def cycle(self, name):
		vote = self.__vote
		mail = self.__mail
		print ('creating inbox for ' + name, mail.page())
		if get(mail.page(),params={'to' : name }).status_code != codes.ok:
			return False

		print ('getting cookie', vote.page())
		cookieAcces = get(vote.page())
		if cookieAcces.status_code != codes.ok:
			return False
		vote.cookie = {'PHPSESSID' : cookieAcces.cookies["PHPSESSID"]}
		vote.nxt()

		print('selecting the restaurant',vote.page())
		if not self.simpleGet(vote):
			return False
		vote.nxt()

		print('putting in score fields', vote.page())
		if post(vote.page(),
				data = {
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
		self.simpleGet(vote)
		vote.nxt()

		print('\'opening\' registery page', vote.page())
		self.simpleGet(vote)

		email = name + '@mailtothis.com'
		print('posting mail adress to:' + email)
		if post(vote.page(),
			data={
				'form_id' : 'inloggen',
				'mField1' : name + '@mailtothis.com',
				'mField5___email1_bChanged' : '1',
				'mField5___email1_sText' : 'e-mailadres',
				'mField5___email1' : email,
				'mField5___email2_bChanged' : '1',
				'mField5___email2_sText' : 'herhaal e-mailadres',
				'mField5___email2' : email
			}, cookies=vote.cookie).status_code != codes.ok:
			return False
		vote.nxt()

		print('deciding not to share', vote.page())
		self.simpleGet(vote)

		post(vote.page(), cookies=vote.cookie, data={
			'form_id' : 'tellafriend'
			})
		vote.nxt()

		birthday = {
			'year' : '1990',
			'month':'11',
			'day':'10'
		}

		print('entering postcode, gender and birthdate', vote.page())
		self.simpleGet(vote)
		if post(vote.page(), cookies=vote.cookie,
			data={
				'form_id' : 'persoonsgegevens',
				'mField10' : '514651', #gender: 514651 is male 514652 is female
				'mField4___Part1' : '7776', #postalcode number
				'mField4___Part2' : 'aa', #postalcode letter
				'persoonsgegevens_mField11_iDay' : birthday['day'],
				'persoonsgegevens_mField11_iMonth' : birthday['month'],
				'persoonsgegevens_mField11_iYear' : birthday['year'],
				'mField11' : birthday['day'] + '-' + birthday['month'] + '-' + birthday['year']
			}).status_code != codes.ok:
			return False
		vote.nxt()

		print('not support pink ribbon (is more work)', vote.page())
		self.simpleGet(vote)
		if post(vote.page(), cookies=vote.cookie, data={
				'form_id' : 'step3first',
				'iPartner' : '501052'
				}).status_code != codes.ok:
			return False
		vote.nxt()
		self.simpleGet(vote)
		vote.nxt()
		print('now visiting final page wich tells us to confirm our vote', vote.page())
		Self.simpleGet(vote)

	def simpleGet(self, site):
		return get(site.page(), cookies=site.cookie).status_code == codes.ok
