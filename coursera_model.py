import numpy as np
import json

import re
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

import pickle

#create regex pattern
re_pattern = re.compile('[^a-zA-Z]')

# create stemmer
stemmer = SnowballStemmer('english')

#create stopwords
eng_stop = set(stopwords.words('english'))

def concatenate_text_data(course_dict):
    name = course_dict['name']
    faq = course_dict['faq']
    syllabus = course_dict['courseSyllabus']
    short_desc = course_dict['shortDescription']
    about = course_dict['aboutTheCourse']
    return " ".join([name, faq, syllabus, short_desc, about])

def tokenize_text(text):
    """clean and tokenize a job description"""
    #should modify this to get rid of single letter words or ' caused junk
    clean_text = re_pattern.sub(" ", text).lower()
    tokenized_desc = [stemmer.stem(word) for word in clean_text.split() if word not in eng_stop]
    return tokenized_desc

def get_top_n_words(course_id, n=5):
    index_val = course_id_to_index[int(course_id)]
    top_n_index = np.argsort(tfidf_mat.getrow(index_val).todense())[-1:-(n + 1):-1, 0]
    words = [feature_mapping[i] for i in top_n_index.tolist()[0]]
    tfidf_vals = tfidf_mat[index_val, top_n_index].data
    return zip(words, tfidf_vals)

def get_n_most_similar_indices(input_text, tfidf_mat, vectorizer, n=5):
    input_tfidf = vectorizer.transform([input_text])
    cos_sims_sparse = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    n = min(n, cos_sims_sparse.nnz) # only return elements with non-zero similarity
    cos_sims = cos_sims_sparse.todense() #shape: (m x 1)
    top_n_indices = np.argsort(cos_sims, axis=0)[-1:-(n + 1):-1, 0]
    return top_n_indices.ravel().tolist()[0]

def build_recommend_table(input_text, tfidf_mat, vectorizer, course_list, n=5):
    indices = get_n_most_similar_indices(input_text, tfidf_mat, vectorizer, n=n)
    header = ['Course Name', 'Course Description']
    table = [header]
    for i in indices:
        course = course_list[i]
        name = course['name']
        short_desc = course['shortDescription']
        url = 'https://www.coursera.org/course/' + course['shortName']
        table.append([name, short_desc, url])
    return table

# dump objs to pickles
if __name__ == '__main__':
    with open('./data/coursera/coursera_courses.json') as c_file:
        coursera_courses = json.load(c_file)
        course_list = coursera_courses['elements']

    course_id_to_index = {}
    course_text_list = []

    for i, course in enumerate(coursera_courses['elements']):
        course_id_to_index[course['id']] = i
        course_text_list.append(concatenate_text_data(course))

    vectorizer = TfidfVectorizer(tokenizer=tokenize_text)
    tfidf_mat = vectorizer.fit_transform(course_text_list)
    feature_mapping = vectorizer.get_feature_names()

    pickle.dump(vectorizer, open("./data/coursera/vectorizer.pkl", "wb" ))
    pickle.dump(tfidf_mat, open( "./data/coursera/tfidf_mat.pkl", "wb" ))
    pickle.dump(course_list, open( "./data/coursera/course_list.pkl", "wb" ))
    pickle.dump(course_id_to_index, open("./data/coursera/course_id_to_index.pkl", "wb" ))
