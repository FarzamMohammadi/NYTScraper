from bs4 import BeautifulSoup
import requests

todaysPaperURL = 'https://www.nytimes.com/section/todayspaper'
htmlText = requests.get(todaysPaperURL).text
soup = BeautifulSoup(htmlText, 'lxml')
story = soup.findAll('p', class_='css-axufdj evys1bk0')
for paragraphs in story:
    print(paragraphs.text)
