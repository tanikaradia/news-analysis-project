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
from utils.feedback_handler import save_feedback

news = fetch_news()

for article in news:
    st.subheader(article["title"])
    st.write("Sentiment:", article["sentiment"])
    st.write("Category:", article["category"])

    col1, col2 = st.columns(2) #split screen to 2

    if col1.button("👍 Correct", key=article["title"] + "c"): # key: Maintain state= titlec (c suffix)
        save_feedback({
            "title": article["title"],
            "predicted_sentiment": article["sentiment"],
            "predicted_category": article["category"],
            "user_sentiment": article["sentiment"],
            "user_category": article["category"],
            "feedback": "correct"
        })
        st.success("Feedback saved ✅")

    if col2.button("👎 Wrong", key=article["title"] + "w"): # remember user action after rerun
        st.session_state[article["title"]] = True

    if st.session_state.get(article["title"], False): #true else false
        st.write("### Correct the values:") # markdown

        new_sentiment = st.selectbox(
            "Correct Sentiment",
            ["Positive", "Neutral", "Negative"],
            key=article["title"] + "sent"
        )

        new_category = st.selectbox(
            "Correct Category",
            ["General", "Politics", "Sports", "Technology", "Business", "Crime"],
            key=article["title"] + "cat"
        )

        if st.button("Submit Correction", key=article["title"] + "submit"): 
            save_feedback({
                "title": article["title"],
                "predicted_sentiment": article["sentiment"],
                "predicted_category": article["category"],
                "user_sentiment": new_sentiment,
                "user_category": new_category,
                "feedback": "wrong"
            }) #update wrong

            st.success("Correction saved ✅")

            # Reset state
            st.session_state[article["title"]] = False
            st.rerun()