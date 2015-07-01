# IWTBA
I Want To Be A (IWTBA) helps you bridge the gap between the job you want and the skills you need.

You can find the live app at [IWTBA.io](http://www.iwtba.io).

## Motivation

So you want to learn math, marketing, maybe some statistics. And you're one of the 13+ million people who have chosen to use online resources like [Coursera](https://www.coursera.org/) to get yourself there. Great! Browse away, Coursera is structured to be easy to navigate for searches like that.

But what if you want to be something more specific? You want to be a . That's a little harder. What's more, what if you don't want to be just any data scientist, you want to be [this data scientist](http://www.krux.com/company/join-us/?gnk=job&gni=8a7886654e28c19e014e36414f387156&gns=Indeed) and you've got the job listing to prove it.

Put that job posting in to IWTBA and it will return a list of courses you should take, structured and categorized in a way that makes it easy for a user to navigate.

## Data

IWTBA is intended to sit in the space between jobs and courses, and allow users to find the path from one to the other using unstructured text queries. To train the recommender, I needed data about jobs and courses.

#### Courses

Coursera has a [robust API](https://tech.coursera.org/app-platform/catalog/) which I used to scrape the raw text used for training (course title, course descriptions, about sections and syllabi) and metadata (id, categories and icons). Some additional fields seemed promising but either were too generic (course FAQs, recommended backgrounds) or had too many missing values (suggested readings, target audience) to be used.

#### Jobs

Two sources were used for job listings: Github and the NYC government.

##### Github
Listings and job titles were scraped from Github jobs using BeautifulSoup. 

##### NYC
NYC has a JSON data dump of job postings available as part of the open government movement.

## Model
The heart of the model is a matrix mapping courses and jobs to the latent topics discovered in both. Cosine similarity is used to find the most similar courses and jobs to a user-inputted job listing.

#### Matrix - [Latent Semantic Analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis] (LSA)
1. Job listings and course text data are cleaned and tokenized using stopwords, stemming and regex.
2. These text documents are converted into a vector space using [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf). TF-IDF is a numeric representation  of text documents that attempts to quantify how import each word is to the document.
3. The 24,000 dimension TF-IDF matrix is then reduced using [singular value decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition] (SVD) to a 1000 dimension matrix. The SVD matrix is comprised of few topics instead of many words.

These topics have interesting properties, one of which is handling multiple words with similar meanings. A latent topic can encode "programming" and "coding" as related concepts, whereas in TF-IDF each word is a separate feature.

#### Cosine Similarity
A similarity score is computed between the input and each job and course in the dataset, giving us an unordered bag of likely recommendations.

#### Topic Classification
A support vector classifier (SVC) is used to score each with one or many of 26 different categories (Math, Engineering, etc.). The model was tuned using coursera course data to have a 40% true positive rate and a 5% false positive rate.

Additionally, I ran the tuned model on each coursera course to determine which of its categories is its *primary* category.

#### Job Predictions and Recommendations
I return the 3 most similar jobs above a minimum threshold as job title predictions. The job title gives the user some insight into what data is driving the recommendations and confidence about those recommendations.

The topic classification are used to structure my recommendations. I recommend all courses that meet a very strict similarity threshold, and then for each category the job has I recommend courses that meet a lower threshold.

## The Webapp

The webapp was built using Flask on a Bootstrap template, and is hosted on AWS EC2. The recommendation page is responsive: headings change or disappear according to which categories I have recommendations for.

## Future Extensions
- Curriculum generation: recommending courses in a specific order.
- Adding additional learning resources such as YouTube and books.

## Packages Used
- BeautifulSoup
- NLTK
- sklearn
- NumPy
- Flask
