from textblob import TextBlob
import pickle

# Load ML models
try:
    with open("models/category_model.pkl", "rb") as f: #read binary
        model_cat = pickle.load(f)

    with open("models/sentiment_model.pkl", "rb") as f:
        model_sent = pickle.load(f)

    with open("models/vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    ML_AVAILABLE = True
except Exception as e:
    print("❌ ML Load Error:", e)
    ML_AVAILABLE = False


def ml_predict_category(text):
    # raise Exception("CHECK WHERE THIS IS CALLED")
    text_vec = vectorizer.transform([text])
    
    probs = model_cat.predict_proba(text_vec)[0] # gives probab
    max_prob = float(max(probs))        # force float

    prediction = model_cat.predict(text_vec)[0]

    # force clean string
    if isinstance(prediction, (list, tuple)):
        prediction = prediction[0]

    prediction = str(prediction)    
    # prediction = str(model_cat.predict(text_vec)[0])  # force string

    return prediction, max_prob

def ml_predict_sentiment(text):
    # return model_sent.predict(text_vec)[0]

    text_vec = vectorizer.transform([text]) 

    probs = model_sent.predict_proba(text_vec)[0]
    max_prob = max(probs)
    prediction = model_sent.predict(text_vec)[0]

    return prediction, max_prob

# Sentiment Function
def get_sentiment(text):

    return TextBlob(text).sentiment.polarity

def get_final_sentiment(title, summary):
    text = (title + " " + summary).lower()

    if len(text.split()) <= 3:
        return "Neutral"

     # Try ML first
    if ML_AVAILABLE:
        # try:
        #     # print("Using ML for category")
        #     return ml_predict_sentiment(text) + " (ML)"
        # except Exception as e:
        #     print("❌ ML Error:", e)
        try:
            pred, conf = ml_predict_sentiment(text)

            # print(f"ML Sentiment: {pred}, Confidence: {conf:.2f}") # Debugging and gives eg.ML Sentiment: Positive, Confidence: 0.42

            if conf > 0.25:
                print("ML used")  # debug
                # return str(pred) + " (ML)"
                return str(pred)

            else:
                print("⚠️ Low confidence → using rules")

        except Exception as e:
            print("❌ ML Error:", e)
    # Fallback
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
    # text = text.lower().replace("watch:", "").replace("video:", "")

    text_clean = text.lower().replace("watch:", "").replace("video:", "")
    
    if len(text_clean.split()) <= 3:
        return "General"
        # return "General (Rule)"
    
    # Priority override (before ML)b
    # if any(word in text_clean for word in ["fuel", "price", "oil", "inflation", "market"]):
    #     return "Business (Rule)"

    # Try ML first
    if ML_AVAILABLE:
        # try:
            # print("Using ML for category")
            # return ml_predict_category(text_clean) + " (ML)"
            pred, conf = ml_predict_category(text_clean)

            # print(f"ML Category: {pred}, Confidence: {conf:.2f}")

            if conf > 0.25:
                # print("DEBUG:", pred, type(pred), conf, type(conf))
                print("ML used")  # debug
                return pred  
            else:
                print("⚠️ Low confidence → using rules")

        # except Exception as e:
        #     print("❌ ML Error:", e)
    # Fallback
    categories = {
        "Politics": ["election", "government", "minister", "pm", "president", "policy", "parliament", "nato", "war", "israel"],
        "Crime": ["police", "crime", "thief", "murder", "arrest", "kill", "fraud", "theft", "robbery", "burglary", "attack", "jailed", "prison", "beating", "assault"],
        "Sports": ["match", "tournament", "cricket", "football", "player", "goal", "score", "championship", "olympics", "pool", "league", "cup", "coach", "batter", "trainer", "race"],
        "Technology": ["ai", "technology", "software", "tech", "internet", "internet", "cyber", "digital"],
        "Business": ["market", "stock", "business", "economy", "company", "finance", "imf", "growth", "inflation", "fuel", "price", "oil"],
        "Entertainment": ["movie", "film", "celebrity", "actor", "show", "music", "tv", "series"]
    }

    for category, keywords in categories.items(): #items(key-c, value-k)
        words = text_clean.split()
        if any(word in words for word in keywords):
            return category
            # return category + " (Rule)"

    return "General"