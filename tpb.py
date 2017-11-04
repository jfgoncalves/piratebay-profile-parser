#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import dateparser
import datetime
from feedgen.feed import FeedGenerator
import yaml

def parsePubDate(date, tz):
    # Formatting this case manually for dateparser
    if 'Y-day' in date:
        date = date.replace('Y-day', 'Yesterday')

    return dateparser.parse(date, settings={'TIMEZONE': 'Europe/Stockholm', 'TO_TIMEZONE': tz, 'RETURN_AS_TIMEZONE_AWARE': True})

def getData(baseURL,tpbUser, UA, tz):
    # Ensuring latest items on top
    rURL = baseURL+'/user/'+tpbUser+'/0/3'
    page = requests.get(rURL, headers={'user-agent': UA})
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', attrs={'id':'searchResult'})

    #Cleaning the DOM a little
    table.find('thead').extract()
    table.find('td', attrs={'class':'vertTh'}).extract()
    # Removing Pagination
    table('tr')[-1].extract()

    infoList = []
    rows = table.find_all('tr')

    for row in rows:
        metaInfo = row.find('font', attrs={'class':'detDesc'}).text.replace(u'\xa0', u' ').split(', ')
        network = row.find_all('td', attrs={'align':'right'})
        #For list use from here
        title = row.find('a', attrs={'class':'detLink'}).text
        guid = baseURL + row.find('a', attrs={'class':'detLink'})['href']
        magnet = row.find('a', attrs={'title':'Download this torrent using magnet'})['href']
        author = metaInfo[2].replace('ULed by ', '')
        size = metaInfo[1].replace('Size ', '')
        tempPubDate = parsePubDate(metaInfo[0].replace('Uploaded ', ''), tz)
        pubDate = tempPubDate.strftime('%a, %d %b %Y %H:%M:%S %z')
        seeders = network[0].text
        leechers = network[1].text

        infoRow = [title, guid, author, pubDate, size, magnet, seeders, leechers]
        infoList.append(infoRow)

    return infoList

def createRSS(data, title, desc, link, o):
    rss = FeedGenerator()
    rss.title(title)
    rss.description(desc)
    rss.link(href=link, rel='self', type='application/rss+xml')
    rss.language('en')

# 0 title, 1 guid, 2 author, 3 pubdate, 4 size, 5 magnet, 6 seeders, 7 leechers
    for item in data:
        entry = rss.add_entry()
        entry.title(item[0])
        entry.author(name=item[2])
        entry.id(item[5])
        entry.guid(guid=item[1], permalink=True)
        entry.pubdate(item[3])
        entry.link(href=item[5])
        entry.description('Size: '+item[4]+', '+item[6]+' seeders and '+item[7]+' leechers.')

    rss.rss_str(pretty=True)
    rss.rss_file(filename=o, pretty=True)

if __name__ == "__main__":
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    data = getData(cfg['baseURL'], cfg['tpbUser'], cfg['UA'], cfg['tz'])
    createRSS(data, cfg['rssTitle'], cfg['rssDesc'], cfg['rssLink'], cfg['outputDest'])
