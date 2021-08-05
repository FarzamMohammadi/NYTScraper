import urllib.request
from datetime import date

todaysPaperURL = 'https://www.nytimes.com/section/todayspaper'

response = urllib.request.urlopen(todaysPaperURL)
webContent = response.read()

today = date.today()
f = open(str(today) + '.html', 'wb')
f.write(webContent)
f.close()
