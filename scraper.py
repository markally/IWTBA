import requests
from bs4 import BeautifulSoup

mysql -uroot

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
        

haiyu course recommendation

# grab wikipedia pages for all coursera categories
# create graph of results
# link coursera courses to subnodes based on categories tie to nodes
# webapp --> I want to know (search through terms)
# search through tree --> do you know

{u'Arts': [u'Arts'],
 u'Biology & Life Sciences': [u'Biology', u'Life Sciences'],
 u'Business & Management': [u'Business', u'Management'],
 u'Chemistry': [u'Chemistry'],
 u'Computer Science: Artificial Intelligence': [u'Computer Science',
  u'Artificial Intelligence'],
 u'Computer Science: Software Engineering': [u'Computer Science',
  u'Software Engineering'],
 u'Computer Science: Systems & Security': [u'Computer Science'],
 u'Computer Science: Theory': [u'Computer Science'],
 u'Economics & Finance': [u'Economics', u'Finance'],
 u'Education': [u'Education'],
 u'Energy & Earth Sciences': [u'Energy', u'Earth Sciences'],
 u'Engineering': [u'Engineering'],
 u'Food and Nutrition': [u'Food', u'Nutrition'],
 u'Health & Society': [u'Health', u'Society'],
 u'Humanities ': [u'Humanities'],
 u'Information, Tech & Design': [u'Information,', u'Technology', u'Design'],
 u'Law': [u'Law'],
 u'Mathematics': [u'Mathematics'],
 u'Medicine': [u'Medicine'],
 u'Music, Film, and Audio': [u'Music,', u'Film,', u'Audio'],
 u'Physical & Earth Sciences': [u'Physical Sciences', u'Earth Sciences'],
 u'Physics': [u'Physics'],
 u'Social Sciences': [u'Social', u'Sciences'],
 u'Statistics and Data Analysis': [u'Statistics', u'Data Analysis'],
 u'Teacher Professional Development': [u'Teacher Professional Development']}