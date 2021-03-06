from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

import pickle
import numpy as np
import dill

model = dill.load(open('./data/model.pkl'))

c_feat_mat = model.feat_mat[:len(model.course_list), :]

# Form page to submit text
#============================================
# create page with a form on it
@app.route('/index.html')
@app.route('/index')
@app.route('/')
def submission_page():
    return render_template('index.html')

# Recommendation page
#============================================
# create page with a form on it

# Recommending
@app.route('/recommend', methods=['POST'])
def recommend_page():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['desc']
    job_titles, best_course_ids, cat_list, has_recommendations = model.build_recommend_page(input_text)
    header = ['', 'Name', 'Description', 'All Categories']

    best_course_list = [model.build_course_row(c_id) for c_id in best_course_ids]

    cat_list_course_info = []
    for cat in cat_list:
        course_info = [model.build_course_row(c_id) for c_id in cat[1]]
        cat_list_course_info.append([cat[0], course_info])

    # need to pass last search as well as table
    # table = list of lists, first list is headers the rest are courses
    return render_template(
        'recommend.html',
        desc=input_text,
        titles=job_titles,
        best_courses=best_course_list,
        cat_list=cat_list_course_info,
        has_recommendations=has_recommendations,
        header=header)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6543, debug=True)

