#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    #JSON file from the AI
    req = request.get_json(silent=True, force=True)
    print("Getting the file")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "transport.test":
        return{}
    result = req.get("result")
    parameters = result.get("parameters")
    location = parameters.get("location")

    transportapi = '5e8409e5f9cd8ef287468355ffd25096'
    appid = 'd50cb982'
    baseURL = "http://transportapi.com/v3/uk/places.json?query=" + location + "&type=train_station&app_id=" + appid + '&app_key='+transportapi
    print(baseURL)
    html = urlopen(baseURL).read().decode('utf8')
    obj = json.loads(html)

    speech = "There is a station at longitude " + obj['member'][0]['logitude'] + "and latitude " + obj['member'][0]['latitude']

    print(speech)
    return {
        "speech": speech
        "displayText": speech
        "source": "apiai-onlinestore-shipping"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
