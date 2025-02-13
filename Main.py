import pandas as pd
import streamlit as st
from api.twitter_api import fetch_twitter_trends
from api.reddit_api import fetch_reddit_posts

# API-Schlüssel und Tokens (diese solltest du sicher verwahren oder per .env-Datei einbinden)
twitter_bearer_token = "DEIN_TWITTER_BEARER_TOKEN"
reddit_client_id = "DEIN_REDDIT_CLIENT_ID"
reddit_secret_token = "DEIN_REDDIT_SECRET_TOKEN"

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
