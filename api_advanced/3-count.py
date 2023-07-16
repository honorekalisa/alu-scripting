#!/usr/bin/python3
""" Count it! """
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    base_url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0'}

    if after:
        params = {'after': after, 'limit': 100}
    else:
        params = {'limit': 100}

    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code != 200:
        print("Invalid subreddit or unable to access the subreddit.")
        return

    data = response.json()
    articles = data['data']['children']

    if counts is None:
        counts = {}

    if not articles:
        # Print the sorted count of keywords
        for keyword, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
            print(f"{keyword.lower()}: {count}")
        return

    for article in articles:
        title = article['data']['title'].lower()

        for keyword in word_list:
            keyword = keyword.lower()

            if keyword in title:
                counts[keyword] = counts.get(keyword, 0) + title.count(keyword)

    after = data['data']['after']
    count_words(subreddit, word_list, after, counts)
