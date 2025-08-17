import json

def calc(budget,clicks):
    return budget/clicks

def function():
    with open('./sample.json', 'r') as jsonFile:
        data = json.load(jsonFile)

        for d in data:
            impression = float(d['impressions'])
            clicks = float(d['clicks'])
            conv = float(d['conversions'])
            id = d['campaign_id']
            budget = float(d['budget'])

            score = calc(budget,clicks)

            for i in range():
                print(f"campaign_id:{id} CPC: {score}")





print(function())