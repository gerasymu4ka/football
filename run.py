# import http.client
import sys
import yaml #pip install pyyaml
from attrdict import AttrDict
import requests #requests library will give you less butthurt than urllib
import json

# Read default.yaml file. Translate .yaml -> dict
with open('default.yaml', 'r') as d:
	default = yaml.load(d.read())

# Read config.yaml file. 
with open('config.yaml', 'r') as c:
	config = yaml.load(c.read())
	cf = AttrDict(config)

	# Ensure that mandatory values have been provided. Raise exception/print message and stop if not.
	try:
		#config['source']['leagues'] and config['source']['API_key'] in config
		cf.source.leagues and cf.source.API_key in cf
			
	except:
		print "Add data to config.yaml file and come back!"
		sys.exit(0)
		
# Config data overrides defaults
with open('yamls.txt', 'w') as y:
	if cmp(default, config) == -1:
		y.writelines(str(config))

with open('yamls.txt', 'r') as y:
	yam = AttrDict(yaml.load(y.read()))

	# API key should be provided as custom request header
	# Download entry-point data from source. Respect API key from config
	try:
		req = requests.get(yam.source.base_url, headers={'X-Auth-Token': yam.source.API_key, 'X-Response-Control': 'minified'})
		req.status_code == requests.codes.ok
	except  ConnectionError:
		print 'A Connection error occurred.'
	except  HTTPError:
		print 'An HTTP error occurred.'

	# Build dependecies for further downloads

	# Store all obtained data locally in plain files
	with open('soccerseasons.txt', 'w') as s:
		s.writelines(req.text)

	

