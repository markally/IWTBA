import requests
from bs4 import BeautifulSoup 
from pymongo import MongoClient

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
        try:
            link_dict = {}
            wiki_link_root = 'https://en.wikipedia.org/'

            r = requests.get(wiki_link_root + url)
            soup = BeautifulSoup(r.text)

            #get title
            title = soup.find('h1', {'id': 'firstHeading'}).text.strip()

            #main text
            main_body = soup.find('div', {'id': 'mw-content-text'})

            paras = main_body.find_all('p')
            links_list = []
            for x in paras:
                links_list.extend(x.find_all('a'))

            print "scraped %s at depth %s" % (url, depth)
            for link_tag in links_list:
                next_url = link['href']
                link_dict = {url: crawl_wiki_page(next_url, depth-1)}
            return link_dict
        except:
            return ""

if __name__ == '__main__':
    client = MongoClient()
    db = client.wikipedia
    col = db.categories

    first_url_root = 'https://en.wikipedia.org/wiki/'

    for cat in coursera_mod_cats:
        col.insert(crawl_wiki_page(first_url_root + cat, 5))






