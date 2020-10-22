import requests
from bs4 import BeautifulSoup

r = requests.get('https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches')
soup = BeautifulSoup(r.content)
tables = soup.find_all('table', {'class' : 'wikitable wikitable-striped infobox_matches_content'})

matches = []
index = 0
for child in tables:
	if ('496' in child.findChild().text and 'vs' in child.findChild().text): #Retrieving upcoming match
		matches.append(child.findChild().text.split('\n'))
		matches[index] = [elem.strip() for elem in matches[index] if elem != '']
		index+=1
		
print(matches)