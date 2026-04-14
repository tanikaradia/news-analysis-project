import json
import pickle #save model

from sklearn.feature_extraction.text import TfidfVectorizer #text→ no.
from sklearn.naive_bayes import MultinomialNB #Naive Bayes algo

# -- Load data
with open("../data/feedback.json", "r") as f:
    data = json.load(f)

texts = []
categories = []
sentiments = []

# -- Prepare dataset
for item in data:
    if item["feedback"] == "wrong":  # only learn from mistakes
        text = item["title"].lower()
        # add artificial keywords (boost learning)
        text += " " + item["user_category"].lower()
        texts.append(text)
        
        categories.append(item["user_category"])
        sentiments.append(item["user_sentiment"])

# Safety check, prevent crash
if len(texts) == 0:
    print("❌ No training data available!")
    exit()

# -- Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts) #X to no.

# -- Train models
model_cat = MultinomialNB()
model_cat.fit(X, categories) #no, label

model_sent = MultinomialNB()
model_sent.fit(X, sentiments)

# -- Save models
with open("../models/category_model.pkl", "wb") as f:
    pickle.dump(model_cat, f)

with open("../models/sentiment_model.pkl", "wb") as f:
    pickle.dump(model_sent, f)

with open("../models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Models trained successfully!")