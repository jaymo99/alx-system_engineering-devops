#!/usr/bin/python3
"""Defines function that uses Reddit API pagination
"""

import requests

base_url = "https://www.reddit.com"
route = "/r/{}/hot.json"
headers = {
        "User-Agent": "Alx_tasks"
        }


def recurse(subreddit, hot_list=[], after=None):
    """returns a list containing all hot article titles for a subreddit
    """
    filters = "?limit=100"
    if after:
        filters += "&after={}".format(after)

    url = base_url + route.format(subreddit) + filters
    response = requests.get(url, headers=headers, allow_redirects=False)
    titles = []
    if (response.status_code == 200):
        data = response.json()['data']
        titles = [post['data']['title'] for post in data['children']]
        hot_list.extend(titles)

        if data['after']:
            recurse(subreddit, hot_list, data['after'])
        return hot_list
    return None
