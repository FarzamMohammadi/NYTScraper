import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from typing import List
import os
import json
import shutil
import datetime


class Article:
    def __init__(self, title, subtitle, content, author, url):
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.author = author
        self.url = url

        url_parts = url.split("/")
        self.year = url_parts[3]
        self.month = url_parts[4]
        self.day = url_parts[5]
        self.category = url_parts[6]
        self.path = url_parts[-1].split(".")[0]

    # https://stackoverflow.com/a/15538391/1489726
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def scrape_todays_html():
    driver = webdriver.Chrome()
    driver.get("https://www.nytimes.com/section/todayspaper")
    html_text = driver.page_source
    driver.quit()
    return html_text


def get_article_links() -> List[str]:
    html_text = scrape_todays_html()
    soup = BeautifulSoup(html_text, 'lxml')
    highlight_articles = soup.findAll('h2', class_='css-byk1jx e4e4i5l1')
    raw_html_links = []
    article_links = []
    unwanted_categories = ['pageoneplus']
    year = str(datetime.date.today().year)

    # Retrieve highlight article raw links
    for articles in highlight_articles:
        raw_html_links.append(str(articles.a))

    # Retrieve remaining article raw links
    remaining_articles = soup.findAll('div', class_='css-141drxa')
    for articles in remaining_articles:
        raw_html_links.append(str(articles.a))
    # Convert raw links to properly formatted URL
    for link in raw_html_links:
        unwanted_article = False

        beginning = link.find('/')
        end = link.find('">')
        formatted_link = link[beginning:end]

        link_parts = formatted_link.split('/')

        # Prevent unwanted links to be added to the list
        try:
            article_year = link_parts[1]
            article_category = link_parts[4]

            if article_year != year:
                unwanted_article = True
            for category in unwanted_categories:
                if article_category == category:
                    unwanted_article = True
        except IndexError:
            unwanted_article = True

        if not unwanted_article:
            article_links.append('https://www.nytimes.com' + link[beginning:end])

    print("Number of articles from today's paper: " + str(len(article_links)))
    return article_links


def scrape_articles(article_links: List[str]) -> List[Article]:
    scraped_articles = []

    # Extract data from article
    for link in article_links:
        title, subtitle, content, author = '', '', '', ''

        # Extract content from article
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'lxml')
        article_content = soup.findAll('p', class_='css-axufdj evys1bk0')
        for paragraphs in article_content:
            content += ('\n' + paragraphs.get_text())

        # Extract author(s) from article
        article_authors = soup.find("div", class_="css-233int epjyd6m0")
        if article_authors is not None:
            for authors in article_authors:
                author += authors.get_text() + " "
            # If not found checks other means to extract the author names
        if author == '':
            article_authors = soup.find("p", class_="css-1hmtklo e1jsehar1")
            if article_authors is not None:
                author += article_authors.get_text()
        author = author.rstrip(" ")

        # Extract title from article
        article_title = soup.find('h1', {'data-testid': 'headline'})
        if article_title is None:
            title = ''
        else:
            title = article_title.get_text()

        # Extract subtitle from article
        article_subtitle = soup.find('p', id='article-summary')
        if article_subtitle is None:
            article_subtitle = soup.find('p', class_='css-1b6a17a e1wiw3jv0')

        if article_subtitle is None:
            subtitle = ''
        else:
            subtitle = article_subtitle.get_text()

        scraped_articles.append(Article(title, subtitle, content, author, link))
    return scraped_articles


def write_articles_to_json_files(article_list: List[Article]):
    if not os.path.exists("data"):
        os.makedirs("data")
    for article in article_list:
        file_dir = f"data/{article.year}/{article.month}/{article.day}"
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open(f"{file_dir}/{article.path}.json", "w") as f:
            f.write(article.to_json())


article_links = get_article_links()
article_list = scrape_articles(article_links)
write_articles_to_json_files(article_list)
