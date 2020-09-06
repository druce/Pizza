from pizza import all_get_df, dedupe
from flask import Flask, request, Response
# from flask_jsonpify import jsonpify, jsonify
from flask_cors import CORS, cross_origin

import pandas as pd

latlong_enabled = True
cachedir = 'cache/'
# run pizza.ipynb using a flask server
# http://localhost:8181/query?location=brooklynheights&keyword=coffee

# TODO:
# install all requirements via npm - retry build step
# npm script to make dist
# maybe train dedupe with the keyword. currently train all together but we never dedupe a frame w/both coffee+pizza

#######################################################
# home
# location = '40.6915812,-73.9954095'
# grand army plaza
# location = '40.671872,-73.972544'
# union st and 4th ave
# location ='40.677485,-73.983310'
# bay ridge
# location = "40.624468,-74.0487134"

# rankby='prominence'
# rankby='distance'
# keyword='coffee'
# ltype='establishment'
# radius='3000'

# use either rankby or radius
# https://developers.google.com/places/web-service/supported_types

PORT = 8181
HOST = '0.0.0.0'

print("starting web server on port %d" % PORT)

app = Flask(__name__)
app.config["DEBUG"] = True

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    # location = '40.6915812,-73.9954095'
    # keyword = 'pizza'

    # gmaps_df = gmaps_get_df(location, keyword)
    # yelp_df = yelp_get_df(location, keyword)
    # foursquare_df = foursquare_get_df(location, keyword)
    # dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
    # dedupe_df = dedupe(dedupe_list)
    # dedupe_df.to_pickle("results.pkl")

    # for demo, don't use API calls
    dedupe_df = pd.read_pickle("cache/pizza_brooklynheights.pkl")
    tablecols = ['name', 'address', 'distance', 'gmaps_rating', 'yelp_rating', 'foursquare_rating', 'lat', 'lng']
    tmpdf = dedupe_df.sort_values('bayes_score', ascending=False).reset_index(drop=True)[tablecols]
    tmpdf['rank'] = tmpdf.index + 1
    tmpdf['distance'] = tmpdf['distance'].apply(lambda d: "%1.1f km" % (float(d)))
    tmpdf['address'] = tmpdf['address'].apply(lambda a: a[:25])
    tmpdf['name'] = tmpdf['name'].apply(lambda a: a[:25])
    tmpdf = tmpdf[['rank'] + tablecols]
    tmpdf.columns = ['Rank', 'Name', 'Address', 'Distance', 'Google Maps', 'Yelp', 'Foursquare', 'Lat', 'Lng']
    retval = tmpdf.to_json(orient="records")
    return Response(retval, mimetype='application/json')


@app.route("/query")
def query():
    # http://localhost:8501
    args = request.args
    if args:
        location = args['location'] if 'location' in request.args else None
        keyword = args['keyword'] if 'keyword' in request.args else None
        lat = args['lat'] if 'lat' in request.args else None
        lng = args['lng'] if 'lng' in request.args else None

        # for demo, don't use API calls, use canned data
        if location and keyword:
            picklefile = "%s%s_%s.pkl" % (cachedir, keyword, location)
            dedupe_df = pd.read_pickle(picklefile)
            tablecols = ['name', 'address', 'distance', 'gmaps_rating', 'gmaps_nratings',
                         'yelp_rating', 'yelp_nratings', 'foursquare_rating', 'foursquare_nratings',
                         'lat', 'lng']
            tmpdf = dedupe_df.sort_values(
                'bayes_score', ascending=False).reset_index(drop=True)[tablecols]
            tmpdf['rank'] = tmpdf.index + 1
            tmpdf['distance'] = tmpdf['distance'].apply(
                lambda d: "%1.1f km" % (float(d)))
            tmpdf['address'] = tmpdf['address'].apply(lambda a: a[:25])
            tmpdf['name'] = tmpdf['name'].apply(lambda a: a[:25])
            tmpdf = tmpdf[['rank'] + tablecols]
            tmpdf.columns = ['Rank', 'Name', 'Address', 'Distance',
                             'Google Maps', 'Gratings', 'Yelp', 'Yratings', 'Foursquare', 'Fratings',
                             'Lat', 'Lng']
            retval = tmpdf.to_json(orient="records")
            return Response(retval, mimetype='application/json')
        # if lat and lng provided and enabled, search online using service APIs
        elif latlong_enabled and lat and lng:
            location_coords = (float(lat), float(lng))
            df_list = all_get_df(location_coords, keyword)
            dedupe_df = dedupe(df_list, location_coords)
            tablecols = ['name', 'address', 'distance', 'gmaps_rating', 'gmaps_nratings',
                         'yelp_rating', 'yelp_nratings', 'foursquare_rating', 'foursquare_nratings',
                         'lat', 'lng']
            tmpdf = dedupe_df.sort_values(
                'bayes_score', ascending=False).reset_index(drop=True)[tablecols]
            tmpdf['rank'] = tmpdf.index + 1
            tmpdf['distance'] = tmpdf['distance'].apply(
                lambda d: "%1.1f km" % (float(d)))
            tmpdf['address'] = tmpdf['address'].apply(lambda a: a[:25])
            tmpdf['name'] = tmpdf['name'].apply(lambda a: a[:25])
            tmpdf = tmpdf[['rank'] + tablecols]
            tmpdf.columns = ['Rank', 'Name', 'Address', 'Distance',
                             'Google Maps', 'Gratings', 'Yelp', 'Yratings', 'Foursquare', 'Fratings',
                             'Lat', 'Lng']
            retval = tmpdf.to_json(orient="records")
            return Response(retval, mimetype='application/json')
        else:
            return "Invalid query string received", 200
    else:
        return "No query string received", 200


app.run(threaded=True, host=HOST, port=PORT)
