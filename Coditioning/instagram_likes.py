import csv
from collections import Counter

freq = Counter()
def engagement_score_calculator(likes,comments,shares):
    return (pow(likes,1.2) + pow(comments,1.3) + pow(shares,1.4)) / 3

def function():
    posts = []
    with open('./input.csv', 'r') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in csvReader:
            score = engagement_score_calculator(float(row['likes']), float(row['comments']), float(row['shares']))
            posts.append({'post_id':row['post_id']}, {'score':score} )

    posts.sort(key=lambda x:x['score'], reverse=True)

    for post in posts[:10]:


print(function())

