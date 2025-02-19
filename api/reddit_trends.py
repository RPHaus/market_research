def extract_shopping_trends(posts):
    """
    Analysiert Reddit-Posts, um mögliche Shopping-Trends zu identifizieren.

    Parameters:
        posts (list): Eine Liste von Reddit-Posts (Dictionary).

    Returns:
        dict: Eine Häufigkeitsanalyse von trendigen Wörtern oder Phrasen, die auf Shopping hinweisen.
    """
    from collections import Counter
    import re

    # Beispielhafte Shopping-bezogene Stichwörter (kann erweitert werden)
    shopping_keywords = ["sale", "deal", "discount", "buy", "price", "new product", "bargain"]

    trend_counter = Counter()

    # Durchsuche die Titel und Inhalte der Posts nach Stichwörtern
    for post in posts:
        title = post.get("title", "").lower()
        body = post.get("selftext", "").lower()

        # Überprüfe, ob ein Stichwort in Titel oder Body vorkommt
        for keyword in shopping_keywords:
            if re.search(rf"\b{keyword}\b", title) or re.search(rf"\b{keyword}\b", body):
                trend_counter[keyword] += 1

    return trend_counter
