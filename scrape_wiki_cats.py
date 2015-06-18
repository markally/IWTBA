import requests
from bs4 import BeautifulSoup 
from pymongo import MongoClient
import time

coursera_mod_cats = (
    'arts',
    'statistics',
    'data_analysis',
    'physical_sciences',
    'earth_sciences',
    'medicine',
    'mathematics',
    'teacher_professional_development',
    'social_sciences',
    'artificial_intelligence',
    'economics',
    'finance',
    'information,'
    'technology'
    'design',
    'engineering',
    'health',
    'society',
    'law',
    'food',
    'nutrition',
    'business',
    'management',
    'humanities',
    'chemistry',
    'physics',
    'computer_science',
    'software_engineering',
    'biology',
    'life_sciences',
    'music',
    'film',
    'audio',
    'energy',
    'earth_sciences',
    'education')

def crawl_wiki_page(url, depth):
    if depth > 0:
        link_dict = {}
        wiki_link_root = 'https://en.wikipedia.org' #links add /wiki/link-title

        time.sleep(1)
        r = requests.get(wiki_link_root + url)
        soup = BeautifulSoup(r.text)

        #get title
        # title = soup.find('h1', {'id': 'firstHeading'}).text.strip()

        #main text
        main_body = soup.find('div', {'id': 'mw-content-text'})

        paras = main_body.find_all('p')
        links_list = []
        for x in paras:
            links_list.extend(x.find_all('a'))

        print "scraped %s at depth %s" % (url, depth)
        for link_tag in links_list:
            next_url = link_tag['href']
            if next_url.startswith('/wiki'):
                link_dict = {url: crawl_wiki_page(next_url, depth-1)}
        if link_dict:
            return link_dict
    else:
        return 'none'

if __name__ == '__main__':
    client = MongoClient()
    db = client['wikipedia']
    col = db['categories']

    for cat in coursera_mod_cats:
        url = 'wiki/' + cat
        col.insert(crawl_wiki_page(url, 5))
        time.sleep(1)






