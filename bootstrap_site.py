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

# Prediction page
#============================================
# create page with a form on it

# recommending
@app.route('/recommend', methods=['POST'])
def recommend_page():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['desc']
    table = model.build_recommend_table(input_text, n=5)

    # need to pass last search as well as table
    # table = list of lists, first list is headers the rest are courses
    return render_template('recommend.html', desc=input_text, header=table[0], table=table[1:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6543, debug=True)