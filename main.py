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
		'schedule': {
			'month': '',
			'day': '',
			'year': '',
			'time': ''
		},
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
		schedule = cleaningArray(match.find_all('span', {'class' : 'timer-object'})[0].contents[0].split(' '))
		processedSchedule = (datetime.strptime(schedule[0] + ' ' + schedule[1] + ' ' +  schedule[2] + ' ' + schedule[3], '%B %d %Y %H:%M') + timedelta(hours=7))
		# processedSchedule = "{:d} {:d} {:d} {:d}:{:02d}".format(processedSchedule.month, processedSchedule.day, processedSchedule.year, processedSchedule.hour, processedSchedule.minute)
		matchData['schedule']['month'] = processedSchedule.month
		matchData['schedule']['day'] = processedSchedule.day
		matchData['schedule']['year'] = processedSchedule.year
		matchData['schedule']['time'] = "{:d}:{:02d}".format(processedSchedule.hour, processedSchedule.minute)
		matchData['tournament'] = match.find_all('a')[5].text
		matches.append(copy.deepcopy(matchData))
			
	nextMatch = matches[0]
	schedule = str(nextMatch['schedule']['month']) + ' ' + str(nextMatch['schedule']['day']) + ' ' + str(nextMatch['schedule']['year']) + ' ' + str(nextMatch['schedule']['time'])
	#Notify a match in upcoming 1 hour
	# if (datetime.now() + timedelta(hours=1) > datetime.strptime(schedule, '%m %d %Y %H:%M')): 
	title = "Incoming 496 match"
	message = nextMatch['teamLeft'] + ' ' + nextMatch['bestOf'] + ' ' +  nextMatch['teamRight'] + ' at ' + nextMatch['schedule']['time'] + '\n' + nextMatch['tournament']
	toaster.show_toast(title, message, duration=5, threaded=None)

def cleaningArray(array):
	removetable = str.maketrans('', '', '!@#$%^&*()-_=+[]{}"\'/?.,<>\\|')
	cleanedList = [s.translate(removetable) for s in array]
	cleanedList = [s for s in cleanedList if s != '']
	return cleanedList

if __name__=='__main__':
	main()	