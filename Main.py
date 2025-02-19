import pandas as pd
import streamlit as st
from api.reddit_api import generate_auth_url, handle_reddit_auth, get_reddit_posts
from api.reddit_trends import extract_shopping_trends
from decouple import config

# Funktion zur Kategorisierung von Trends
def categorize_trends(trends):
    """
    Kategorisiert die identifizierten Shopping-Trends in typische Kategorien.

    Parameters:
        trends (dict): Häufigkeitsanalyse der Shopping-Trends.

    Returns:
        dict: Kategorisierte Trends mit den zugehörigen Stichwörtern und deren Häufigkeit.
    """
    categories = {
        "Rabatte": ["sale", "deal", "discount", "bargain"],
        "Neue Produkte": ["new product", "new release", "latest"],
        "Preisvergleiche": ["price", "compare", "comparison", "cheaper", "cost"],
        "Allgemeine Angebote": ["buy", "offer", "available", "promotion"],
    }

    categorized_trends = {category: {} for category in categories}

    # Iteriere über die identifizierten Trends und ordne sie den Kategorien zu
    for trend, count in trends.items():
        for category, keywords in categories.items():
            if trend in keywords:
                categorized_trends[category][trend] = count

    return categorized_trends

### Authentifizierung REDDIT START ###
# Streamlit-Seite
st.title("Reddit Shopping Trends")

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
        
        # 4. Daten aus einem Subreddit abrufen (z. B. r/shopping)
        subreddit = "shopping"  # Du kannst auch andere Subreddits verwenden
        st.write(f"Abrufen von Posts aus dem Subreddit: {subreddit}")
        posts = get_reddit_posts(subreddit, token, limit=50)

        if posts:
            st.write(f"{len(posts)} Posts abgerufen.")
            
            # 5. Shopping-Trends analysieren
            trends = extract_shopping_trends(posts)

            # 6. Ergebnisse anzeigen
            st.subheader("Identifizierte Shopping-Trends:")
            if trends:
                for trend, count in trends.items():
                    st.write(f"- {trend}: {count} Erwähnungen")
            else:
                st.write("Keine Shopping-Trends gefunden.")
        else:
            st.write("Keine Posts abgerufen.")
    else:
        st.write("Fehler bei der Token-Anforderung!")
        
### Authentifizierung REDDIT END ###

# Daten kombinieren
data = reddit_data

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
