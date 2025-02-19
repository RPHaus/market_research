import urllib.parse
import requests
from api.reddit_auth import get_access_token
from decouple import config                         # Reddit App-Einstellungen (lade die sensiblen Daten aus der .env)

client_id = config("REDDIT_CLIENT_ID")
redirect_uri = "http://localhost:8501"  # Muss mit der Redirect-URI auf Reddit übereinstimmen
state = "random_state_string"  # Sicherer zufälliger String
scope = "read"  # Die angeforderten Berechtigungen

def generate_auth_url():
    """
    Erstellt die OAuth2-URL, um den Benutzer zur Reddit-Login-Seite weiterzuleiten.

    Returns:
        str: Die vollständige URL für die Benutzerweiterleitung.
    """
    auth_url = (
        f"https://www.reddit.com/api/v1/authorize?"
        f"client_id={client_id}&response_type=code"
        f"&state={state}&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&duration=permanent&scope={scope}"
    )
    return auth_url

def handle_reddit_auth(code):
    """
    Verarbeitet den erhaltenen Auth-Code und fordert ein Access Token von Reddit an.

    Parameters:
        code (str): Der von Reddit zurückgesandte Autorisierungs-Code.

    Returns:
        str: Das Access-Token, wenn die Anfrage erfolgreich ist, oder None.
    """
    if code:
        token = get_access_token(code)
        return token
    return None

def get_reddit_posts(subreddit, access_token, limit=10):
    """
    Holt eine Liste der neuesten Posts aus einem Subreddit.

    Parameters:
        subreddit (str): Der Name des Subreddits.
        access_token (str): Das Access-Token für die Reddit-API.
        limit (int): Die maximale Anzahl von Posts, die abgerufen werden sollen.

    Returns:
        list: Eine Liste der abgerufenen Reddit-Posts, oder eine leere Liste bei einem Fehler.
    """
    # URL für die Reddit-API, um Posts aus einem Subreddit abzurufen
    url = f"https://oauth.reddit.com/r/{subreddit}/new?limit={limit}"

    # Header mit dem Access-Token und einem User-Agent
    headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "ShoppingTrendApp/0.1"
    }

    # Sende eine GET-Anfrage an die Reddit-API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extrahiere die Posts aus der JSON-Antwort
        posts = response.json().get("data", {}).get("children", [])
        return [post["data"] for post in posts]  # Gib die Daten der Posts zurück
    else:
        print(f"Fehler beim Abrufen der Posts: {response.status_code}")
        return []
