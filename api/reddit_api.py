import requests
from decouple import config

def authenticate_reddit():
    """Authentifiziert sich bei Reddit und gibt das Token zurück."""
    
    # Lade die Anmeldedaten aus der .env-Datei
    client_id = config("REDDIT_CLIENT_ID")
    secret_token = config("REDDIT_SECRET_TOKEN")
    username = config("REDDIT_USERNAME")
    password = config("REDDIT_PASSWORD")
    
    # Authentifizierung bei Reddit (OAuth2 mit "password"-Grant-Type)
    auth = requests.auth.HTTPBasicAuth(client_id, secret_token)
    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    headers = {"User-Agent": "ShoppingTrendApp/0.1"}
    
    # Token-Request
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    
    # Überprüfe, ob die Authentifizierung erfolgreich war
    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print(f"Fehler bei der Authentifizierung: {response.status_code}")
        return None
