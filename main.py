import requests
import copy
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from win10toast import ToastNotifier

r = requests.get('https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches')
soup = BeautifulSoup(r.content, 'html.parser')
tables = soup.find_all('table', {'class' : 'wikitable wikitable-striped infobox_matches_content'})
preProcessMatches = []
matches = []
matchData = {
	'teamLeft': '',
	'teamRight': '',
	'bestOf': '',
	'time': '',
	'tournament': ''
}

toaster = ToastNotifier()
index = 0
for child in tables:
	if ('496' in child.findChild().text and 'vs' in child.findChild().text): #Retrieving upcoming match
		preProcessMatches.append(child.findChild())
		index+=1


for match in preProcessMatches:
	matchData['teamLeft'] = match.find_all('a')[0].text
	matchData['teamRight'] = match.find_all('a')[3].text
	matchData['bestOf'] = match.find_all('td')[1].text.replace('\n','')
	time = match.find_all('span', {'class' : 'timer-object'})[0].contents[0].split(' ')
	processedTime = (datetime.strptime(time[4], '%H:%M') + timedelta(hours=7))
	processedTime = "{:d}:{:02d}".format(processedTime.hour, processedTime.minute)
	matchData['time'] = processedTime
	matchData['tournament'] = match.find_all('a')[5].text
	matches.append(copy.copy(matchData))

title = "Incoming 496 match"
nextMatch = matches[0]
message = nextMatch['teamLeft'] + ' ' + nextMatch['bestOf'] + ' ' +  nextMatch['teamRight'] + ' at ' + nextMatch['time'] + '\n' + nextMatch['tournament']
toaster.show_toast(title, message, duration=5)
		