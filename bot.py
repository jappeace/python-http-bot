from requests import get, codes, post, exceptions
from structure import site
from random import choice
import string
from time import time, sleep
from json import loads
from bs4 import BeautifulSoup
from subprocess import call

class hyperTexter:
	__mail = site('http://mailinator.com')
	__vote = site('http://restaurantverkiezing.nl')

	def __init__(self):
		self.__mail.addAll([
			'/inbox.jsp',
			'/set',
			'/grab',
			'/rendermail.jsp'
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
		print ('creating inbox for ' + name)
		if get(mail.page(),params={'to' : name }).status_code != codes.ok:
			return False

		print ('getting cookie')
		cookieAcces = get(vote.page())
		if cookieAcces.status_code != codes.ok:
			return False
		vote.cookie = {'PHPSESSID' : cookieAcces.cookies["PHPSESSID"]}
		vote.nxt()

		print('selecting the restaurant')
		if not self.simpleGet(vote):
			return False
		vote.nxt()

		print('putting in score fields')
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

		email = name + '@' + choice([
			'mailtothis.com', 'mailinator.net',
			'spamgoes.in', 'mailismagic.com',
			'reallymymail.com', 'sogetthis.com', 'monumentmail.com'])
		print('posting mail adress to: ' + email)
		if post(vote.page(),
			data={
				'form_id' : 'inloggen',
				'mField1' : name,
				'mField5___email1_bChanged' : '1',
				'mField5___email1_sText' : 'e-mailadres',
				'mField5___email1' : email,
				'mField5___email2_bChanged' : '1',
				'mField5___email2_sText' : 'herhaal e-mailadres',
				'mField5___email2' : email
			}, cookies=vote.cookie).status_code != codes.ok:
			return False
		vote.nxt()

		print('deciding not to share')
		post(vote.page(), cookies=vote.cookie, data={
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
		if post(vote.page(), cookies=vote.cookie,
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
		if post(vote.page(), cookies=vote.cookie, data={
				'form_id' : 'step3first',
				'iPartner' : '501052'
				}).status_code != codes.ok:
			return False


		print('getting the address (mailinator crappy security)')
		temp = str(round(time() * 10000))
		try:
			mail.nxt()
			address = loads(get(mail.page(), params={
				'box' : name,
				'time' : temp
				}).text)["address"]
		except KeyError:
			#mailinator needs script to timeout so I change the wireless
			print("Changing network")
			self.switchNetwork()
			return False
		print('getting mailbox')
		mail.nxt()
		emailId = self.searchMail(get(mail.page(), params={
			'address' : address,
			'inbox' : name,
			'time' : temp
			}))
		mail.nxt()

		print("getting the correct email")
		email = BeautifulSoup(get(mail.page(), params={
			"msgid" : emailId,
			"time" : temp
			}).text.encode('utf8'))

		print('parsing mail and clicking the link')
		link = email.a.get('href')
		if(link == "/"):
			print('clicking failed')
			print(str(emailId))
			return False
		return get(link).status_code == codes.ok

	def simpleGet(self, site):
		return get(site.page(), cookies=site.cookie).status_code == codes.ok

	def searchMail(self, response):
		inbox = loads(response.text)
		for email in inbox["maildir"]:
			if email['subject'] == "Bevestig nu je stem op Restaurant De Grillerije":
				return email["id"]
		return "not found"

	def switchNetwork(self):
		nmoutput = commands.getoutput("nm-tool")
		searcher = "Wireless Access Points (* = current AP)"

		# slice out the wireless section only (excluding the title above)
		slicedoutput = nmoutput[nmoutput.find(searcher)+len(searcher):]

		trimmed_to_current = slicedoutput[slicedoutput.find("*")+1:]

		if "Klooster" == trimmed_to_current[:trimmed_to_current.find(":")]:
			call("nmcli dev wifi connect ARV7519C72EE5 password 1578A57BCE38", shell=True)
		else:
			call("nmcli dev wifi connect Klooster password 1234554321", shell=True)
