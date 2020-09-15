import time
# import traceback
# import pdb
from itertools import product
from multiprocessing import Pool

import numpy as np
import pandas as pd
import pandas_dedupe

from geopy.distance import distance

from sklearn.preprocessing import StandardScaler

import requests

import gmaps
from yelpapi import YelpAPI
from foursquare import Foursquare, FoursquareException

with open('secrets/apikey.txt') as f:
    api_key = f.readline().strip()
    f.close
gmaps.configure(api_key=api_key)

# https://github.com/gfairchild/yelpapi
with open('secrets/yelpkey.txt') as f:
    yelp_key = f.readline().strip()
    f.close
yelp_api = YelpAPI(yelp_key)

with open('secrets/foursquare_id.txt') as f:
    foursquare_id = f.readline().strip()
    f.close
with open('secrets/foursquare_secret.txt') as f:
    foursquare_secret = f.readline().strip()
    f.close

#######################################################

MIN_USER_RATINGS = 20
MIN_RATING = 0
NRESULTS = 50
RADIUS = 1000

#######################################################

GMAPS_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
rankby = 'distance'
ltype = 'establishment'

#######################################################


def gmaps_get_first_page(api_key, location, **kwargs):
    """get first page of results from gmaps using api_key, location, kwargs for search spec"""
    # use either rankby or radius kwarg
    request_url = GMAPS_URL + '?key=' + api_key
    request_url += '&location=' + location
    for name, val in kwargs.items():
        request_url += '&' + name + '=' + str(val)
    r = requests.get(request_url)
    j = r.json()
    return j


def gmaps_get_next_page(api_key, next_page_token):
    """get next search engine results page page using search token, waiting until available"""
    r = requests.get(GMAPS_URL + '?pagetoken=' + next_page_token + '&key=' + api_key)
    for i in range(10):
        j = r.json()
        if not j['results']:  # wait for next page to be available
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


def gmaps_get_df(location_coords, keyword):

    # use either rankby or radius
    location_str = "%.7f,%.7f" % location_coords
    gmaps_df = gmaps_get_all_df(api_key, location_str, keyword=keyword, ltype=ltype, radius=RADIUS)
    if gmaps_df.empty:
        return None
    else:
        # gmaps_get_df(api_key, location, keyword=keyword, ltype=ltype, radius=RADIUS)
        gmaps_df = gmaps_df.loc[(gmaps_df['user_ratings_total'] >= MIN_USER_RATINGS) &
                                (gmaps_df['rating'] >= MIN_RATING)] \
                           .sort_values(['rating', 'user_ratings_total'], ascending=False) \
                           .reset_index(drop=True)
        gmaps_df = gmaps_df[['name', 'vicinity', 'rating', 'user_ratings_total',
                             'geometry.location.lat', 'geometry.location.lng']]
        gmaps_df.columns = ['name', 'address', 'rating', 'nratings', 'lat', 'lng']
        # drop trailing ", Brooklyn"
        gmaps_df['address'] = gmaps_df['address'] \
            .apply(lambda address: " ".join(address.split(',')[:-1]))
        gmaps_df['distance'] = gmaps_df \
            .apply(lambda row: distance((row['lat'], row['lng']), location_coords).km,
                   axis=1)
        gmaps_df['category'] = keyword
        
        return gmaps_df


def yelp_get_df(location_coords, keyword):
    lat, lng = location_coords
    response = yelp_api.search_query(categories=keyword, latitude=lat, longitude=lng,
                                     radius=RADIUS, sort_by=rankby, limit=NRESULTS)

    yelp_df = pd.json_normalize(response['businesses'])
    if not yelp_df.empty:
        yelp_df = yelp_df.loc[(yelp_df['review_count'] >= MIN_USER_RATINGS) & (yelp_df['rating'] >= MIN_RATING)] \
                         .sort_values(['rating', 'review_count'], ascending=False) \
                         .reset_index(drop=True)
        display_columns = ['name', 'location.address1', 'rating', 'review_count',
                           'coordinates.latitude', 'coordinates.longitude', 'url']
        yelp_df = yelp_df[display_columns]
        yelp_df.columns = ['name', 'address', 'rating', 'nratings', 'lat', 'lng', 'url']
        yelp_df['distance'] = yelp_df.apply(lambda row: distance((row['lat'], row['lng']), location_coords).km,
                                            axis=1)
        yelp_df['category'] = keyword
        if yelp_df.empty:
            return None
        else:
            return yelp_df

    else:
        return None


def foursquare_get_df(location_coords, keyword):
    location_str = "%.7f,%.7f" % location_coords
    client = Foursquare(client_id=foursquare_id,
                        client_secret=foursquare_secret,
                        redirect_uri='http://streeteye.com/')
    response = client.venues.search(params={'query': keyword, 'll': "%s" % location_str,
                                            'radius': RADIUS, 'limit': NRESULTS})

    foursquare_array = []

    for i, venue in pd.json_normalize(response['venues']).iterrows():
        venue_id = venue['id']
        # query detailed venue info from foursquare
        venue_name = venue['name']
        venue_address = venue['location.address']
        # sometimes no URL
        try:
            venue_url = venue['delivery.url']
        except:
            venue_url = ''

        venue_lat = venue['location.lat']
        venue_lng = venue['location.lng']
        # default these to -1
        venue_rating = -1
        venue_nratings = -1
        try:
            # get rating, nratings with another API call for venue details
            venue_details = client.venues(venue_id)['venue']
            venue_rating = venue_details['rating']
            venue_nratings = venue_details['ratingSignals']
        except FoursquareException as e:
            print("Foursquare exception", type(e), str(e))
        except Exception as e:
            continue
            # sometimes no rating ... probably not popular enough
            # print(type(e), str(e))
            # print(traceback.format_exc())
            # print("No rating for %s" % venue_name)

        foursquare_array.append([venue_name, venue_address, venue_rating, venue_nratings,
                                 venue_lat, venue_lng, venue_url])

    foursquare_df = pd.DataFrame(foursquare_array)

    if len(foursquare_df) and len(foursquare_df.columns):
        foursquare_df.columns = ['name', 'address', 'rating', 'nratings', 'lat', 'lng', 'url']
        foursquare_df = foursquare_df.loc[(foursquare_df['nratings'] >= MIN_USER_RATINGS) &
                                          (foursquare_df['rating'] >= MIN_RATING)] \
                                     .sort_values(['rating', 'nratings'], ascending=False) \
                                     .reset_index(drop=True)

        foursquare_df['distance'] = foursquare_df.apply(lambda row: distance((row['lat'],
                                                                              row['lng']),
                                                                             location_coords).km,
                                                        axis=1)
        foursquare_df['category'] = keyword
        if foursquare_df.empty:
            return None
        else:
            return foursquare_df
    else:
        return None


