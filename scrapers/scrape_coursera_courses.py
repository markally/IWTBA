import requests
import json

url = 'https://api.coursera.org/api/catalog.v1/courses?fields=id,shortName,name,language,shortDescription,smallIcon,aboutTheCourse,faq,courseSyllabus&includes=categories'

r = requests.get(url)
json.dump(r.json(), open('./data/coursera/coursera_courses.json', 'w'))