import urllib.parse
from api.reddit_auth import get_access_token

# Reddit App-Einstellungen (lade die sensiblen Daten aus der .env)
from decouple import config
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
