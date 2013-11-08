from abc import ABCMeta, abstractmethod

class rstring(metaclass=ABCMeta):
	@abstractmethod
	def __str__(self):
		pass
	def __repr__(self):
		return self.__str__()

class site(rstring):
	__url = ''
	__pages = []
	__current = -1
	def __init__(self, url):
		self.__url = url
	def __str__(self):
		self.__current = (self.__current + 1) % len(self.__pages)
		return self.__url + str(self.__pages[(self.__current)])
	def add(self, page):
		self.__pages.append(page)

class page(rstring):
	__path = ''
	def __init__(self, path):
		self.__path = path
	def __str__(self):
		return self.__path
