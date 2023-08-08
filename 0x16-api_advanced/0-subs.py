#!/usr/bin/python3
"""Defines function to get number of subreddit subscribers
"""

import requests
import sys

base_url = "https://www.reddit.com"
route = "/r/{}/about.json"
headers = {
        "User-Agent": "Alx_tasks"
        }


def number_of_subscribers(subreddit):
    """returns the number of subscribers for a subreddit.
    """
    url = base_url + route.format(subreddit)
    response = requests.get(url, headers=headers, allow_redirects=False)
    if (response.status_code != 200):
        return 0
    data = response.json()
    subscribers = data['data']['subscribers']
    return subscribers
