import pandas as pd
import streamlit as st

# Funktion zum Abrufen aller Trends
data = fetch_all_trends()

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

# Daten verarbeiten und kategorisieren
df = pd.DataFrame(data)
df["category"] = df["text"].apply(categorize_text)

# Streamlit-Dashboard
st.title("Shopping-Trend-Analyse")
st.dataframe(df)
st.bar_chart(df["category"].value_counts())
