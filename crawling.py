import csv
import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent

homeUrl = "https://pubs.aip.org"
baseUrl = "https://pubs.aip.org/aip/apm/issue/"
standardYear = 2012
ua = UserAgent()

def processAllUrls(startYear, startMonth):
    urls = getUrls(startYear, startMonth)

    # urls = urls[:1]  # check once

    for url in urls:
        res = accessUrl(url[2])
        if res.status_code == 200:
            retPapers = parseAplPaperList(standardYear + url[0], url[1], res.text)
            if not retPapers:
                return
            else:
                convertToCsv(retPapers)


def convertToCsv(retPapers):
    #   return year, month, seq, title, authors, receivedDate, acceptedDate, publishDate
    with open('output.csv', 'a', newline='\n', encoding='utf-8') as file:
        writer = csv.writer(file)
        for paper in retPapers:
            writer.writerow(paper)


def getUrls(startYear, startMonth):
    allUrls = []
    for yearIter in range(startYear, 12):
        for monthIter in range(startMonth, 13):
            allUrls.append((yearIter, monthIter, baseUrl + str(yearIter) + "/" + str(monthIter)))
    return allUrls


def accessUrl(url):
    headers = {
        'User-Agent': ua.random,
    }
    res = requests.get(url, headers=headers)
    return res


def parseAplPaperList(year, month, paperList):
    retPapers = []
    soup = BeautifulSoup(paperList, features="html.parser")
    titles = soup.find_all('h5', class_='customLink')

    # titles = titles[:1]  # check once

    seq = 1
    for title in titles:
        tag = title.find('a')
        if tag.has_attr('href'):
            paperUrl = homeUrl + tag['href']
            res = accessUrl(paperUrl)
            time.sleep(5)
            if res.status_code == 200:
                retPaper = parseAplPaper(year, month, seq, res.text)
                if retPaper is not None:
                    retPapers.append(retPaper)
                    seq = seq + 1
                else:
                    return retPapers

    return retPapers


def parseAplPaper(year, month, seq, paper):
    print(f"Try to parse {year}/{month}/#{seq}...")
    soup = BeautifulSoup(paper, features="html.parser")
    titleEl = soup.find('h1', class_='wi-article-title article-title-main')
    if titleEl is None:
        print(f"Failed to parse html page.")
        return None
    else:
        title = titleEl.text.strip()
        authors = []
        authorsElement = soup.find_all('div', 'al-author-name')
        for element in authorsElement:
            authors.append(element.find('a').text)
        authors = ", ".join(authors)
        publishDate = convertDate(soup.find('span', 'article-date').text.strip())

        dates = soup.find_all('div', 'wi-date')
        receivedDate = convertDate(dates[0].text.strip())
        acceptedDate = convertDate(dates[1].text.strip())
        print(f"{year}/{month}/#{seq} : {title}")
        return year, month, seq, title, authors, receivedDate, acceptedDate, publishDate


def convertDate(date):
    dataObj = datetime.strptime(date, "%B %d %Y")
    return dataObj.strftime("%Y-%m-%d")


if __name__ == '__main__':
    processAllUrls(1, 1)
