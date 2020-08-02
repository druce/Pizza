# run pizza.ipynb in a flask server
# http://localhost:8501/query?location=40.6875627,-74.0035107&keyword=coffee&ltype=establishment&rankby=distance

# show form
# show querying status / progress bar
# show map
# html getting the json
# sortable table
# dropdown coffee / pizza
# dropdown locations
# swap background image https://www.papajohns.com/free-pizza/img/hero-free-pizza.jpg
# https://wallpaperaccess.com/black-coffee
# make it work on colab

import time
from pprint import pprint
from ipywidgets import widgets, interact
import pdb

import numpy as np
import pandas as pd
import pandas_dedupe

from sklearn.preprocessing import StandardScaler

import requests, json 

from flask import Flask, request

import gmaps
with open('apikeys/apikey.txt') as f:
    api_key = f.readline().strip()
    f.close
gmaps.configure(api_key=api_key)

# https://github.com/gfairchild/yelpapi
from yelpapi import YelpAPI
with open('apikeys/yelpkey.txt') as f:
    yelp_key = f.readline().strip()
    f.close
yelp_api = YelpAPI(yelp_key)

import foursquare
with open('apikeys/foursquare_id.txt') as f:
    foursquare_id = f.readline().strip()
    f.close
with open('apikeys/foursquare_secret.txt') as f:
    foursquare_secret = f.readline().strip()
    f.close

import folium


#######################################################

MIN_USER_RATINGS = 40
MIN_RATING = 3
NRESULTS = 50
RADIUS = 3000

#######################################################

GMAPS_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
rankby='distance'
ltype='establishment'

#######################################################

def gmaps_get_first_page(api_key, location, **kwargs):
    """get first page of results from gmaps using api_key, location, kwargs for search spec"""
    request_url = GMAPS_URL + '?key=' + api_key
    request_url += '&location=' + location
    for name, val in kwargs.items():
        request_url += '&' + name + '=' + val
    r = requests.get(request_url)
    j = r.json()
    return j


def gmaps_get_next_page(api_key, next_page_token):
    """get next search engine results page page using search token, waiting until available"""
    r = requests.get(GMAPS_URL + '?pagetoken=' + next_page_token +
                        '&key=' + api_key)
    for i in range(10):
        j = r.json()
        if not j['results']: # wait for next page to be available
            time.sleep(5)
            continue
        else:
            return j


def gmaps_get_all_df(api_key, location, **kwargs):
    """return dataframe of all results using api_key, location, search kwargs"""
    # get first page
    j = gmaps_get_first_page(api_key, location, **kwargs)
    venues_df = pd.json_normalize(j['results'])

    # get pages while additional pages available
    while 'next_page_token' in j:
        next_page_token = j['next_page_token']
        time.sleep(5)
        j = gmaps_get_next_page(api_key, next_page_token)
        venues_df = venues_df.append(pd.json_normalize(j['results']))
        
    return venues_df


def gmaps_get_df(location, keyword):

    # use either rankby or radius
    gmaps_df = gmaps_get_all_df(api_key, location, keyword=keyword, ltype=ltype, rankby=rankby)
    if len(gmaps_df) and len(gmaps_df.columns):
        # gmaps_get_df(api_key, location, keyword=keyword, ltype=ltype, radius=RADIUS)
        gmaps_df = gmaps_df.loc[(gmaps_df['user_ratings_total'] >= MIN_USER_RATINGS) & (gmaps_df['rating'] >= MIN_RATING)] \
                           .sort_values(['rating', 'user_ratings_total'], ascending=False) \
                           .reset_index(drop=True)
        gmaps_df = gmaps_df[['name', 'vicinity', 'rating', 'user_ratings_total', 'geometry.location.lat', 'geometry.location.lng']]
        gmaps_df.columns = ['name', 'address', 'rating', 'nratings', 'lat', 'lng']
        # drop trailing ", Brooklyn"
        gmaps_df['address'] = gmaps_df['address'].apply(lambda address: " ".join(address.split(',')[:-1]))
        return gmaps_df
    else:
        return None


def yelp_get_df(location, keyword):
    lat, lng = eval(location)
    response = yelp_api.search_query(categories=keyword, latitude=lat, longitude=lng, 
                                     radius=RADIUS, sort_by=rankby, limit=NRESULTS)

    yelp_df = pd.json_normalize(response['businesses'])
    if len(yelp_df) and len(yelp_df.columns):    
        yelp_df = yelp_df.loc[(yelp_df['review_count'] >= MIN_USER_RATINGS) & (yelp_df['rating'] >= MIN_RATING)] \
                         .sort_values(['rating', 'review_count'], ascending=False) \
                         .reset_index(drop=True)
        display_columns = ['name', 'location.address1', 'rating', 'review_count', 'coordinates.latitude', 'coordinates.longitude', 'url']
        yelp_df = yelp_df[display_columns]
        yelp_df.columns = ['name', 'address', 'rating', 'nratings', 'lat', 'lng', 'url']
        return yelp_df
    else:
        return None


