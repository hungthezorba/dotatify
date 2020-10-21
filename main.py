import requests
from bs4 import BeautifulSoup

r = requests.get('https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches')
soup = BeautifulSoup(r.content)
tables = soup.find_all('table', {'class' : 'wikitable wikitable-striped infobox_matches_content'})
match = tables[0]
for child in tables:
	if ('496' in child.findChild().text):
		matchInfo = child.findChild().text.split('\n')
		for element in matchInfo:
			if element == '':
				matchInfo.remove('');
		print (matchInfo)