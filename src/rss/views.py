from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import feedgenerator,datetime

def index(request):
    xml = makeXml(getData());
    return HttpResponse(xml,content_type = 'application/xml');

def getData():
    url = 'https://sakurazaka46.com/s/s46/diary/blog/list?ima=0000';
    response = requests.get(url);
    soup = BeautifulSoup(response.content,'html.parser');

    ul = soup.find(attrs = { 'class': 'com-blog-part'});

    dataObj = [];
    for li in ul.find_all('li'):
        title = li.find('h3').text;
        author = li.find(attrs = { 'class': 'name'}).text;
        link = 'https://sakurazaka46.com' + li.find('a').get('href').replace('&','&amp;');
        description = li.find(attrs = {'class': 'lead'}).text;
        pubDate = li.find(attrs = {'class': 'date'}).text;
        # pubDate = getPubDate(link);
        pubDateSplit = pubDate.split('/');
        pubDateArray = [int(pubDateSplit[0]),int(pubDateSplit[1]),int(pubDateSplit[2])];

        dataObj.append({'title':title,'author':author,'link':link,'description':description,'pubDate':pubDateArray});
    return dataObj;

def getPubDate(url):
    response = requests.get(url);
    soup = BeautifulSoup(response.content,'html.parser');

    div = soup.find(attrs = {'class': 'blog-foot'})
    return div.find(attrs = {'class': 'date'}).text;

def makeXml(data):
    feed = feedgenerator.Rss201rev2Feed(
    title = 'SAKURAZAKA46 BLOG',
    link = 'https://sakurazaka46.com/s/s46/diary/blog/list',
    feed_url = 'http://www.example.com/blog/rss',
    description = 'SAKURAZAKA46 BLOG',
    author_name = 'SAKURAZAKA46',
    pubdate = datetime.datetime.now());
    
    for tempObj in data:
        feed.add_item(
        title = tempObj['title'],
        link = tempObj['link'],
        description = tempObj['description'],
        author_name = tempObj['author'],
        pubdate = datetime.datetime(tempObj['pubDate'][0],tempObj['pubDate'][1],tempObj['pubDate'][2]));

    return feed.writeString('utf-8');

