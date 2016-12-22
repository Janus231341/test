#!/usr/bin/env python

from urllib.request import urlopen
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	print(json.dumps(req, indent=4))

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def makeWebhookResult(req):
	#getting the action from AI.API
	if req.get("result").get("action") != "shipping.cost":
		return {}
	result = req.get("result")
	parameters = result.get("parameters")
	zone = parameters.get("shipping-zone")

	transportapi = '5e8409e5f9cd8ef287468355ffd25096'
	appid = 'd50cb982'
	url = ('http://transportapi.com/v3/uk/places.json?query=euston&type=train_station&app_id='+appid+'&app_key='+transportapi)

	html = urlopen(url).read().decode('utf8')
	obj = json.loads(html)
	test = (obj['member'][0])
	cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

	speech = "The cost of shipping to " + zone + " is " + str(test[zone]) + " euros."

	print("Response:")
	print(speech)


	#returning result back to AI.API in required format
	return {
		"speech": speech,
		"displayText": speech,
		#"data": {},
		# "contextOut": [],
		"source": "apiai-onlinestore-shipping"
	}


if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print "Starting app on port %d" % port

	app.run(debug=True, port=port, host='0.0.0.0')
