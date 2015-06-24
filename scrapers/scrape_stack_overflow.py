# stackoverflow careers scrape
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pymongo import MongoClient

class StackOverflowScraper():

    def __init__(self, browser, seed_url, mongo_col):
        self.browser = browser
        self.url = seed_url
        self.col = mongo_col

    def scrape_posting(self):
        """
        Scrape a job posting using selenium.

        Input: URL
        Output: dictionary of useful info. 
                URL, job title, company name, body text, next job URL
        """
        # load page
        browser.get(self.url)

        # get metadata
        title = browser.find_element_by_css_selector(".title.job-link").text
        company = browser.find_element_by_css_selector(".employer").text
        tags = [ele.text for ele in browser.find_elements_by_css_selector(".post-tag.job-link")]
        
        # get posting body
        desc_eles = browser.find_elements_by_css_selector(".description")
        para_eles = browser.find_elements_by_tag_name('p')
        body = " ".join([ele.text for ele in para_eles])

        # get next url
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "next-job"))
            )
        finally:
            print "next_url did not load"
        next_url = browser.find_element_by_id("next-job").get_attribute("href")

        return {
            'url': self.url,
            'title': title,
            'company': company,
            'tags': tags,
            'body': body,
            'next_url': next_url
            }

    def scrape(self, max_jobs=300, delay=3.0, max_retries=3):
        """
        Scrape site for jobs according to parameters for max jobs scraped, 
        timing delays and max retries.
        """
        n_jobs = 0
        n_retries = 0
        while n_jobs < max_jobs and n_retries < 3:
                try:
                    print "Scraping job #%s" % n_jobs
                    time.sleep(delay)
                    posting_dict = self.scrape_posting()
                    self.url = posting_dict['next_url']
                    self.col.insert(posting_dict)
                    n_jobs += 1
                    n_retries = 0 # reset retries
                    print "Scraped %s from %s and stored. Job #%s..." \
                        % (posting_dict['title'], posting_dict['company'], n_jobs)
                except Exception as e:
                    print "Exception caught: %s" % e
                    n_retries += 1
        if n_retries == 3:
            print "Retry limit exceeded."
        if n_jobs == max_jobs:
            print "Maximum jobs scraped"
        print "Terminating scrape."


if __name__ == '__main__':
    # initialize browser
    print "Initializing webdriver..."
    browser = webdriver.Chrome()

    # start at seed job. This is the most recent posting at writing of this script.
    seed_url = 'http://careers.stackoverflow.com/jobs/91174/full-stack-web-developer-g-element-pte-ltd?a=uzLJ17G7cY0&so=p'

    # start MongoDB
    print "Spinning up Mongo Connection..."
    client = MongoClient()
    db = client.jobs
    col = db.stackoverflow

    print "Initializing scraper..."
    soc = StackOverflowScraper(browser, seed_url, col)
    print "Beginning scrape..."
    soc.scrape()

