import requests
from decouple import config

def get_access_token(auth_code):
    """
    Tauscht einen erhaltenen Autorisierungs-Code gegen ein Access Token aus, 
    um auf die Reddit API zuzugreifen.

    Parameters:
        auth_code (str): Der Code, den Reddit nach erfolgreicher Anmeldung 
                         und Autorisierung zurückgibt.

    Returns:
        str: Das Access Token, wenn die Anfrage erfolgreich ist. 
             Andernfalls None.
    """
    # Lade die Reddit Client-ID und das Secret Token aus der .env-Datei
    client_id = config("REDDIT_CLIENT_ID")
    secret_token = config("REDDIT_SECRET_TOKEN")
    
    # Die Redirect URI, die bei der App-Registrierung auf Reddit angegeben wurde
    # Diese muss mit der URI übereinstimmen, die beim Abrufen des Auth-Codes verwendet wurde
    redirect_uri = config("REDDIT_REDIRECT_URI")  # Lokale Entwicklung oder Cloud-URL

    # Erstelle die HTTP-Basic-Authentifizierung mit Client ID und Secret Token
    # Diese Methode wird benötigt, um Reddit mitzuteilen, dass die App berechtigt ist
    # ein Token anzufordern.
    auth = requests.auth.HTTPBasicAuth(client_id, secret_token)

    # Daten, die für die Access Token-Anfrage benötigt werden
    data = {
        "grant_type": "authorization_code",  # OAuth2 Grant-Typ
        "code": auth_code,                  # Der erhaltene Autorisierungs-Code
        "redirect_uri": redirect_uri        # Die bei der App-Registrierung hinterlegte Redirect URI
    }

    # Header für die Anfrage. Der User-Agent sollte eine kurze Beschreibung der App enthalten.
    headers = {"User-Agent": "ShoppingTrendApp/0.1"}

    # Sende eine POST-Anfrage an die Reddit-API, um das Access Token zu erhalten
    response = requests.post("https://www.reddit.com/api/v1/access_token", 
                             auth=auth, data=data, headers=headers)

    # Überprüfe, ob die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        # Extrahiere das Access Token aus der JSON-Antwort und gib es zurück
        token = response.json().get("access_token")
        return token
    else:
        # Bei einem Fehler den Statuscode ausgeben und None zurückgeben
        print(f"Fehler bei der Token-Anforderung: {response.status_code}")
        return None
