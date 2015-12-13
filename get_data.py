import sys
import yaml #pip install pyyaml
from attrdict import AttrDict
import requests #requests library will give you less butthurt than urllib
import json
import os

# Read default.yaml file. Translate .yaml -> dict
with open('default.yaml', 'r') as d:
	default = yaml.load(d.read())

# Read config.yaml file. 
with open('config.yaml', 'r') as c:
	config = yaml.load(c.read())
	cf = AttrDict(config)

	# Ensure that mandatory values have been provided. Raise exception/print message and stop if not.
	try:
		cf.source.leagues and cf.source.API_key in cf	
	except:
		print "Add data to config.yaml file and come back!"
		sys.exit()
		
# Config data overrides defaults
with open('yamls.txt', 'w') as y:
	if cmp(default, config) == -1:
		y.writelines(str(config))

with open('yamls.txt', 'r') as y:
	yam = AttrDict(yaml.load(y.read()))

	# API key should be provided as custom request header
	# Download entry-point data from source. Respect API key from config
	req_soccerseasons = requests.get(yam.source.base_url, headers={'X-Auth-Token': yam.source.API_key, 'X-Response-Control': 'minified'})
	
	# Store all obtained data locally in plain files
	with open('soccerseasons.txt', 'w') as s:
		s.writelines(req_soccerseasons.text)

		
	# Build dependecies for further downloads
	soccerseasons = req_soccerseasons.json()
	# Your code should not query API if data is already available locally
	if (os.stat('teams.txt').st_size == 0 and os.stat('leagues.txt').st_size == 0 and os.stat('leagues.txt').st_size == 0):
		for s in soccerseasons:
			#get teams
			req_teams = requests.get(yam.source.base_url + '{}/teams'.format(s['id']), headers={'X-Auth-Token': yam.source.API_key, 'X-Response-Control': 'minified'})
			teams = req_teams.json()
			with open('teams.txt', 'a+') as t:
				t.writelines(str(teams))
				t.writelines('\n')

			#get leaguetable
			req_leaguetable = requests.get(yam.source.base_url + '{}/leagueTable'.format(s['id']), headers={'X-Auth-Token': yam.source.API_key, 'X-Response-Control': 'minified'})
			leagues = req_leaguetable.json()
			with open('leagues.txt', 'a+') as lg:
				lg.writelines(str(leagues))
				lg.writelines('\n')

			#get fixtures
			req_fixtures = requests.get(yam.source.base_url + '{}/fixtures'.format(s['id']), headers={'X-Auth-Token': yam.source.API_key, 'X-Response-Control': 'minified'})
			fixtures = req_fixtures.json()
			with open('fixtures.txt', 'a+') as f:
				f.writelines(str(fixtures))
				f.writelines('\n')






	

