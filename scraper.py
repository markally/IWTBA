import requests
from bs4 import BeautifulSoup


class Scraper():
    """A class for scraping job postings and course sites"""

    def __init__(self):
        pass

    def scrape_coursera_course(self, course_id):
        """scrape coursera course metadata
        can get all data by excluding the course ID. Won't include on-demand courses.

        full scrape url would look like the below

        https://api.coursera.org/api/catalog.v1/courses?id=2&fields=shortDescription,language,aboutTheCourse,faq,courseSyllabus&includes=categories'
        
        of these, FAQ may be less useful, as it has details that are not content related
        May not need category data if we already have course:category links from categories scrape
        """
        full_url = 'https://api.coursera.org/api/catalog.v1/courses?id=%s&fields=shortDescription,language,aboutTheCourse,faq,courseSyllabus&includes=categories' % (course_id)
        req = requests.get(full_url)
        return req.json()

    def scrape_coursera_category(self, cat_id):
        """scrape category metadata

        category metadata includes id, name, shortname, description, and courses"""
        full_url = 'https://api.coursera.org/api/catalog.v1/categories?id=%s&fields=description&includes=courses' % (cat_id)
        req = requests.get(full_url)
        return req.json()

        https://api.coursera.org/api/catalog.v1/courses?fields=shortDescription,language,aboutTheCourse,faq,courseSyllabus&includes=categories'

    def scrape_angellist():
        """scrape angellist job postings

        Currently, API requests require I be whitelisted. Waiting on reply from angellist team"""
        pass

    def scrape_indeed():
        """scrape indeed job postings"""
        pass