-- read in table to DB

SELECT *
FROM category
WHERE LOWER(CONVERT(cat_title using latin1)) in
    ('arts',
    'statistics',
    'data_analysis',
    'physical_sciences',
    'earth_sciences',
    'medicine',
    'mathematics',
    'teacher_professional_development',
    'social_sciences',
    'artificial_intelligence',
    'economics',
    'finance',
    'information,'
    'technology'
    'design',
    'engineering',
    'health',
    'society',
    'law',
    'food',
    'nutrition',
    'business',
    'management',
    'humanities',
    'chemistry',
    'physics',
    'computer_science',
    'software_engineering',
    'biology',
    'life_sciences',
    'music',
    'film',
    'audio',
    'energy',
    'earth_sciences',
    'education')
AND cat_pages > 5;




-- 28 values

-- ORIGINAL COURSERA CATEGORIES
-- +-----------+-----------------+-----------+-------------+-----------+
-- | cat_id    | cat_title       | cat_pages | cat_subcats | cat_files |
-- +-----------+-----------------+-----------+-------------+-----------+
-- |      1832 | Arts            |       107 |          36 |         0 |
-- |     24251 | Physics         |        51 |          39 |         0 |
-- |     86989 | Chemistry       |       175 |          69 |         0 |
-- |    117621 | Education       |       252 |          59 |         0 |
-- |    121155 | Engineering     |       173 |          24 |         0 |
-- |    182910 | Law             |       103 |          27 |         0 |
-- |    196957 | Mathematics     |        28 |          19 |         0 |
-- |    198457 | Medicine        |        42 |          23 |         0 |
-- |    284773 | Social_sciences |       231 |          43 |         0 |
-- |    349022 | Social_Sciences |         2 |           0 |         0 |
-- |    452175 | LAW             |         0 |           0 |         0 |
-- |    643081 | EDUCATION       |         0 |           0 |         0 |
-- | 175345080 | ENGINEERING     |         0 |           0 |         0 |
-- +-----------+-----------------+-----------+-------------+-----------+


-- MODIFIED COURSERA CATEGORIES
-- +--------+-------------------------+-----------+-------------+-----------+
-- | cat_id | cat_title               | cat_pages | cat_subcats | cat_files |
-- +--------+-------------------------+-----------+-------------+-----------+
-- |    200 | Nutrition               |       234 |          26 |         0 |
-- |   1832 | Arts                    |       107 |          36 |         0 |
-- |  24251 | Physics                 |        51 |          39 |         0 |
-- |  24989 | Film                    |        61 |          29 |         0 |
-- |  54377 | Artificial_intelligence |       295 |          29 |         0 |
-- |  67751 | Biology                 |       124 |          29 |         0 |
-- |  77943 | Business                |       183 |          61 |         0 |
-- |  86989 | Chemistry               |       175 |          69 |         0 |
-- |  98333 | Computer_science        |        40 |          12 |         0 |
-- | 106877 | Data_analysis           |       126 |          12 |         0 |
-- | 116037 | Earth_sciences          |       141 |          24 |         0 |
-- | 116789 | Economics               |       290 |          52 |         0 |
-- | 117621 | Education               |       252 |          59 |         0 |
-- | 120841 | Energy                  |        70 |          29 |         0 |
-- | 121155 | Engineering             |       173 |          24 |         0 |
-- | 132856 | Finance                 |       392 |          23 |         1 |
-- | 153550 | Health                  |        44 |          40 |         0 |
-- | 161036 | Humanities              |       112 |          33 |         0 |
-- | 182910 | Law                     |       103 |          27 |         0 |
-- | 193927 | Management              |       469 |          32 |         0 |
-- | 196957 | Mathematics             |        28 |          19 |         0 |
-- | 198457 | Medicine                |        42 |          23 |         0 |
-- | 211205 | Music                   |        35 |          33 |         0 |
-- | 246970 | Physical_sciences       |        15 |           5 |         0 |
-- | 284773 | Social_sciences         |       231 |          43 |         0 |
-- | 284860 | Society                 |        89 |          59 |         0 |
-- | 285085 | Software_engineering    |        81 |          23 |         0 |
-- | 295061 | Statistics              |        93 |          59 |         0 |
-- +--------+-------------------------+-----------+-------------+-----------+
-- get top level pages matching coursera categories, with counts
-- Schema: cl_from is page ID, cl_to is category name (which may not have a page)
-- categories are stored with capitalized words and underscores instead of space

CREATE TABLE rootcat
SELECT cat_id, cat_title
FROM category
WHERE LOWER(CONVERT(cat_title using latin1)) in
    ('arts',
    'statistics',
    'data_analysis',
    'physical_sciences',
    'earth_sciences',
    'medicine',
    'mathematics',
    'teacher_professional_development',
    'social_sciences',
    'artificial_intelligence',
    'economics',
    'finance',
    'information,'
    'technology'
    'design',
    'engineering',
    'health',
    'society',
    'law',
    'food',
    'nutrition',
    'business',
    'management',
    'humanities',
    'chemistry',
    'physics',
    'computer_science',
    'software_engineering',
    'biology',
    'life_sciences',
    'music',
    'film',
    'audio',
    'energy',
    'earth_sciences',
    'education')
AND cat_pages > 5;

CREATE TABLE onedeep
SELECT 
    categorylinks.cl_to, 
    categorylinks.cl_from
FROM categorylinks
INNER JOIN rootcat
ON categorylinks.cl_to = rootcat.cat_title;

CREATE TABLE twodeep
SELECT
    pl_from,
    pl_title
FROM pagelinks
INNER JOIN onedeep
WHERE pagelinks.pl_from = onedeep.cl_from;

CREATE TABLE twodeepids
SELECT
    



CREATE TABLE twodeep
SELECT
    pl_from,
    pl_title
FROM pagelinks
INNER JOIN onedeep
WHERE pagelinks.pl_from = onedeep.cl_from;

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