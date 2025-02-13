import requests

def fetch_reddit_posts(client_id, secret_token):
    auth = requests.auth.HTTPBasicAuth(client_id, secret_token)
    data = {
        "grant_type": "password",
        "username": "DEIN_REDDIT_USERNAME",
        "password": "DEIN_REDDIT_PASSWORT"
    }
    headers = {"User-Agent": "ShoppingTrendApp/0.1"}
    token_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    token = token_response.json().get("access_token")
    
    headers["Authorization"] = f"bearer {token}"
    response = requests.get("https://oauth.reddit.com/r/shopping/new", headers=headers)
    
    if response.status_code == 200:
        posts = response.json().get("data", {}).get("children", [])
        return [{"text": post["data"]["title"], "platform": "Reddit"} for post in posts]
    else:
        print("Reddit API-Fehler:", response.status_code)
        return []
