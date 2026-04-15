from scraper import fetch_news

# def main():
#     news = fetch_news()
#     import json

#     with open("data/news.json", "w") as f:
#         json.dump(news, f, indent=4)

#     # for article in news[:5]:
#     #     print(article)

# if __name__ == "__main__":
#     main() #direct exec no import

# --Streamlit UI--
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) #py import(full path(path join(src(curr),up)))

import streamlit as st
from feedback.feedback_handler import save_feedback

MINISTRY_MAP = {
    "Politics": "External Affairs",
    "Business": "Finance",
    "Crime": "Home Affairs",
    "Sports": "Youth Affairs and Sports",
    "Technology": "Electronics and IT",
    "Entertainment": "Information & Broadcasting",
    "General": "General"
}

# gov_keywords = [
#     "india", "government", "ministry",
#     "pm", "modi", "policy", "parliament"
# ]

# HEADER + CATEGORY BAR
st.set_page_config(page_title="News Analysis", layout="wide")

col1, col2 = st.columns([8, 2])

with col1:
    st.title("📰 SMART SENTIMENT INSIGHTS")

with col2:
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh News"):
        st.rerun()

st.markdown("---")

news = fetch_news()

# filtered_news = []
# for article in news:
#     title = article["title"].lower()
#     if any(word in title for word in gov_keywords):
#         filtered_news.append(article)
# news = filtered_news

from src.analyzer import classify_category, get_final_sentiment
for article in news:
    text = article["title"]

    category = classify_category(text)
    sentiment = get_final_sentiment(text, "")

    article["category"] = category
    article["ministry"] = MINISTRY_MAP.get(category, "General")
    article["sentiment"] = sentiment

# CATEGORY FILTER ---
selected_category = st.selectbox(
    "Filter Category",
    [
    "All",
    "External Affairs",
    "Finance",
    "Home Affairs",
    "Youth Affairs and Sports",
    "Electronics and IT",
    "Information & Broadcasting",
    "General"
]
)

# APPLY FILTER ---
if selected_category != "All":
    news = [article for article in news if article["ministry"] == selected_category]

language = st.selectbox("Language", ["English", "Hindi"])
if language == "Hindi":
    st.info("Hindi support coming soon")

# 3-COLUMN NEWS GRID ---
cols = st.columns(3)

# CATEGORY-BASED IMAGES ---
def get_image(category):
    base_path = os.path.join("assets")
    category = category.lower()
    if "sports" in category:
        return os.path.join(base_path, "sports.jpg")
    elif "business" in category:
        return os.path.join(base_path, "business.jpg")
    elif "technology" in category:
        return os.path.join(base_path, "technology.jpg")
    elif "politics" in category:
        return os.path.join(base_path, "politics.jpg")
    elif "crime" in category:
        return os.path.join(base_path, "crime.jpg")    
    elif "entertainment" in category:
        return os.path.join(base_path, "entertainment.jpg")
    else:
        return os.path.join(base_path, "default.jpg")

for idx, article in enumerate(news):

    with cols[idx % 3]:

        key = f"{article['title']}_{idx}"
        # ---- Initialize states ----
        if key + "_done" not in st.session_state:
            st.session_state[key + "_done"] = False

        if key + "_edit" not in st.session_state:
            st.session_state[key + "_edit"] = False

        done = st.session_state[key + "_done"]
        edit = st.session_state[key + "_edit"]

        # ---- CARD UI ----
        with st.container():
            # Replace image line ---
            st.image(get_image(article["category"]), width=220)
            st.markdown(
                f"<div style='font-size:25px; font-weight:600;'>{article['title']}</div>",
                unsafe_allow_html=True
            )
            st.markdown(f"[🔗 Read more]({article['link']})")
            # Confidence (%) + Better Sentiment Display ---
            st.write(f"🏷️ {article['category']}")
            st.write(f"🏛️ {article['ministry']}")

            sentiment = article["sentiment"]

            if sentiment == "Negative":
                print(f"🚨 ALERT: Negative news → {article['title']} | Ministry: {article['ministry']}")

            if sentiment == "Positive":
                st.success("🟢 Positive")
            elif sentiment == "Negative":
                st.error("🔴 Negative")
            else:
                st.info("🔵 Neutral")

            # ---- If NOT submitted ----
            if not done and not edit:
                col1, col2 = st.columns(2)

                if col1.button("👍 Correct", key=key + "c"):
                    save_feedback({
                        "title": article["title"],
                        "predicted_sentiment": article["sentiment"],
                        "predicted_category": article["category"],
                        "user_sentiment": article["sentiment"],
                        "user_category": article["category"],
                        "feedback": "correct"
                    })

                    st.success("Feedback saved ✅")
                    st.session_state[key + "_done"] = True
                    st.rerun()

                if col2.button("👎 Wrong", key=key + "_wrong"):
                    st.session_state[key + "_edit"] = True
                    st.rerun()

            # ---- Correction UI ----
            if edit and not done:
                st.write("### Correct values:")

                new_sentiment = st.selectbox(
                    "Sentiment",
                    ["Positive", "Neutral", "Negative"],
                    key=key + "_sent"
                )

                new_category = st.selectbox(
                    "Category",
                    [
                        "General", "Politics", "Sports",
                        "Technology", "Business", "Crime"
                    ],
                    key=key + "_cat"
                )

                if st.button("Submit", key=key + "_submit"):
                    save_feedback({
                        "title": article["title"],
                        "predicted_sentiment": article["sentiment"],
                        "predicted_category": article["category"],
                        "user_sentiment": new_sentiment,
                        "user_category": new_category,
                        "feedback": "wrong"
                    })

                    st.success("Correction saved ✅")
                    st.session_state[key + "_done"] = True
                    st.session_state[key + "_edit"] = False
                    st.rerun()

            if done:
                st.info("Already submitted ✅")

        st.markdown("---")