import requests

def fetch_twitter_trends(bearer_token):
    url = "https://api.twitter.com/2/tweets/search/recent"
    query = {
        "query": "#shopping OR #fashion OR #tech OR #beauty",
        "tweet.fields": "text,created_at",
        "max_results": 10
    }
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    
    response = requests.get(url, headers=headers, params=query)
    
    if response.status_code == 200:
        data = response.json()
        tweets = [{"text": tweet["text"], "platform": "Twitter"} for tweet in data.get("data", [])]
        return tweets
    else:
        print("Twitter API-Fehler:", response.status_code)
        return []
