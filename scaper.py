import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class Article:
    def __init__(self, content):
        self.content = content

    def exportArticles(self):
        pass


def getTodaysHTML():
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")
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


def scrapeArticles(articleLinks):
    scrapedArticles = []
    # Extract content from article
    for link in articleLinks:
        articleContent = ''
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'lxml')
        story = soup.findAll('p', class_='css-axufdj evys1bk0')
        for paragraphs in story:
            articleContent += paragraphs.get_text()
        scrapedArticles.append(Article(articleContent))

    return scrapedArticles


articleLinks = getArticleLinks()
articleList = scrapeArticles(articleLinks)

for article in articleList:
    print(article.content)

