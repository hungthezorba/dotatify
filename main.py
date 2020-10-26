import requests
import copy
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

datetime = datetime
r = requests.get('https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches')
soup = BeautifulSoup(r.content, 'html.parser')
tables = soup.find_all('table', {'class' : 'wikitable wikitable-striped infobox_matches_content'})
preProcessMatches = []
matches = []
nextMatch = {
	'teamLeft': '',
	'teamRight': '',
	'bestOf': '',
	'time': '',
	'tournament': ''
}
index = 0
for child in tables:
	if ('496' in child.findChild().text and 'vs' in child.findChild().text): #Retrieving upcoming match
		preProcessMatches.append(child.findChild())
		index+=1


for match in preProcessMatches:
	nextMatch['teamLeft'] = match.find_all('a')[0].text
	nextMatch['teamRight'] = match.find_all('a')[3].text
	nextMatch['bestOf'] = match.find_all('td')[1].text.replace('\n','')
	time = match.find_all('span', {'class' : 'timer-object'})[0].contents[0].split(' ')
	processedTime = (datetime.strptime(time[4], '%H:%M') + timedelta(hours=7))
	processedTime = "{:d}:{:02d}".format(processedTime.hour, processedTime.minute)
	nextMatch['time'] = processedTime
	nextMatch['tournament'] = match.find_all('a')[5].text
	matches.append(copy.copy(nextMatch))
print (matches)
		