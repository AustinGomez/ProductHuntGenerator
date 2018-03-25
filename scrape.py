import requests
import json
from collections import namedtuple
import csv

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer 17b52c63689dd3a619ac0c54da7de3c7968644b5feaf087ae1d4de439e25b2cf",
    "Host": "api.producthunt.com"
}

with open('./producthunt.txt', 'a') as out:

    data = []
    for i in range(0, 12):

        r = requests.get("https://api.producthunt.com/v1/posts/all?sort_by=votes_count&order=desc&search[featured_year]=2016&search[featured_month]=" + str(i),
                         headers=headers)

        parsed = json.loads(r.content)
        for post in parsed["posts"]:
            out.write(post["name"].replace("\"", '') + ": " + post["tagline"] + "\n")