from requests import get, codes, post, exceptions, Session
from structure import site
from random import choice
import string
from time import time, sleep
from json import loads
from bs4 import BeautifulSoup
from subprocess import call, getoutput

class hyperTexter:
	__mail = site('http://www.fakemailgenerator.com')
	__vote = site('http://restaurantverkiezing.nl')

	def __init__(self):
		self.__mail.addAll([
			'/active.php',
			'/checkemail.php'
			])
		self.__vote.addAll([
				'/',
				'/selecteer/dv/restaurantdegrillerije',
				'/state8/flow20551',
				'/emaillogin/state9/flow20551',
				'/state10/flow20551',
				'/state11/flow20551',
				'/state12/flow20551', #no pink ribbon crap
				'/state13/flow20551', # serverside rederict
				'/state14/flow20551' #final page
			])

	def start(self, name):
		result = False
		try:
			result = self.cycle(name)
		except exceptions.ConnectionError:
			result = False
		self.__vote.reset()
		self.__mail.reset()
		return result
	def cycle(self, name):
		vote = self.__vote
		mail = self.__mail
		mail.s = Session()
		mail.d = choice(['jourrapide.com', 'teleworm.us', 'superrito.com', 'rhyta.com',
			'gustr.com', 'fleckens.hu', 'einrot.com', 'dayrep.com', 'cuvox.de', 'armyspy.com'])
		mail.add('/inbox/' + mail.d +'/'+ name.lower() + '/')
		print ('creating inbox for ' + name)
		if mail.s.get(mail.page(),params={'u' : name, 'd':'@'+ mail.d }).status_code != codes.ok:
			return False
		mail.nxt()
		if mail.s.get(mail.page(),params={'u' : name, 'd':'@' + mail.d }).status_code != codes.ok:
			return False

		print ('getting cookie')
		vote.s = Session()
		vote.s.get(vote.page())
		vote.nxt()

		print('selecting the restaurant')
		if not self.simpleGet(vote):
			return False
		vote.nxt()
		numb = ['7', '8', '8', '9', '9', '9','10','10','10','10']
		print('putting in score fields')
		if vote.s.post(vote.page(),
				data = {
					'form_id' : 'beoordelen',
					'mField2' : choice(numb),
					'mField3' : choice(numb),
					'mField6' : choice(numb),
					'mField7' : choice(numb),
					'mField40' : '',
					'mField41' : ''
				}
			).status_code != codes.ok:
			return False
		vote.nxt()

		email = name + '@' + mail.d
		print('posting mail adress to: ' + email)
		if vote.s.post(vote.page(),
			data={
				'form_id' : 'inloggen',
				'mField1' : name,
				'mField5___email1_bChanged' : '1',
				'mField5___email1_sText' : 'e-mailadres',
				'mField5___email1' : email,
				'mField5___email2_bChanged' : '1',
				'mField5___email2_sText' : 'herhaal e-mailadres',
				'mField5___email2' : email
			}).status_code != codes.ok:
			return False
		vote.nxt()

		print('deciding not to share')
		vote.s.post(vote.page(), data={
			'form_id' : 'tellafriend'
			})
		vote.nxt()

		print('entering postcode, gender and birthdate')
		birthday = {
			'year' : '19' + choice(['80', '81', '82', '83', '84',
				'85', '86', '87', '88', '89', '91', '90', '92', '93', '94', '95', '96', '97', '98', '99']),
			'month':choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']),
			'day':choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
				'16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28'])
		}
		if vote.s.post(vote.page(),
			data={
				'form_id' : 'persoonsgegevens',
				'mField10' : choice(['514651', '514652']), #gender: 514651 is male 514652 is female
				'mField4___Part1' : ''.join(choice(string.digits) for x in range(4)), #postalcode number
				'mField4___Part2' : ''.join(choice(string.ascii_uppercase) for x in range(2)), #postalcode letter
				'persoonsgegevens_mField11_iDay' : birthday['day'],
				'persoonsgegevens_mField11_iMonth' : birthday['month'],
				'persoonsgegevens_mField11_iYear' : birthday['year'],
				'mField11' : birthday['day'] + '-' + birthday['month'] + '-' + birthday['year']
			}).status_code != codes.ok:
			return False
		vote.nxt()

		print('not support pink ribbon (is more work)')
		if vote.s.post(vote.page(), data={
				'form_id' : 'step3first',
				'iPartner' : '501052'
				}).status_code != codes.ok:
			return False


		mail.nxt()

		print("getting the correct email")
		email = self.mailGet()
		if email == False:
			return False
		email = mail.s.get(email.find('iframe').get('src'))
		link = BeautifulSoup(email.text.encode('utf8')).a.get('href')
		print('parsing mail and clicking the link: '+ link)
		return get(link).status_code == codes.ok


	def simpleGet(self, site):
		if(hasattr(site, 's')):
			return site.s.get(site.page()).status_code == codes.ok
		else:
			return get(site.page(), cookies=site.cookie).status_code == codes.ok
	def mailGet(self, limit = 20):
		mail = self.__mail
		for x in range(0, limit):
			print ('attempting to get mail: ' + str(x))
			response = mail.s.get(mail.page())
			if response.url == mail.page():
				print('found it')
				return BeautifulSoup(response.text.encode('utf8'))
		return False
