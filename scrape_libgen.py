import requests
import html5lib
import sys
import html5lib
from bs4 import BeautifulSoup
import time


def get_libgen_data(soup):
    body = soup.find_all('table')
    one = body[1]
    counter = len(one.find_all('tr'))
    data = {}

    for each_row in range(1, counter):
        row = one.find_all('tr')[each_row]
        author = row.find_all('td')[1].text
        title = row.find_all('td')[0].find_all('a')[0].text.strip()
        if title.strip():
            pass
        else:
            title = row.find_all('td')[0].find_all('a')[1].text.strip()
        publisher = row.find_all('td')[3].text
        year_published = row.find_all('td')[3].text
        num_pages = row.find_all('td')[5].text
        size = row.find_all('td')[6].text
        extension = row.find_all('td')[7].text
        download_link = row.find_all('td')[8].a["href"]

        data.update({each_row: {'author': author, 'title':title, 'publisher':publisher, 'year_published':year_published,
                                'num_pages':num_pages, 'extension': extension, 'download_link': download_link, 'size': size}})
    return data


def get_download_url(link):
    r = requests.get(link)
    download_soup = BeautifulSoup(r.content, "html5lib")
    download_link = download_soup.find_all('table',{ "id" : "main" })[0].find_all('a')[0]['href']
    full_link = link.split("/")[0] + "//" + link.split("/")[2] + '/' + download_link
    return full_link
