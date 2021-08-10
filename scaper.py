import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from typing import List
import os
import json
import shutil


class Article:
    def __init__(self, content, url):
        self.content = content
        self.url = url

        urlParts = url.split("/")
        self.year = urlParts[3]
        self.month = urlParts[4]
        self.day = urlParts[5]
        self.path = urlParts[-1].split(".")[0]
        # todo add categories which can be dervied from the url

    def exportArticles(self):
        pass

    # https://stackoverflow.com/a/15538391/1489726
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def getTodaysHTML():
    driver = webdriver.Chrome()
    driver.get("https://www.nytimes.com/section/todayspaper")
    htmlText = driver.page_source
    driver.quit()
    return htmlText


def getArticleLinks():
    htmlText = getTodaysHTML()
    soup = BeautifulSoup(htmlText, 'lxml')
    highlightArticles = soup.findAll('h2', class_='css-byk1jx e4e4i5l1')
    rawHTMLLinks = []
    articleLinks = []

    # Retrieve highlight article links
    for articles in highlightArticles:
        rawHTMLLinks.append(str(articles.a))
    for link in rawHTMLLinks:
        beginning = link.find('/')
        end = link.find('">')
        articleLinks.append('https://www.nytimes.com' + link[beginning:end])

    # Retrieve remaining article links
    remainingArticles = soup.findAll('div', class_='css-141drxa')
    for articles in remainingArticles:
        rawHTMLLinks.append(str(articles.a))

    for element in rawHTMLLinks:
        beginning = element.find('/')
        end = element.find('">')
        formattedLink = element[beginning:end]
        # Prevent correction links to be added to the list
        if not formattedLink[12:23] == 'pageoneplus':
            articleLinks.append('https://www.nytimes.com' + element[beginning:end])

    print("Number of articles from today's paper: " + str(len(articleLinks)))
    return articleLinks


def scrapeArticles(articleLinks) -> List[Article]:
    scrapedArticles = []
    # Extract content from article
    for link in articleLinks:
        articleContent = ''
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'lxml')
        story = soup.findAll('p', class_='css-axufdj evys1bk0')
        for paragraphs in story:
            articleContent += paragraphs.get_text()
        scrapedArticles.append(Article(articleContent, link))

    return scrapedArticles


def write_articles_to_json_files(article_list: List[Article]):
    if not os.path.exists("data"):
        os.makedirs("data")
    for article in article_list:
        file_dir = f"data/{article.year}/{article.month}/{article.day}"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open(f"{file_dir}/{article.path}.json", "w") as f:
            f.write(article.to_json())


articleLinks = getArticleLinks()
articleList = scrapeArticles(articleLinks)

write_articles_to_json_files(articleList)
