import numpy as np
import json

import re
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer

import dill
from bs4 import BeautifulSoup

from sklearn.decomposition import TruncatedSVD
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer, Normalizer

class IWTBA():
    def __init__(self, svd=True, categorizer=True):
        # Triggers for building models
        self.svd=svd
        self.categorizer=categorizer
        # Initialize Tokenizer Parts
        # Create regex pattern
        self.re_pattern = re.compile('[^a-zA-Z]')

        # Create stemmer
        self.stemmer = SnowballStemmer('english')

        # Create stopwords
        self.eng_stop = set(stopwords.words('english'))

        # Placeholders
        self.feat_mat = None
        self.feat_labels = None

        self.course_list = None
        self.course_id_to_index = None
        self.jobs_titles = None

        self.cat_id_to_name = None
        self.course_cats_binarized = None
        self.label_arr_to_cat_id = None

    # ----------------
    # Read in Corpus
    # ----------------
    def concatenate_coursera_text_data(self, course_dict):
        """helper function for parsing coursera courses"""
        name = course_dict['name']
        syllabus = BeautifulSoup(course_dict['courseSyllabus']).text
        short_desc = course_dict['shortDescription']
        about = BeautifulSoup(course_dict['aboutTheCourse']).text
        return " ".join([name, syllabus, short_desc, about])

    def _get_coursera_corpus(self):
        """collect coursera course text and metadata"""
        with open('./data/coursera/coursera_courses.json') as c_file:
            coursera_courses = json.load(c_file)

        course_id_to_index = {} # dict to allow reverse searching from id
        course_text_list = []
        course_list = []
        course_categories = []

        i = 0
        for course in coursera_courses['elements']:
            if course['language'] == 'en':
                course_id_to_index[course['id']] = i
                course_text_list.append(self.concatenate_coursera_text_data(course))
                course_list.append(course)
                if self.categorizer:
                    course_categories.append(course['links'].get('categories', [-1]))
                i += 1


        if self.categorizer:
            # get category list
            cat_info_list = coursera_courses['linked']['categories']
            self.cat_id_to_name = {cat['id']:
                {'name':cat['name'], 'shortName':cat['shortName']} for cat in cat_info_list}

            # binarize labels and discard low-count categories    
            mlb = MultiLabelBinarizer()
            course_cats_binarized = mlb.fit_transform(course_categories)

            # filter to only tags with > 40 courses
            mask = course_cats_binarized.sum(axis=0) > 40
            course_cats_binarized = course_cats_binarized[:, mask]
            self.course_cats_binarized = course_cats_binarized

            # create dict to get back from masked index, to index, to id
            label_arr_to_cat_id = {}
            for i, k in enumerate(mask.nonzero()[0].tolist()):
                label_arr_to_cat_id[i] = mlb.classes_[k]

            self.label_arr_to_cat_id = label_arr_to_cat_id


        return course_list, course_text_list, course_id_to_index

    def _get_nyc_corpus(self):
        """collect nyc gov't job descriptions and titles"""
        ny_jobs_raw = open('./data/nyc/ny_jobs_data.json').read()
        ny_jobs_data = json.loads(ny_jobs_raw)

        ny_jobs_columns = [col['fieldName'] for col in ny_jobs_data['meta']['view']['columns']]

        ny_jobs_desc_index = ny_jobs_columns.index('job_description')
        ny_jobs_title_index = ny_jobs_columns.index('business_title') #there's also civic title

        ny_jobs_descriptions = []
        ny_jobs_titles = []

        for job in ny_jobs_data['data']:
            ny_jobs_descriptions.append(job[ny_jobs_desc_index])
            ny_jobs_titles.append(job[ny_jobs_title_index])

        return ny_jobs_titles, ny_jobs_descriptions

    def _get_github_corpus(self):
        """collect github job descriptions and titles"""
        git_data = json.load(open('./data/github/github_postings'))
        git_jobs_titles = []
        git_jobs_descriptions = []

        for job in git_data:
            git_jobs_titles.append(job['title'])
            git_jobs_descriptions.append(BeautifulSoup(job['description']).text)

        return git_jobs_titles, git_jobs_descriptions

    def get_corpus(self, coursera=True, nyc=True, github=True):
        """collect data sets, return combined corpus and store metadata"""
        combined_text = []
        job_titles = []
        if coursera:
            course_list, course_text_list, course_id_to_index = self._get_coursera_corpus()
            combined_text += course_text_list
            self.course_list = course_list
            self.course_id_to_index = course_id_to_index
        if nyc:
            ny_jobs_titles, ny_jobs_descriptions = self._get_nyc_corpus()
            combined_text += ny_jobs_descriptions
            job_titles.extend(ny_jobs_titles)
        if github:
            git_jobs_titles, git_jobs_descriptions = self._get_github_corpus()
            combined_text += git_jobs_descriptions
            job_titles.extend(git_jobs_titles)
        if job_titles:
            self.job_titles = job_titles

        return combined_text

    #--------------------
    # Model Building and Processing
    #--------------------
    def tokenize_text(self, text):
        """clean and tokenize a job description"""
        #should modify this to get rid of single letter words or ' caused junk
        clean_text = self.re_pattern.sub(" ", text).lower()
        tokenized_desc = [self.stemmer.stem(word) for word in clean_text.split() if word not in self.eng_stop]
        return tokenized_desc

    def _fit_svd(self, feat_mat, svd_comps):
        self.svd = TruncatedSVD(n_components=svd_comps)
        feat_mat = self.svd.fit_transform(feat_mat)
        self.normalizer = Normalizer(copy=False)
        self.normalizer.transform(feat_mat)
        return feat_mat        

    def _fit_categorizer(self):
        classifier = SVC(kernel='linear', probability=True, class_weight='auto')
        cat_clf = OneVsRestClassifier(classifier)
        cat_clf.fit(self.feat_mat[:len(self.course_list), :], self.course_cats_binarized)
        self.categorizer = cat_clf

    def fit(self, svd_comps=1000):
        """fit the tfidf vectorizer (and svd) and store it and the resulting feature matrix"""
        vectorizer = TfidfVectorizer(tokenizer=self.tokenize_text)
        feat_mat = vectorizer.fit_transform(self.get_corpus())
        self.vectorizer = vectorizer
        if self.svd:
            feat_mat = self._fit_svd(feat_mat, svd_comps)
        self.feat_mat = feat_mat
        if self.categorizer:
            self._fit_categorizer()
        self.feat_labels = vectorizer.get_feature_names()

    def vectorize(self, input_text):
        vector = self.vectorizer.transform([input_text])
        if self.svd:
            vector = self.svd.transform(vector)
            self.normalizer.transform(vector)
        return vector

    #--------------------
    # Result Functions
    #--------------------
    def _get_course_sims(self, input_text):
        """get course similarities."""
        input_vect = self.vectorize(input_text)
        c_feat_mat = self.feat_mat[:len(self.course_list), :]
        cos_sims = np.dot(c_feat_mat, input_vect.T) #nx1 shape
        if type(cos_sims) != np.ndarray: #tfidf is in sparse format
            cos_sims = np.array(cos_sims.todense())
        return cos_sims   

    def get_n_most_similar_course_indices(self, input_text, n=5, threshold=.3):
        """get n most similar indices, sorted, from a sparse matrix"""
        input_vect = self.vectorize(input_text)
        c_feat_mat = self.feat_mat[:len(self.course_list), :]
        cos_sims = np.dot(c_feat_mat, input_vect.T)
        if type(cos_sims) != np.ndarray: #tfidf is in sparse format
            cos_sims = np.array(cos_sims.todense())
        n = min(n, np.sum(cos_sims > threshold)) # return only good courses
        n = max(n, 1) # return at least 1 course
        top_n_indices = np.argsort(cos_sims, axis=0)[-1:-(n + 1):-1, 0]
        return top_n_indices.ravel().tolist()

    def build_recommend_table(self, input_text, n=5):
        """
        Collect meta data from recommended courses,
        and then return a table for displaying recommendations.
        """
        indices = self.get_n_most_similar_course_indices(input_text, n=n)
        header = ['Course Name', 'Course Description']
        table = [header]
        for i in indices:
            course = self.course_list[i]
            name = course['name']
            short_desc = course['shortDescription']
            url = 'https://www.coursera.org/course/' + course['shortName']
            table.append([name, short_desc, url])
        return table

    def _get_job_category_scores(self, input_text):
        """
        Get decision function results for categorizer.
        """
        vect = self.vectorize(input_text)
        cat_scores = self.categorizer.decision_function(vect)
        return cat_scores

    def get_job_categories(self, input_text, threshold=.034):
        """
        Classify posting and return categories.
        Threshold of 0.034 corresponds to a .05 false positive rate
        """
        cat_scores = self._get_job_category_scores(input_text)
        cat_predictions = cat_scores > threshold
        cat_names = []
        for i in cat_predictions.nonzero()[1].tolist():
            cat_id = self.label_arr_to_cat_id[i]
            cat_name = self.cat_id_to_name[cat_id]['name']
            cat_names.append(cat_name)
        return cat_names

    def get_n_most_similar_job_indices(self, input_text, n=3, threshold=.3):
        """get n most similar job indices, sorted"""
        input_vect = self.vectorize(input_text)
        c_feat_mat = self.feat_mat[len(self.course_list):, :]
        cos_sims = np.dot(c_feat_mat, input_vect.T)
        if type(cos_sims) != np.ndarray: #tfidf is in sparse format
            cos_sims = np.array(cos_sims.todense())
        n = min(n, np.sum(cos_sims > threshold)) # return only good courses
        n = max(n, 1) # return at least 1 course
        top_n_indices = np.argsort(cos_sims, axis=0)[-1:-(n + 1):-1, 0]
        return top_n_indices.ravel().tolist()

    def get_job_titles(self, input_text, n=3, threshold=.3):
        """return titles from indices."""
        top_n_indices = self.get_n_most_similar_job_indices(input_text, n=n, threshold=threshold)
        titles = []
        for i in top_n_indices:
            job_title = self.job_titles[i]
            if job_title not in titles:
                titles.append(job_title)
        return titles

    def build_course_row(self, course_id):
        """collect course metadata and build row for recommendation page.
        Input: Course ID
        Output: List of strings.
            Course IMG as url
            Course Title
            Course URL
            Course Description
            Course Categories
        """
        course = self.course_list[course_id]
        c_name = course['name']
        c_img = course['smallIcon']
        #url works for coursera only
        c_url = 'https://www.coursera.org/course/' + course['shortName']
        c_desc = course['shortDescription']
        c_cats = [self.cat_id_to_name[cat_id]['name'] for cat_id in course['links']['categories']]
        return c_name, c_img, c_url, c_desc, c_cats

    def build_recommend_page(self, input_text, thresh=.3):
        # get n job titles > threshold
        job_titles = self.get_job_titles(input_text, n=3, threshold=thresh)

        # get and sort course similarities
        course_sims = self._get_course_sims(input_text) #nx1 shape
        sorted_sim_indices = course_sims.argsort(axis=0)[::-1, :] #sorted descending

        # get sorted course similarity indices for sims > thresh

        # get category scores for job posting
        job_cat_scores = self._get_job_category_scores(input_text)

        # get category scores for each recommended course
        # 1 * job cat score if cat has tag, 0 otherwise
        course_cat_scores = job_cat_scores * self.course_cats_binarized

        # for each course, largest value becomes it's parent category
        course_parent_cat = np.argmax(course_cat_scores, axis = 1)

        # best recommendations thresholds
        # get courses with cos sim > high thresh
        high_thresh = .5
        best_course_ids = []
        for course_id in sorted_sim_indices:
            if course_sims[course_id] > high_thresh:
                best_course_ids.append(course_id)
                
        # for each category in job_cat_scores > thresh
        # create list of courses with sim > thresh
        good_courses_by_cat_arr_id = {}
        thresh_mask = (course_sims > thresh).ravel()
        for i, score in enumerate(job_cat_scores[0]):
            if score > .034:
                cat_mask = course_parent_cat == i
                cat_and_thresh_mask = np.logical_and(cat_mask, thresh_mask)
                valid_courses = cat_and_thresh_mask.nonzero()[0].tolist()
                if valid_courses:
                    good_courses_by_cat_arr_id[i] = valid_courses

        cat_list = []
        for k, v in good_courses_by_cat_arr_id.iteritems():
            cat_id = model.label_arr_to_cat_id[k]
            cat_name = self.cat_id_to_name[cat_id]['name']
            cat_list.append([cat_name, v])

        return job_titles, best_course_ids, cat_list

if __name__ == '__main__':
    model = IWTBA()
    model.fit()

    dill.dump(model, open("./data/model.pkl", "wb"), 2)