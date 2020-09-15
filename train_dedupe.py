from itertools import product
import pandas as pd
import pandas_dedupe

tempdf = None
for k, l, j in product(['pizza', 'coffee', 'icecream'], 
                    ['midtown','downtown','uppereastside','upperwestside','brooklynheights','grandarmyplaza','bayridge','williamsburg',],
                    ['gmaps', 'yelp', 'foursquare']):
    filename = "cache/%s_%s_%s.pkl" % (j, k, l)
    try:
        if tempdf is None:
            tempdf = pd.read_pickle(filename)
            tempdf['category'] = k
            print(filename)
        else:
            newdf = pd.read_pickle(filename)            
            newdf['category'] = k
            tempdf = pd.concat([tempdf, newdf])
            print(filename)
    except:
        print("missing ", filename)

tempdf['latlong'] = tempdf[['lat','lng']].apply(tuple, axis=1)
tempdf['shortname'] = tempdf['name'].apply(lambda n: n[:25])

tempdf.to_csv('train_df.csv', index=False)

        
