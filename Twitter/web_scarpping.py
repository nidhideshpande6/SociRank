"""import requests

url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2021-04-16&'
       'sortBy=popularity&'
       'apiKey=878a2fc5700b4cd2a9eeec5115f7712b')

response = requests.get(url)

print (response.text)
"""

import requests
url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey=878a2fc5700b4cd2a9eeec5115f7712b')
#url = 'https://newsapi.org/v2/everything?q=keyword&apiKey=878a2fc5700b4cd2a9eeec5115f7712b'
response = requests.get(url)
for i in response.json()['articles']:
       print(i['title'])

