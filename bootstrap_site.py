from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)

import pickle
import numpy as np

from model import tokenize_description

tfidf_mat = pickle.load(open("./data/tfidf_mat.pkl", "rb" ))
job_titles = pickle.load(open("./data/job_titles.pkl", "rb" ))
vectorizer = pickle.load(open("./data/vectorizer.pkl", "rb" ))

# Form page to submit text
#============================================
# create page with a form on it
@app.route('/')
def submission_page():
    return render_template('index.html')

# predicting
@app.route('/predict', methods=['POST'])
def prediction_page():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['desc']

    input_tfidf = vectorizer.transform([input_text])
    cos_sims = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    most_sim_job = job_titles[np.argmax(cos_sims.todense())]
    return render_template('predict.html', desc=str(input_text), job=str(most_sim_job))

# My word counter app
#==============================================
# create the page the form goes to
@app.route('/closest_job', methods=['POST'] )
def closest_job():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['user_input']


    input_tfidf = vectorizer.transform([input_text])
    cos_sims = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    most_sim_job = job_titles[np.argmax(cos_sims.todense())]

    # now return your results
    return 'Approximate job title: %s' % (most_sim_job)

def return_closest_job():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['user_input']

    input_tfidf = vectorizer.transform([input_text])
    cos_sims = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    most_sim_job = job_titles[np.argmax(cos_sims.todense())]

    # now return your results
    return 'Approximate job title: %s' % (most_sim_job)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)