def foursquare_get_df(location, keyword):

    client = foursquare.Foursquare(client_id=foursquare_id, 
                                   client_secret=foursquare_secret, 
                                   redirect_uri='http://streeteye.com/')
    response = client.venues.search(params={'query': keyword, 'll': "%s" % location, 
                                            'radius': RADIUS, 'limit': NRESULTS})

    foursquare_array = []

    for i, venue in pd.json_normalize(response['venues']).iterrows():
        venue_id = venue['id']
        # query detailed venue info from foursquare
        venue_details = client.venues(venue_id)['venue']
        try:
            venue_name = venue['name']
            venue_address = venue['location.address']
            venue_rating = venue_details['rating']
            venue_nratings = venue_details['ratingSignals']
            venue_url = venue['delivery.url']
            venue_lat = venue['location.lat']
            venue_lng = venue['location.lng']
            foursquare_array.append([venue_name, venue_address, venue_rating, venue_nratings, venue_lat, venue_lng, venue_url])
            
        except Exception as e:
            # sometimes no rating ... probably not popular enough
            # print(type(e), str(e))
            # print(traceback.format_exc())
            # print("No rating for %s" % venue_name)
            continue

    foursquare_df = pd.DataFrame(foursquare_array)
    if len(foursquare_df) and len(foursquare_df.columns):
        foursquare_df.columns = ['name', 'address', 'rating', 'nratings', 'lat', 'lng', 'url']
        return foursquare_df
    else:
        return None


def dedupe(dedupe_list):

    for i, source_df in enumerate(dedupe_list):
        source_df['source'] = i

    venues_df = pd.concat(dedupe_list).reset_index()
    venues_df['latlong'] = venues_df[['lat','lng']].apply(tuple, axis=1)
    venues_df['shortname'] = venues_df['name'].apply(lambda n: n[:25])
    venues_df2 = pandas_dedupe.dedupe_dataframe(venues_df, ['shortname', 'address', ('latlong', 'LatLong')])
    venues_df['cluster'] = venues_df2['cluster id']
    venues_df = venues_df.sort_values(['cluster', 'source'])[['cluster', 'name', 'address', 'rating', 'nratings', 'lat', 'lng', 'source']]

    # group by clusters, uniquify name
    cluster_df = venues_df.groupby('cluster')[['name', 'address', 'lat', 'lng', 'source']] \
                          .first() \
                          .reset_index()

    # merge ratings by source
    merge_df = cluster_df \
        .merge(venues_df.loc[venues_df['source']==0][['cluster','rating']], on='cluster', how='outer') \
        .rename(columns={'rating': 'gmaps_rating'})
    merge_df['gmaps_rating_std'] = StandardScaler().fit_transform(merge_df[['gmaps_rating']])

    merge_df = merge_df \
        .merge(venues_df.loc[venues_df['source']==1][['cluster','rating']], on='cluster', how='outer') \
        .rename(columns={'rating': 'yelp_rating'})
    merge_df['yelp_rating_std'] = StandardScaler().fit_transform(merge_df[['yelp_rating']])

    merge_df = merge_df \
        .merge(venues_df.loc[venues_df['source']==2][['cluster','rating']], on='cluster', how='outer') \
        .rename(columns={'rating': 'foursquare_rating'})
    merge_df['foursquare_rating_std'] = StandardScaler().fit_transform(merge_df[['foursquare_rating']])

    # bayes score
    rating_cols = ['gmaps_rating_std', 'yelp_rating_std', 'foursquare_rating_std']
    merge_df['nratings'] = merge_df[rating_cols].count(axis=1)
    nratings_mean = np.mean(merge_df['nratings'])
    rating_avg = np.nanmean(merge_df[rating_cols])
    merge_df['w'] = merge_df['nratings']/(merge_df['nratings'] + nratings_mean)
    merge_df['R'] = np.mean(merge_df[rating_cols], axis=1)
    merge_df['bayes_score'] = merge_df['w'] * merge_df['R'] + (1 - merge_df['w']) * rating_avg
    merge_df = merge_df.sort_values('bayes_score', ascending=False)
    return merge_df[['name', 'address', 'gmaps_rating', 'yelp_rating', 'foursquare_rating', 'nratings', 'bayes_score']]


def df_to_table(df):
    
    # markers = [(row.lat, row.lng) for row in df.itertuples()]
    # marker_hover = ["%s: %s (%s)" % (row.name, row.rating, row.nratings) for row in df.itertuples()]
        
    retstr = "<html><head><title>Pizza Pizza Pizza</title></head><body><table>"
    retstr += "<tr><td>Rating</td><td>Reviews</td><td>Name</td><td>Address</td></tr>"
    row_template = "<tr><td>{rating}</td><td>{nratings}</td><td>{name}</td><td>{address}</td></tr>"
    retstr += "\n".join([row_template.format(**row) for i, row in df.iterrows()])
        
    retstr += "</table></body></html>"
    return retstr    

#######################################################
# home
# location = '40.6915812,-73.9954095'
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

PORT=80
HOST='0.0.0.0'

print("starting web server on port %d" % PORT)

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    location = '40.6915812,-73.9954095'
    keyword = 'pizza'
    ltype = 'establishment'
    rankby = 'distance'

    gmaps_df = gmaps_get_df(location, keyword)
    yelp_df = yelp_get_df(location, keyword)
    foursquare_df = foursquare_get_df(location, keyword)
    dedupe_list = filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df])
    print(len(gmaps_df), len(yelp_df), len(foursquare_df))
    print("Deduping %d dataframes" % (len(list(dedupe_list))))
    return dedupe(dedupe_list).to_json()


@app.route("/query")
def query():

    args = request.args
    if args:
        location = args['location']
        keyword = args['keyword']
        ltype = args['ltype']
        rankby = args['rankby']

        gmaps_df = gmaps_get_df(location, keyword)
        yelp_df = yelp_get_df(location, keyword)
        foursquare_df = foursquare_get_df(location, keyword)
        print(len(gmaps_df), len(yelp_df), len(foursquare_df))
        pdb.set_trace()
        dedupe_list = filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df])
        print("Deduping %d dataframes" % (len(list(dedupe_list))))
        return dedupe(dedupe_list).to_json()
    else:
        return "No query string received", 200

app.run(threaded=True, host=HOST, port=PORT)
