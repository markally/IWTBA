from flask import Flask
from flask import request
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
    return '''
    <form action="/closest_job" method='POST' >
        <input type="text" name="user_input" />
        <input type="submit" />
    </form>
    '''

# My word counter app
#==============================================
# create the page the form goes to
@app.route('/closest_job', methods=['POST'] )
def closest_job():
    # get data from request form, the key is the name you set in your form
    input_text = request.form['user_input']

    input_tfidf = vectorizer.transform([input_text])
    cos_sims = tfidf_mat.dot(input_tfidf.T) #vects already have unit norm
    most_sim_job = job_titles[np.argmax(cos_sims)]

    # now return your results
    return 'Approximate job title: %s' % (most_sim_job)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)