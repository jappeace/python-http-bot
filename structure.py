class site:
	def __init__(self, url):
		self.__pages = []
		self.__current = 0
		self.__url = url
	def add(self, page):
		self.__pages.append(page)
	def addAll(self, pages):
		self.__pages.extend(pages)
	def nxt(self):
		self.__current += 1
		if self.__current >= len(self.__pages):
			self.reset()
			return False
		return True
	def page(self):
		return self.__url + self.__pages[self.__current]
	def reset(self):
		self.__current = 0
