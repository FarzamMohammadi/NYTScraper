from bs4 import BeautifulSoup
import requests

addressToScrape = 'https://www.nytimes.com/interactive/2021/08/04/sports/olympics/sydney-mclaughlin-hurdles-400m-olympics.html?action=click&module=Top%20Stories&pgtype=Homepage'

htmlText = requests.get(addressToScrape).text
soup = BeautifulSoup(htmlText, 'lxml')
story = soup.findAll('p', class_='g-body')
for paragraphs in story:
    print(paragraphs.text)