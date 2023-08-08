#!/usr/bin/python3
"""Defines function to get titles of top 10 hot posts
"""

import requests
import sys

base_url = "https://www.reddit.com"
route = "/r/{}/hot.json"
headers = {
        "User-Agent": "Alx_tasks"
        }


def top_ten(subreddit):
    """prints the first 10 hot posts listed for a given subreddit.
    """
    filters = "?limit=10"
    url = base_url + route.format(subreddit) + filters
    response = requests.get(url, headers=headers, allow_redirects=False)
    titles = []
    if (response.status_code == 200):
        data = response.json()
        titles = [post['data']['title'] for post in data['data']['children']]

    if len(titles) > 0:
        for title in titles:
            print(title)
        return
    print(None)
