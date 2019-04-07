from html.parser import HTMLParser
import requests
from urllib import parse


def webscrapper(url):
	try :	
		res = requests.get(url)
		res.encoding = 'UTF-8'
		webscrape = res.text

		return webscrape
	except :
		print("Error occurred")



queue = set()
crawled = set()

second = set()

URL = 'https://www.dragzon.com'
crawled.add(URL)



class PageLinks(HTMLParser):
	def __init__(self):
		super().__init__()
		self.link = set()
		self.match = False
		self.web = ''
		
	def feeder(self,web):
		self.web = web
		self.feed(web)

	def handle_starttag(self,tags,attr):
		if 'a' in tags:
			for(attribute,value) in attr:
				if attribute == 'href':
					url = parse.urljoin(URL,value)
					self.link.add(url)
		if tags == 'title':
			self.match = True

	def handle_data(self,data):
		if self.match == True:
			data = data.replace('/','')
			filename = './Testing/' + data.replace('|','') + '.html'
			with open(filename,'w') as blob:
				blob.write(self.web)
				blob.close()			
			self.match = False

	def returnSet(self):
		return self.link.copy()

web = webscrapper(URL)

linker = PageLinks()
linker.feeder(web)

queue = linker.returnSet()

for x in queue:
	crawled.add(x)
	webscrape = webscrapper(x)
	linker.feeder(webscrape)
	print('Crawled : ' + str(len(crawled)) + 'Left : ' + str(len(queue)-len(crawled)) )

second = linker.returnSet()

	
print(queue)	
print(crawled)
print(second)

	