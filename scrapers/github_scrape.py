# quick and dirty github scrape
# only 265 jobs, pages 0 to 5 (50 per page)

postings = []
for x in range(6):
    r = requests.get('https://jobs.github.com/positions.json?description=&page=%s' % x)
    postings.extend(r.json()) #r.json is a list of dicts

json.dump(postings, open('github_postings', 'w'))