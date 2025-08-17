import requests
import json
from json import JSONDecodeError
import csv

url = "http://localhost:3001/users"
params = {"page": 1, "per_page": 50}
with open('./user_details111.csv', 'a') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=['id', 'name', 'role', 'email', 'active'])
    writer.writeheader()
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()  # raises HTTPError if status >= 400

        try:
            data = resp.json()
            for d in data:

                id = d['id']
                name = d['name']
                role = d['role']
                email = d['email']
                status = d['active']

                if status is False:
                    writer.writerow({'id': id, 'name': name, 'role': role, 'email': email, 'active': status})



        except JSONDecodeError:
            print("Response was not valid JSON")
            print("Raw text:", resp.text)

    except requests.RequestException as e:
        print(f"Request failed: {e}")


