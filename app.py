from pizza import *

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

@app.route('/', methods=['GET'])
def home():
    location = '40.6915812,-73.9954095'
    keyword = 'pizza'
    ltype = 'establishment'
    rankby = 'distance'

    gmaps_df = gmaps_get_df(location, keyword)
    yelp_df = yelp_get_df(location, keyword)
    foursquare_df = foursquare_get_df(location, keyword)
    dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
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
        dedupe_list = list(filter(lambda df: df is not None, [gmaps_df, yelp_df, foursquare_df]))
        print(len(gmaps_df), len(yelp_df), len(foursquare_df))
        print("Deduping %d dataframes" % (len(list(dedupe_list))))
        return dedupe(dedupe_list).to_json()
    else:
        return "No query string received", 200

app.run(threaded=True, host=HOST, port=PORT)
