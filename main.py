import requests
import copy
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from win10toast import ToastNotifier

def main():
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
		time = cleaningArray(match.find_all('span', {'class' : 'timer-object'})[0].contents[0].split(' '))
		processedTime = (datetime.strptime(time[0] + ' ' + time[1] + ' ' +  time[2] + ' ' + time[3], '%B %d %Y %H:%M') + timedelta(hours=7))
		processedTime = "{:d} {:d} {:d} {:d}:{:02d}".format(processedTime.month, processedTime.day, processedTime.year, processedTime.hour, processedTime.minute)
		matchData['time'] = processedTime
		matchData['tournament'] = match.find_all('a')[5].text
		matches.append(copy.copy(matchData))
	
	nextMatch = matches[0]
	#Notify a match in upcoming 1 hour
	if (datetime.now() + timedelta(hours=2) > datetime.strptime(nextMatch['time'], '%m %d %Y %H:%M')): 
		title = "Incoming 496 match"
		message = nextMatch['teamLeft'] + ' ' + nextMatch['bestOf'] + ' ' +  nextMatch['teamRight'] + ' at ' + nextMatch['time'] + '\n' + nextMatch['tournament']
		toaster.show_toast(title, message, duration=5)

def cleaningArray(array):
	removetable = str.maketrans('', '', '!@#$%^&*()-_=+[]{}"\'/?.,<>\\|')
	cleanedList = [s.translate(removetable) for s in array]
	cleanedList = [s for s in cleanedList if s != '']
	return cleanedList

if __name__=='__main__':
	main()	