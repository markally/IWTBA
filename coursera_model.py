import pandas as pd
import numpy as np
import json

import re
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

with open('./data/coursera_courses.json') as c_file:
    coursera_courses = json.load(c_file)

def concatenate_text_data(course_dict):
    name = course_dict['name']
    faq = course_dict['faq']
    syllabus = course_dict['courseSyllabus']
    short_desc = course_dict['shortDescription']
    about = course_dict['aboutTheCourse']
    return " ".join([name, faq, syllabus, short_desc, about])

course_id_index = {}
course_text_list = []

for i, course in enumerate(coursera_courses['elements']):
    course_id_index[course['id']] = i
    course_text_list.append(concatenate_text_data(course))

#create regex pattern
re_pattern = re.compile('[^a-zA-Z]')

# create stemmer
stemmer = SnowballStemmer('english')

#create stopwords
eng_stop = set(stopwords.words('english'))

def tokenize_text(text):
    """clean and tokenize a job description"""
    #should modify this to get rid of single letter words or ' caused junk
    clean_text = re_pattern.sub(" ", text).lower()
    tokenized_desc = [stemmer.stem(word) for word in clean_text.split() if word not in eng_stop]
    return tokenized_desc

vectorizer = TfidfVectorizer(tokenizer=tokenize_text)
tfidf_mat = vectorizer.fit_transform(course_text_list)
feature_mapping = vectorizer.get_feature_names()

def get_top_n_words(course_id, n=5):
    index_val = course_id_index[int(course_id)]
    top_n_index = np.argsort(tfidf_mat.getrow(index_val).todense())[:, -n:]
    words = [feature_mapping[i] for i in top_n_index.tolist()[0]]
    tfidf_vals = tfidf_mat[index_val, top_n_index].data
    return zip(words, tfidf_vals)
get_top_n_words(index_val)

def get_most_similar_index(input_text, tfidf_mat, vectorizer):
    input_tfidf = vectorizer.transform([input_text])
    cos_sims = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    return np.argmax(cos_sims)

def get_most_sim_job(input_text, tfidf_mat, vectorizer):
    return job_titles[get_most_similar_index(input_text, tfidf_mat, vectorizer)]

# # dump vectorizer and tfidf_mat to pickles

# pickle.dump(vectorizer, open("./data/vectorizer.pkl", "wb" ))
# pickle.dump(tfidf_mat, open( "./data/tfidf_mat.pkl", "wb" ))
# pickle.dump(job_titles, open( "./data/job_titles.pkl", "wb" ))
