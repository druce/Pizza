Find highest rated pizza (or other query string) in Google Maps, Yelp and Foursquare by distance from a location.

Needs:

- Google API key in apikey.txt, get one from [GCP](https://console.cloud.google.com/google/maps-apis/credentials)
- Yelp key in yelpkey.txt get one from [Yelp](https://www.yelp.com/developers/documentation/v3)
- Foursquare ID and secret in foursquare_id.txt, foursquare_secret.txt, get them from [Foursquare](https://developer.foursquare.com/docs/places-api/getting-started/)

For Google maps in Jupyter add the gmaps extension:
- `conda install jupyter_contrib_nbextensions`
- `conda install -c conda-forge gmaps`
- `jupyter nbextension enable --py gmaps`

For sortable grid dataframes:
- `pip install qgrid`
- `jupyter nbextension enable --py --sys-prefix qgrid`

See `requirements.txt` for additional requirements.

Run `pizza.ipynb` in Jupyter.

Web app also available: to run locally with docker app server: `runlocal.sh`.

To deploy the web app to Amazon Container Service see [`deploy.md`](deploy.md) 

| Name	| Address | GMaps rating | Yelp rating | Foursquare rating | nratings | bayes_score |
| ----	| ------- | ------------ | ----------- | ----------------- | -------- | ----------- |
| Juliana's | 19 Old Fulton St | 4.6 | 4.5 | 8.9 | 3 | 1.025914 |
| Sottocasa | 298 Atlantic Ave | 4.6 | 4.5 |  | 2 | 0.805374 |
| L'Arte Della Pizza Brooklyn | 172 5th Ave | 4.8 |  |  | 1 | 0.796201 |
| Piz-zetta | 90 Livingston St |  | 4.5 |  | 1 | 0.633529 |
| Lucali | 575 Henry St |  | 4.5 |  | 1 | 0.633529 |
| Forcella Fried Pizza | 445 Albee Square W | 4.4 | 4.5 |  | 2 | 0.594050 |
| Dellarocco's | 214 Hicks St | 4.6 | 4.0 |  | 2 | 0.481007 |
| Pizza Secret | 72 5th Ave | 4.5 |  | 7.9 | 2 | 0.408143 |
| Brado | 155 Atlantic Ave | 4.5 | 4.0 |  | 2 | 0.375345 |
| Luzzo's | 145 Atlantic Ave | 4.5 | 4.0 |  | 2 | 0.375345 |
| Table 87 | 87 Atlantic Ave | 4.5 | 4.0 |  | 2 | 0.375345 |
| Patrizia's Pizza and Pasta | 35 Broadway |  |  | 8.2 | 1 | 0.374531 |
| Fatoosh Pitza & Grill | 330 Hicks St |  | 4.0 | 8.1 | 2 | 0.356678 |
| Union Street Pizza | 226 4th Ave | 4.5 |  |  | 1 | 0.350441 |
| Patsy’s Pizzeria | 450 Dean St | 4.5 |  |  | 1 | 0.350441 |
| La Villa Pizzeria | 261 5th Ave | 4.5 |  |  | 1 | 0.350441 |
| The House of Pizza & Calzone | 132 Union St | 4.6 | 4.0 | 7.3 | 3 | 0.329868 |
| Pizza Town | 85 5th Ave | 4.5 |  | 7.5 | 2 | 0.264953 |
| Lean Crust Pizza | 737 Fulton St | 4.4 |  |  | 1 | 0.201854 |
| Fascati Pizza | 80 Henry St |  | 4.0 | 7.6 | 2 | 0.177691 |
| Layla Jones | 214 Court St |  | 4.0 |  | 1 | 0.177388 |
| La Cigogne | 215 Union St |  | 4.0 |  | 1 | 0.177388 |
| Circa Brewing | 141 Lawrence St |  | 4.0 |  | 1 | 0.177388 |
| Enoteca on Court | 347 Court St |  | 4.0 |  | 1 | 0.177388 |
| Sam's | 238 Court St |  | 4.0 |  | 1 | 0.177388 |
| Fornino | Pier 6 Brooklyn Bridge Park |  | 4.0 |  | 1 | 0.177388 |
| Claudine's | 311 Smith St |  | 4.0 |  | 1 | 0.177388 |
| Numero 28 | 68 Bergen St | 4.3 | 4.0 |  | 2 | 0.164021 |
| Forno Rosso | 327 Gold St | 4.3 | 4.0 |  | 2 | 0.164021 |
| Front Street Pizza | 80 Front St | 4.4 | 4.0 | 7.0 | 3 | 0.082588 |
| Gino's Pizzeria | 218 Flatbush Ave | 4.3 |  |  | 1 | 0.053267 |
| Mario's Pizzeria | 224 Dekalb Ave | 4.3 |  |  | 1 | 0.053267 |
| Via Roma Pizza Bar | 445 Court St | 4.3 |  |  | 1 | 0.053267 |
| Fresh 99 cents pizza | 51 Willoughby St | 4.3 |  |  | 1 | 0.053267 |
| Not Ray's Pizza | 694 Fulton St | 4.3 |  |  | 1 | 0.053267 |
| Artichoke Basille's Pizza | 59 5th Ave | 4.3 |  |  | 1 | 0.053267 |
| Fornino At Pier 6-Open for the 2020 season! | Brooklyn Bridge Park Pier 6 Bridge Park Dr | 4.3 |  |  | 1 | 0.053267 |
| Brooklyn Pizza Market | 267 Smith St |  | 3.5 | 8.0 | 2 | -0.003486 |
| My Little Pizzeria | 114 Court St | 4.4 | 3.5 |  | 2 | -0.054684 |
| Joey Pepperoni's Pizza | 381 Broadway |  |  | 7.2 | 1 | -0.128871 |
| Brooklyn Pizza Market | 267 A Smith St | 4.1 |  |  | 1 | -0.243907 |
| Grimaldi's Pizzeria | 1 Front St | 4.2 | 3.5 |  | 2 | -0.266007 |
| Fortina - Brooklyn | 445 Albee Square W |  | 3.5 |  | 1 | -0.278753 |
| Pronto Pizza | 139 Ct St |  | 3.5 |  | 1 | -0.278753 |
| Giardini Pizza | 363 Smith St | 4.2 | 3.5 | 7.1 | 3 | -0.305260 |
| Joe’s Pizza of Park Slope | 483 5th Ave |  |  | 6.8 | 1 | -0.330232 |
| Francesco's Pizzeria & Trattoria | 529 Henry St | 4.1 | 3.5 |  | 2 | -0.371669 |
| Sal's Pizza Store | 305 Court St | 4.4 | 3.0 |  | 2 | -0.379051 |
| F&F Pizzeria | 459 Court St | 4.0 |  |  | 1 | -0.392493 |
| 99 Cents Hot Pizza | 255 Livingston St | 4.0 |  |  | 1 | -0.392493 |
| Smiling Pizza Restaurant | 323 7th Ave |  |  | 6.6 | 1 | -0.430912 |
| Norm’s | 345 Adams St | 4.0 | 3.5 |  | 2 | -0.477331 |
| Angelica | 332 Livingston St | 3.9 |  |  | 1 | -0.541080 |
| Antonio's Pizzeria | 32 Court St | 3.9 | 3.5 |  | 2 | -0.582993 |
| 2 Bros. Pizza | 395 Flatbush Ave Ext | 4.1 | 3.0 | 7.1 | 3 | -0.638903 |
| Monty Q's | 158 Montague St | 4.1 | 3.0 | 6.8 | 3 | -0.722225 |
| Papa John's Pizza | 148 Lawrence St | 3.7 |  |  | 1 | -0.838254 |
| Pronto Pizza | 139 Court St | 4.0 |  | 5.8 | 2 | -0.871913 |
| Ignazio's | 4 Water St | 4.0 | 3.0 | 6.5 | 3 | -0.887525 |
| Mario's Pizzeria | 222 Hoyt St | 3.6 |  |  | 1 | -0.986841 |
| Caruso's | 150 Smith St | 3.7 | 3.0 |  | 2 | -1.118683 |
| Papa John's Pizza | 138 4th Ave | 3.5 |  |  | 1 | -1.135428 |

