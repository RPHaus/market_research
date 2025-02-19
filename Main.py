import pandas as pd
import streamlit as st
from api.twitter_api import fetch_twitter_trends
from api.reddit_api import generate_auth_url, handle_reddit_auth, get_reddit_posts
from decouple import config

### Authentifizierung REDDIT START ###
# Streamlit-Seite
st.title("Reddit OAuth2-Login")
st.write("Klicke auf den untenstehenden Link, um dich bei Reddit anzumelden.")

# 1. OAuth2 URL generieren und anzeigen
auth_url = generate_auth_url()
st.markdown(f"[Bei Reddit anmelden]({auth_url})")

# 2. Den Auth-Code aus der URL abfangen
code = st.experimental_get_query_params().get("code", [None])[0]  # Den 'code'-Parameter aus der URL lesen

# 3. Wenn ein Code vorhanden ist, hole das Access Token
if code:
    st.write("Code erhalten! Hole Access-Token...")
    token = handle_reddit_auth(code)

    if token:
        st.write("Erfolgreich authentifiziert!")
        st.write(f"Dein Reddit-Access-Token lautet: {token}")
    else:
        st.write("Fehler bei der Token-Anforderung!")
        
### Authentifizierung REDDIT END ###


# Daten abrufen
twitter_data = fetch_twitter_trends(twitter_bearer_token)
reddit_data = fetch_reddit_posts(reddit_client_id, reddit_secret_token)

# Daten kombinieren
data = twitter_data + reddit_data

# Kategorien-Erkennung (wie zuvor)
def categorize_text(text):
    categories = {
        "Fashion": ["dress", "jeans", "shoes", "fashion"],
        "Technik": ["laptop", "smartphone", "tech", "gadgets"],
        "Kosmetik": ["skincare", "makeup", "beauty", "lipstick"],
        "Home & Living": ["sofa", "furniture", "home", "kitchen"],
    }

    for category, keywords in categories.items():
        if any(re.search(rf"\b{keyword}\b", text, re.IGNORECASE) for keyword in keywords):
            return category
    return "Sonstiges"

# Daten in DataFrame umwandeln
df = pd.DataFrame(data)
df["category"] = df["text"].apply(categorize_text)

# Streamlit-Dashboard
st.title("Shopping-Trend-Analyse")
st.dataframe(df)
st.bar_chart(df["category"].value_counts())
