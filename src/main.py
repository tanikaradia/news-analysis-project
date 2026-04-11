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

news = fetch_news()

for article in news:
    key = article["title"]

    # ---- Initialize states ----
    if key + "_done" not in st.session_state:
        st.session_state[key + "_done"] = False

    if key + "_edit" not in st.session_state:
        st.session_state[key + "_edit"] = False

    done = st.session_state[key + "_done"]
    edit = st.session_state[key + "_edit"]

    # st.write("DEBUG:", key, done, edit)

    # ---- Display Article ----
    st.subheader(article["title"])
    st.write("Sentiment:", article["sentiment"])
    st.write("Category:", article["category"])

    # ---- If NOT submitted ----
    if not done and not edit:
        col1, col2 = st.columns(2) #split screen to 2

        # 👍 Correct
        if col1.button("👍 Correct", key=key + "c"): # key: Maintain state
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
            st.rerun() #fresh run with new state: refresh instantly, no 2x click🌟

        # 👎 Wrong
        if col2.button("👎 Wrong", key=key + "_wrong"):
            # st.write("Wrong button clicked")   # DEBUG
            st.session_state[key + "_edit"] = True
            st.rerun()

    # ---- If user clicked WRONG → show correction UI ----
    if edit and not done:
        st.write("### Correct the values:") # markdown

        new_sentiment = st.selectbox(
            "Correct Sentiment",
            ["Positive", "Neutral", "Negative"],
            key=key + "_sent"
        )

        new_category = st.selectbox(
            "Correct Category",
            ["General", "Politics", "Sports", "Technology", "Business", "Crime"],
            key=key + "_cat"
        )

        if st.button("Submit Correction", key=article["title"] + "_submit"): 
            save_feedback({
                "title": article["title"],
                "predicted_sentiment": article["sentiment"],
                "predicted_category": article["category"],
                "user_sentiment": new_sentiment,
                "user_category": new_category,
                "feedback": "wrong"
            })

            st.success("Correction saved ✅")

            # Reset states
            st.session_state[key + "_done"] = True
            st.session_state[key + "_edit"] = False
            st.rerun()

    # ---- If already submitted ----
    if done:
        st.info("Already submitted ✅")

    st.markdown("---")