import urllib.parse
import urllib.request

url = 'https://www.nytimes.com/live/2021/08/04/world/covid-delta-variant-vaccine'

response = urllib.request.urlopen(url)
webContent = response.read()

f = open('obo-t17800628-33.html', 'wb')
f.write(webContent)
f.close