def generic_get_df(service, location_coords, keyword):
    """Query specified service for location and keyword, return dataframe"""

    if service == "gmaps":
        retdf = gmaps_get_df(location_coords, keyword)
    elif service == "yelp":
        retdf = yelp_get_df(location_coords, keyword)
    elif service == "foursquare":
        retdf = foursquare_get_df(location_coords, keyword)

    return retdf


def all_get_df(location_coords, keyword):
    """Query all services for location and keyword, return list of dataframes"""

    services = ['gmaps', 'yelp', 'foursquare']
    args = list(product(services, [location_coords], [keyword]))
    with Pool() as pool:
        df_list = pool.starmap(generic_get_df, args)
    df_list = [df for df in df_list if df is not None]
    return df_list


def dedupe(dedupe_list, location_coords):
    for i, source_df in enumerate(dedupe_list):
        source_df['source'] = i
    venues_df = pd.concat(dedupe_list).reset_index()
    venues_df['latlong'] = venues_df[['lat', 'lng']].apply(tuple, axis=1)
    venues_df['shortname'] = venues_df['name'].apply(lambda n: n[:25])

    # dedupe and assign cluster id
    venues_df2 = pandas_dedupe.dedupe_dataframe(venues_df, ['category', 'shortname', 'address', ('latlong', 'LatLong')])
    venues_df['cluster'] = venues_df2['cluster id']
    venues_df = venues_df.sort_values(['cluster', 'source'])[['cluster', 'name', 'address', 'rating', 'nratings',
                                                              'lat', 'lng', 'distance', 'source']]

    # group by clusters, uniquify name
    cluster_df = venues_df.groupby('cluster')[['name', 'address', 'lat', 'lng', 'distance', 'source']] \
                          .first() \
                          .reset_index()

    # merge ratings by source
    merge_df = cluster_df \
        .merge(venues_df.loc[venues_df['source'] == '0'][['cluster', 'rating', 'nratings']],
               on='cluster', how='outer') \
        .rename(columns={'rating': 'gmaps_rating', 'nratings': 'gmaps_nratings'})
    merge_df['gmaps_rating_std'] = StandardScaler().fit_transform(merge_df[['gmaps_rating']])

    merge_df = merge_df \
        .merge(venues_df.loc[venues_df['source'] == '1'][['cluster', 'rating', 'nratings']],
               on='cluster', how='outer') \
        .rename(columns={'rating': 'yelp_rating', 'nratings': 'yelp_nratings'})
    merge_df['yelp_rating_std'] = StandardScaler().fit_transform(merge_df[['yelp_rating']])

    merge_df = merge_df \
        .merge(venues_df.loc[venues_df['source'] == '2'][['cluster', 'rating', 'nratings']],
               on='cluster', how='outer') \
        .rename(columns={'rating': 'foursquare_rating', 'nratings': 'foursquare_nratings'})
    merge_df['foursquare_rating_std'] = StandardScaler().fit_transform(merge_df[['foursquare_rating']])

    merge_df['distance'] = merge_df.apply(lambda row: distance((row['lat'], row['lng']), location_coords).km,
                                          axis=1)

    # bayes score
    rating_cols = ['gmaps_rating_std', 'yelp_rating_std', 'foursquare_rating_std']
    merge_df['nratings'] = merge_df[rating_cols].count(axis=1)
    nratings_mean = np.mean(merge_df['nratings'])
    rating_avg = np.nanmean(merge_df[rating_cols])
    merge_df['w'] = merge_df['nratings']/(merge_df['nratings'] + nratings_mean)
    merge_df['R'] = np.mean(merge_df[rating_cols], axis=1)
    merge_df['bayes_score'] = merge_df['w'] * merge_df['R'] + (1 - merge_df['w']) * rating_avg
    merge_df = merge_df.sort_values('bayes_score', ascending=False)
    merge_df[['name', 'address', 'gmaps_rating', 'yelp_rating', 'foursquare_rating', 'nratings', 'bayes_score']]
    return merge_df


def df_to_table(df):

    # markers = [(row.lat, row.lng) for row in df.itertuples()]
    # marker_hover = ["%s: %s (%s)" % (row.name, row.rating, row.nratings) for row in df.itertuples()]

    retstr = "<html><head><title>Pizza Pizza Pizza</title></head><body><table>"
    retstr += "<tr><td>Rating</td><td>Reviews</td><td>Name</td><td>Address</td></tr>"
    row_template = "<tr><td>{rating}</td><td>{nratings}</td><td>{name}</td><td>{address}</td></tr>"
    retstr += "\n".join([row_template.format(**row) for i, row in df.iterrows()])

    retstr += "</table></body></html>"
    return retstr
