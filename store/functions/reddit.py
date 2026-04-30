import requests


def fetch_reddit_posts(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    headers = {
        "User-Agent": "django-reddit-app/1.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    data = response.json()

    posts = []

    for item in data["data"]["children"]:
        post = item["data"]

        posts.append({
            "title": post.get("title"),
            "author": post.get("author"),
            "url": "https://reddit.com" + post.get("permalink", "")
        })

    return posts
