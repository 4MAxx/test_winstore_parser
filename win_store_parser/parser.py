import requests
import urllib.parse
import datetime

URL = 'https://apps.microsoft.com/store/api/Products/GetFilteredProducts/'
HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
PARAMS = {'hl': 'ru - ru',
          'gl': 'US',
          'NoItems': 24,
          'Category': 'Business'
          }
PARAMS_FOR_DETAILS = {'hl': 'ru - ru',
                      'gl': 'US'
                      }
CURSOR_STR = ['', 'bz0yMCZiPQ==', 'bz00MCZiPQ==', 'bz02MCZiPQ==', 'bz04MCZiPQ==',
              'bz0xMDAmYj0=', 'bz0xMjAmYj0=', 'bz0xNDAmYj0=', 'bz0xNjAmYj0=', 'bz0xODAmYj0=',
              'bz0yMDAmYj0=', 'bz0yMjAmYj0=', 'bz0yNDAmYj0=', 'bz0yNjAmYj0=', 'bz0yODAmYj0=',
              'bz0zMDAmYj0=', 'bz0zMjAmYj0=', 'bz0zNDAmYj0=', 'bz0zNjAmYj0=', 'bz0zODAmYj0=',
              'bz00MDAmYj0=', 'bz00MjAmYj0=', 'bz00NDAmYj0=', 'bz00NjAmYj0=', 'bz00ODAmYj0=',
              'bz01MDAmYj0=', 'bz01MjAmYj0=', 'bz01NDAmYj0=', 'bz01NjAmYj0=', 'bz01ODAmYj0=',
              'bz02MDAmYj0=', 'bz02MjAmYj0=', 'bz02NDAmYj0=', 'bz02NjAmYj0=', 'bz02ODAmYj0=',
              'bz03MDAmYj0=', 'bz03MjAmYj0=', 'bz03NDAmYj0=', 'bz03NjAmYj0=', 'bz03ODAmYj0=',
              'bz04MDAmYj0=', 'bz04MjAmYj0=', 'bz04NDAmYj0=', 'bz04NjAmYj0=', 'bz04ODAmYj0=',
              'bz05MDAmYj0=', 'bz05MjAmYj0=', 'bz05NDAmYj0=', 'bz05NjAmYj0=', 'bz05ODAmYj0=',
             ]
number_of_items = 10

if __name__ == "__main__":
    pages = number_of_items // 20
    if number_of_items % 20 != 0:
        pages += 1
    apps_data = []
    for page in range(0, pages):
        products = requests.get(URL, headers=HEADERS, params=PARAMS)
        products.raise_for_status()
        productsList = products.json()['productsList']
        for prod in productsList:
            prod_properties = {'categories': prod['categories'],
                               'id': prod['productId'],
                               'company': prod['publisherName'],
                               'title': prod['title']
                               }
            prod_id = prod_properties["id"]
            URL_FOR_DETAILS = f'https://apps.microsoft.com/store/api/ProductsDetails/GetProductDetailsById/{prod_id}'
            details = requests.get(URL_FOR_DETAILS, headers=HEADERS, params=PARAMS_FOR_DETAILS)
            details.raise_for_status()
            app_details = details.json()
            app_date_str = app_details['releaseDateUtc']
            app_date = datetime.datetime.strptime(app_date_str.partition('T')[0], '%Y-%m-%d')
            prod_properties['release_date'] = app_date.date()
            prod_properties['contacts'] = [x['uri'] for x in app_details['supportUris']]
            company_name_encoded = urllib.parse.quote(prod_properties['company'].encode('utf8'))
            company_url = f'https://apps.microsoft.com/store/search?publisher={company_name_encoded}'
            prod_properties['company_url'] = company_url
            apps_data.append(prod_properties)
        PARAMS['Cursor'] = CURSOR_STR[page]

    for i in apps_data:
        print(i)
    print(len(apps_data))