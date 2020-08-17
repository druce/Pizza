from pizza import *
from flask import Response
from flask_jsonpify import jsonpify, jsonify
from flask_cors import CORS, cross_origin

# run concept of pizza.ipynb using a flask server
# http://localhost:8501/query?location=brooklynheights&keyword=coffee

# center the table, center the form widgets
# start with empty table
# clear the table when dropdown changes
# append the table header on first search
# resize overlay when body resizes

# show the map

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

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    location = '40.6915812,-73.9954095'
    keyword = 'pizza'

    # gmaps_df = gmaps_get_df(location, keyword)
    # yelp_df = yelp_get_df(location, keyword)
    # foursquare_df = foursquare_get_df(location, keyword)
    # dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
    # dedupe_df = dedupe(dedupe_list)
    # dedupe_df.to_pickle("results.pkl")

    # for demo, don't use API calls
    dedupe_df = pd.read_pickle("pizza_brooklynheights.pkl")
    tablecols = ['name', 'address', 'distance', 'gmaps_rating', 'yelp_rating', 'foursquare_rating']
    tmpdf = dedupe_df.sort_values('bayes_score', ascending=False).reset_index(drop=True)[tablecols]
    tmpdf['rank'] = tmpdf.index + 1
    tmpdf['distance'] = tmpdf['distance'].apply(lambda d: "%1.1f km" % (float(d)))
    tmpdf['address'] = tmpdf['address'].apply(lambda a: a[:25])
    tmpdf['name'] = tmpdf['name'].apply(lambda a: a[:25])
    tmpdf = tmpdf[['rank'] + tablecols]
    tmpdf.columns=['Rank', 'Name', 'Address', 'Distance', 'Google Maps', 'Yelp', 'Foursquare']
    retval = tmpdf.to_json(orient="records")
    return Response(retval, mimetype='application/json')


@app.route("/query")
def query():
    # http://localhost:8501
    args = request.args
    if args:
        location = args['location']
        keyword = args['keyword']

        # gmaps_df = gmaps_get_df(location, keyword)
        # yelp_df = yelp_get_df(location, keyword)
        # foursquare_df = foursquare_get_df(location, keyword)
        # dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
        # dedupe_df = dedupe(dedupe_list)
        # dedupe_df.to_pickle("results.pkl")

        # for demo, don't use API calls
        picklefile = "%s_%s.pkl" % (keyword, location)
        dedupe_df = pd.read_pickle(picklefile)
        tablecols = ['name', 'address', 'distance', 'gmaps_rating', 'yelp_rating', 'foursquare_rating']
        tmpdf = dedupe_df.sort_values('bayes_score', ascending=False).reset_index(drop=True)[tablecols]
        tmpdf['rank'] = tmpdf.index + 1
        tmpdf['distance'] = tmpdf['distance'].apply(lambda d: "%1.1f km" % (float(d)))
        tmpdf['address'] = tmpdf['address'].apply(lambda a: a[:25])
        tmpdf['name'] = tmpdf['name'].apply(lambda a: a[:25])
        tmpdf = tmpdf[['rank'] + tablecols]
        tmpdf.columns=['Rank', 'Name', 'Address', 'Distance', 'Google Maps', 'Yelp', 'Foursquare']
        retval = tmpdf.to_json(orient="records")
        return Response(retval, mimetype='application/json')
        
        dedupe_df = pd.read_pickle("pizza_brooklynheights.pkl")
        df_list = dedupe_df.values.tolist()
        return Response(jsonify(df_list), mimetype='application/json')
    else:
        return "No query string received", 200

app.run(threaded=True, host=HOST, port=PORT)
