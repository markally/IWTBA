import pandas as pd
import numpy as np
import json

import re
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

jobs_raw = open('./data/ny_jobs_data.json').read()
jobs_data = json.loads(jobs_raw)

jobs_columns = [col['fieldName'] for col in jobs_data['meta']['view']['columns']]

job_desc_index = jobs_columns.index('job_description')
job_title_index = jobs_columns.index('business_title') #there's also civic title

#could loop through this once
job_descriptions = [job[job_desc_index] for job in jobs_data['data']]
job_titles = [job[job_title_index] for job in jobs_data['data']]

#create regex pattern
re_pattern = re.compile('[^a-zA-Z]')

# create stemmer
stemmer = SnowballStemmer('english')

#create stopwords
eng_stop = set(stopwords.words('english'))

def tokenize_description(job_desc):
    """clean and tokenize a job description"""
    #should modify this to get rid of single letter words or ' caused junk
    clean_desc = re_pattern.sub(" ", job_desc).lower()
    tokenized_desc = [stemmer.stem(word) for word in clean_desc.split() if word not in eng_stop]
    return tokenized_desc

vectorizer = TfidfVectorizer(tokenizer=tokenize_description)
tfidf_mat = vectorizer.fit_transform(job_descriptions)

def get_most_similar_index(input_text, tfidf_mat, vectorizer):
    input_tfidf = vectorizer.transform([input_text])
    cos_sims = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    return np.argmax(cos_sims)

def get_most_sim_job(input_text, tfidf_mat, vectorizer):
    return job_titles[get_most_similar_index(input_text, tfidf_mat, vectorizer)]

# dump vectorizer and tfidf_mat to pickles

pickle.dump(vectorizer, open("./data/vectorizer.pkl", "wb" ))
pickle.dump(tfidf_mat, open( "./data/tfidf_mat.pkl", "wb" ))
pickle.dump(job_titles, open( "./data/job_titles.pkl", "wb" ))
