from abc import ABCMeta
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
		__current = __current + 1 % __pages.size
		return self.__url + __pages[(__current)]
class page(rstring):
	__path = ''
	def __init__(self, path):
		self.__path = path
	def __str__(self):
		return __path
