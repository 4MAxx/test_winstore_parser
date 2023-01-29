import requests

URL = 'https://apps.microsoft.com/store/api/Products/GetFilteredProducts/'
HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
number_of_items = 20
PARAMS = {'hl': 'ru - ru',
          'gl': 'US',
          'NoItems': number_of_items,
          'Category': 'Business'
          }
PARAMS_FOR_DETAILS = {'hl': 'ru - ru',
                      'gl': 'US'
                      }


if __name__ == "__main__":
    products = requests.get(URL, headers=HEADERS, params=PARAMS)
    products.raise_for_status()
    productsList = products.json()['productsList']
    apps_data = []
    for prod in productsList:
        prod_properties = {'categories': prod['categories'],
                           'productId': prod['productId'],
                           'publisherName': prod['publisherName'],
                           'title': prod['title']
                           }
        URL_FOR_DETAILS = f'https://apps.microsoft.com/store/api/ProductsDetails/GetProductDetailsById/{prod_properties["productId"]}'
        details = requests.get(URL_FOR_DETAILS, headers=HEADERS, params=PARAMS_FOR_DETAILS)
        details.raise_for_status()
        app_details = details.json()
        prod_properties['releaseDateUtc'] = app_details['releaseDateUtc']
        prod_properties['supportUris'] = [x['uri'] for x in app_details['supportUris']]
        apps_data.append(prod_properties)

    for i in apps_data:
        print(i)