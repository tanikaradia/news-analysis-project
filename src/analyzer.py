from textblob import TextBlob

# Sentiment Function
def get_sentiment(text):
    # polarity = TextBlob(text).sentiment.polarity #Analyze text- tone, ret polarity
    # if polarity > 0:
    #     return "Positive"
    # elif polarity < 0:
    #     return "Negative"
    # else:
    #     return "Neutral"
    return TextBlob(text).sentiment.polarity

def get_final_sentiment(title, summary):
    text = (title + " " + summary).lower()
    
    # Rule: Question / uncertainty → Neutral
    if "?" in title or "could" in title.lower():
        return "Neutral"
    
    # ---- Logic: Strong negative keywords (override) ----
    negative_keywords = ["murder", "kill", "death", "attack", "crime", "killer"]
    neutral_keywords = ["stroke", "hospital", "ill", "injury"]
    positive_keywords = ["success", "win", "winner", "won", "victory", "growth", "triumph", "historic"]

    if any(word in text for word in negative_keywords):
        return "Negative"
    if any(word in text for word in neutral_keywords):
        return "Neutral"
    if any(word in text for word in positive_keywords):
        return "Positive"

    # ---- Score-based logic ----
    title_score = get_sentiment(title)
    summary_score = get_sentiment(summary)

    # # Rule 1: If title is strong → trust it
    # if title_sent != "Neutral":
    #     return title_sent

    # # Rule 2: If title neutral → use summary
    # return summary_sent

    # strongly opinionated → trust it
    if abs(title_score) > 0.2:
        return "Positive" if title_score > 0 else "Negative"

    # Otherwise weak → combine both
    avg_score = (title_score + summary_score) / 2

    if avg_score > 0.05:
        return "Positive"
    elif avg_score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Category Function
def classify_category(text):
    # remove noisy words
    text = text.lower().replace("watch:", "").replace("video:", "")

    categories = {
        "Politics": ["election", "government", "minister", "pm", "president"],
        "Crime": ["police", "crime", "thief", "murder", "arrest"],
        "Sports": ["match", "tournament", "cricket", "football", "player"],
        "Technology": ["ai", "technology", "software", "tech", "internet"],
        "Business": ["market", "stock", "business", "economy", "company"],
        "Entertainment": ["movie", "film", "celebrity", "actor", "show"]
    }

    for category, keywords in categories.items(): #items(key-c, value-k)
        if any(word in text for word in keywords): #keyword in text?: first match
            return category
    
    return "General"
    