# run pizza.ipynb in a flask server
# http://localhost:8501/query?location=40.6875627,-74.0035107&keyword=coffee&ltype=establishment&rankby=distance

import time
import requests, json 

import flask
from flask import request, jsonify

import gmaps
with open('apikey.txt') as f:
    api_key = f.readline().strip()
    f.close
gmaps.configure(api_key=api_key)

#######################################################

MIN_USER_RATINGS = 10
MIN_RATING = 4
URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

#######################################################

def get_gmaps_results(api_key, location, **kwargs):

    request_url = URL + '?key=' + api_key
    request_url += '&location=' + location
    for name, val in kwargs.items():
        request_url += '&' + name + '=' + val
    r = requests.get(request_url)
    j = r.json()
    return j

def get_next_page(api_key, next_page_token):
    r = requests.get(URL + '?pagetoken=' + next_page_token +
                        '&key=' + api_key)
    for i in range(10):
        j = r.json()
        if not j['results']: # wait for next page to be available
            time.sleep(5)
            continue
        else:
            return j

def process_results(results):
    global ratings, addresses
    for i, res in enumerate(results): 
        if res['user_ratings_total'] < MIN_USER_RATINGS:
            continue
        if res['rating'] < MIN_RATING:
            continue
        addresses[res['name']] = res['vicinity']
        ratings[res['name']] = res['rating']
        print(res['name'], res['rating'])
    return i+1

def runquery(api_key, location, **kwargs):
    j = get_gmaps_results(api_key, location, **kwargs)
    results = j['results']
    totalresults = 0
    
    totalresults += process_results(results)
    
    while 'next_page_token' in j:
        next_page_token = j['next_page_token']
        time.sleep(5)
        j = get_next_page(api_key, next_page_token)
        results = j['results'] 
        totalresults += process_results(results)
        
    return totalresults
#######################################################

ratings = {}
addresses = {}

# home
# location = '40.6875627,-74.0035107'
# grand army plaza
# location = '40.671872,-73.972544'
# union st and 4th ave
# location ='40.677485,-73.983310'
# bay ridge
# location = "40.624468,-74.0487134"

#rankby='prominence'
# rankby='distance'
# keyword='coffee'
# ltype='establishment'
# radius='3000'

# use either rankby or radius
#https://developers.google.com/places/web-service/supported_types

PORT=8501
HOST='0.0.0.0'

print("starting web server on port %d" % PORT)
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return jsonify(jarray)

@app.route("/query")
def query():
    args = request.args
    if args:
        location = args['location']
        keyword = args['keyword']
        ltype = args['ltype']
        rankby = args['rankby']
        
        runquery(api_key, location, keyword=keyword, ltype=ltype, rankby=rankby)

        ### sorted array
        jarray = []
        for name, rating in reversed(sorted(ratings.items(), key=lambda item: item[1])):
            #print (rating, name, addresses[name])
            jarray.append([name, addresses[name], rating])

        return(jsonify(jarray))

    else:
        return "No query string received", 200

app.run(host=HOST, port=PORT)
