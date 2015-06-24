from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

import pickle
import numpy as np

import coursera_model as cm
from coursera_model import tokenize_text

c_tfidf_mat = pickle.load(open("./data/coursera/tfidf_mat.pkl", "rb" ))
c_course_list = pickle.load(open("./data/coursera/course_list.pkl", "rb" ))
c_vectorizer = pickle.load(open("./data/coursera/vectorizer.pkl", "rb" ))

# Form page to submit text
#============================================
# create page with a form on it
@app.route('/index.html')
@app.route('/index')
@app.route('/')
def submission_page():
    return render_template('index.html')

# Prediction page
#============================================
# create page with a form on it

# recommending
@app.route('/recommend', methods=['POST'])
def recommend_page():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['desc']
    table = cm.build_recommend_table(input_text, c_tfidf_mat, c_vectorizer, c_course_list, n=5)

    # need to pass last search as well as table
    # table = list of lists, first list is headers the rest are courses
    return render_template('recommend.html', desc=str(input_text), header=table[0], table=table[1:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)