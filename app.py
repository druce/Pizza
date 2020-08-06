from pizza import *
from flask import Response
from flask_jsonpify import jsonpify
from flask_cors import CORS, cross_origin

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
    ltype = 'establishment'
    rankby = 'distance'

    # gmaps_df = gmaps_get_df(location, keyword)
    # yelp_df = yelp_get_df(location, keyword)
    # foursquare_df = foursquare_get_df(location, keyword)
    # dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
    # dedupe_df = dedupe(dedupe_list)
    # dedupe_df.to_pickle("results.pkl")

    # for debug, don't use API calls
    dedupe_df = pd.read_pickle("results.pkl")
    return Response(dedupe_df.to_json(orient="records"), mimetype='application/json')


@app.route("/query")
def query():

    args = request.args
    if args:
        location = args['location']
        keyword = args['keyword']
        ltype = args['ltype']
        rankby = args['rankby']

        # gmaps_df = gmaps_get_df(location, keyword)
        # yelp_df = yelp_get_df(location, keyword)
        # foursquare_df = foursquare_get_df(location, keyword)
        # dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
        # dedupe_df = dedupe(dedupe_list)
        # dedupe_df.to_pickle("results.pkl")

        # for debug, don't use API calls
        dedupe_df = pd.read_pickle("results.pkl")
        df_list = dedupe_df.values.tolist()
        JSONP_data = jsonpify(df_list)
        return Response(JSONP_data, mimetype='application/json')
    else:
        return "No query string received", 200

app.run(threaded=True, host=HOST, port=PORT)
