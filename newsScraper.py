import requests
import functools
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm, tqdm_notebook

from key import NEWSAPI_KEY
from utils import SELECTED_CATEGORY

def getSources():
    '''Return the new's sources avaible'''
    source_url = 'https://newsapi.org/v1/sources?language=en'
    response = requests.get(source_url).json()
    sources = []
    for source in response['sources']:
        sources.append(source['id'])
    return sources

def mapping():
    '''Map each data sources to its category'''
    d = {}
    response = requests.get('https://newsapi.org/v1/sources?language=en')
    response = response.json()
    for s in response['sources']:
        d[s['id']] = s['category']
    return d

def category(source, m):
    '''Return the category of a source given the category dictionary'''
    try:
        return m[source]
    except:
        return 'NC'

def getDailyNews():
    sources = getSources()
    d = mapping()
    url = 'https://newsapi.org/v1/articles?source={0}&sortBy={1}&apiKey={2}'
    responses = []
    for i, source in tqdm_notebook(enumerate(sources), total=len(sources)):

        if(category(source, d) in SELECTED_CATEGORY):
            try:
                u = url.format(source, 'top', NEWSAPI_KEY)
            except:
                u = url.format(source, 'latest', NEWSAPI_KEY)

            response = requests.get(u)
            r = response.json()
            try:
                for article in r['articles']:
                    article['source'] = source
                responses.append(r)
            except:
                print('Rate limit exceeded ... please wait and retry in 6 hours')
                return None

    articles = list(map(lambda r: r['articles'], responses))
    articles = list(functools.reduce(lambda x,y: x+y, articles))
    print("{} articles scraped".format(len(articles)))

    news = pd.DataFrame(articles)
    news = news.dropna()
    news = news.drop_duplicates()
    news.reset_index(inplace=True, drop=True)

    news['category'] = news['source'].map(lambda s: category(s, d))
    news['scraping_date'] = datetime.now()

    try:
        aux = pd.read_csv('./data/news/news.csv')
        aux = aux.append(news)
        aux = aux.drop_duplicates('url')
        aux.reset_index(inplace=True, drop=True)
        aux.to_csv('./data/news/news.csv', encoding='utf-8', index=False)
    except:
        news.to_csv('./data/news/news.csv', index=False, encoding='utf-8')

    print('Done')

def main():
    # sources = getSources()
    # m = mapping()
    # for s in sources:
    #     print("{}\t\t{}".format(s, m[s]))
    getDailyNews()

if __name__ == '__main__':
    main()
