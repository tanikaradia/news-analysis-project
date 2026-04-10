from textblob import TextBlob

# Sentiment Function
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity #Analyze text- tone, ret polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"


# Category Function
def classify_category(text):
    text = text.lower()

    # remove noisy words
    text = text.replace("watch:", "").replace("video:", "")

    if any(word in text for word in ["election", "government", "minister", "pm", "president"]):
        return "Politics"

    elif any(word in text for word in ["police", "crime", "thief", "murder", "arrest"]):
        return "Crime"

    elif any(word in text for word in ["match", "tournament", "cricket", "football", "player"]):
        return "Sports"

    elif any(word in text for word in ["ai", "technology", "software", "tech", "internet"]):
        return "Technology"

    elif any(word in text for word in ["market", "stock", "business", "economy", "company"]):
        return "Business"

    elif any(word in text for word in ["movie", "film", "celebrity", "actor", "show"]):
        return "Entertainment"

    return "General"