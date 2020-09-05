import requests
import json
import os
import configparser
from mdutils import MdUtils
from datetime import datetime

config = configparser.ConfigParser()
config.read(os.environ['CONFIG'])

# Sam stuff
TRELLO_KEY = config['TRELLO']['KEY']
TRELLO_TOKEN = config['TRELLO']['TOKEN']

# Tech team board.
TECH_TEAM_ID = config['MAMAS']['TECH_TEAM']

# Cards in board.
IN_PROGRESS_ID = config['BOARDS']['IN_PROGRESS']
FINISHED_ID = config['BOARDS']['FINISHED']

# Headers
headers = {
	'Accept': 'application/json'
}

def jsonDump(one_card):
	print(json.dumps(one_card, sort_keys=True, indent=4, separators=(",", ": ")))

def cardReport(card):
	report = {}

	report['name'] = card['name']
	report['labels'] = list(map(lambda label: label['name'], card['labels']))

	actions = requests.request(
		'GET',
		'https://api.trello.com/1/cards/%s/actions'%(card['id']),
		headers=headers,
		params={
			'key': TRELLO_KEY,
			'token': TRELLO_TOKEN,
			'filter': 'commentCard'
		}
	)
	comments = actions.json()

	if (len(comments) > 0):
		report['recentComment'] = comments[0]['data']['text']
	else:
		report['recentComment'] = card['desc']

	memberList = []
	for memberId in card['idMembers']:
		member = requests.request(
			'GET',
			'https://api.trello.com/1/members/%s'%(memberId),
			headers=headers,
			params={
				'key': TRELLO_KEY,
				'token': TRELLO_TOKEN
			}
		)
		memberList.append(member.json()['fullName'])
	report['members'] = memberList

	return report

def generateMdFile(cardInfo):
	now = datetime.now()
	filename = now.strftime('%Y-%m-%d-%H-%M-%S')
	reportname = '%s-report'%(filename)

	print('Generating %s...'%(reportname))
	mdFile = MdUtils(file_name=reportname,title='Today\'s Trello Report')

	# Intro text
	mdFile.write('Hey tech-team! Here’s a snapshot of what we’re working on based on our current Trello! ')
	mdFile.write('If you have updates you want to give or are interested in following up with/joining some of this work,')
	mdFile.write('either ask here, message the folks on the task, or get in the Trello yourself and see what’s going on!')
	mdFile.new_line()
	mdFile.new_line()

	for card in cardInfo:
		# Card Title
		print('Creating entry for %s...'%(card['name']))
		mdFile.write('**%s**'%(card['name']))

		# Card Tags
		if (len(card['labels']) > 0):
			mdFile.write(' (')
			for i in range(len(card['labels'])):
				mdFile.write('%s'%(card['labels'][i]))
				if (i != len(card['labels'])-1):
					mdFile.write(', ')
			mdFile.write(')')

		# Names on the card
		if (len(card['members']) > 0):
			mdFile.write(' [')
			for i in range(len(card['members'])):
				mdFile.write('%s'%(card['members'][i]))
				if (i != len(card['members'])-1):
					mdFile.write(', ')
			mdFile.write(']')

		# Recent comment
		if (len(card['recentComment']) > 0):
			mdFile.write(': ')
			mdFile.write('%s'%card['recentComment'])
		else:
			mdFile.write(': No further information (someone should add some comments/users)!')

		# Lines between files
		mdFile.new_line()
		mdFile.new_line()

	# Create file
	mdFile.create_md_file()
	print('Done!')

response = requests.request(
	'GET',
	'https://api.trello.com/1/lists/%s/cards'%(IN_PROGRESS_ID),
	headers=headers,
	params={
		'key': TRELLO_KEY,
		'token': TRELLO_TOKEN
	}
)

in_progress_cards = json.loads(response.text)

cardInfo = list(map(lambda card: cardReport(card), in_progress_cards))

generateMdFile(cardInfo)
