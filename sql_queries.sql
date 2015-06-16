-- read in table to DB




-- get top level pages matching coursera categories, with counts
-- Schema: cl_from is page ID, cl_to is category name (which may not have a page)
-- categories are stored with capitalized words and underscores instead of space
SELECT cl_to, COUNT(*)
FROM categorylinks
WHERE LOWER(CONVERT(cl_to using latin1)) in
    ('arts',
    'statistics_and_data_analysis',
    'physical_&_earth_sciences',
    'medicine',
    'mathematics',
    'teacher_professional_development',
    'social_sciences',
    'computer_science:_artificial_intelligence',
    'economics_&_finance',
    'information,_tech_&_design',
    'engineering',
    'health_&_society',
    'law',
    'food_and_nutrition',
    'computer_science:_systems_&_security',
    'business_&_management',
    'computer_science:_theory',
    'humanities_',
    'chemistry',
    'physics',
    'computer_science:_software_engineering',
    'biology_&_life_sciences',
    'music,_film,_and_audio',
    'energy_&_earth_sciences',
    'education')
GROUP BY cl_to;

-- 

SELECT cl_to, cl_from
FROM categorylinks
WHERE LOWER(CONVERT(cl_to using latin1)) in
    ('arts',
    'statistics_and_data_analysis',
    'physical_&_earth_sciences',
    'medicine',
    'mathematics',
    'teacher_professional_development',
    'social_sciences',
    'computer_science:_artificial_intelligence',
    'economics_&_finance',
    'information,_tech_&_design',
    'engineering',
    'health_&_society',
    'law',
    'food_and_nutrition',
    'computer_science:_systems_&_security',
    'business_&_management',
    'computer_science:_theory',
    'humanities_',
    'chemistry',
    'physics',
    'computer_science:_software_engineering',
    'biology_&_life_sciences',
    'music,_film,_and_audio',
    'energy_&_earth_sciences',
    'education')
GROUP BY cl_to
LIMIT 10;

-- Create table containing pages linking to coursera categories
-- not all categories are found -- some have different names

CREATE TABLE test_cat
SELECT cl_to, cl_from
FROM categorylinks
WHERE LOWER(CONVERT(cl_to using latin1)) in
    ('arts',
    'statistics_and_data_analysis',
    'physical_&_earth_sciences',
    'medicine',
    'mathematics',
    'teacher_professional_development',
    'social_sciences',
    'computer_science:_artificial_intelligence',
    'economics_&_finance',
    'information,_tech_&_design',
    'engineering',
    'health_&_society',
    'law',
    'food_and_nutrition',
    'computer_science:_systems_&_security',
    'business_&_management',
    'computer_science:_theory',
    'humanities_',
    'chemistry',
    'physics',
    'computer_science:_software_engineering',
    'biology_&_life_sciences',
    'music,_film,_and_audio',
    'energy_&_earth_sciences',
    'education');

-- Create paths of length 3: Category --> Page (as ID) --> Next Page (as name)
-- Will need to convert page 1 to a name for use in graph

SELECT 
    test_cat.cl_to,
    pagelinks.pl_from,
    pagelinks.pl_title
FROM pagelinks
INNER JOIN test_cat
ON pagelinks.pl_from = test_cat.cl_from;

-- Same as above, but outputting to csv

SELECT 
    test_cat.cl_to,
    pagelinks.pl_from,
    pagelinks.pl_title
FROM pagelinks
INNER JOIN test_cat
ON pagelinks.pl_from = test_cat.cl_from
INTO OUTFILE '/Users/datascientist/Documents/mark/IWTBA/data/wikibooks_3_path.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';