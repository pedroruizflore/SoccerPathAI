import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SoccerPath AI", page_icon="⚽")

st.title("⚽ SoccerPath AI - Athlete Dashboard")
st.subheader("Performance Tracking for Pedro Henrique (Tabor College)")

# Sidebar for adding new match stats
st.sidebar.header("Add Match Statistics")
goals = st.sidebar.number_input("Goals", min_value=0, step=1)
assists = st.sidebar.number_input("Assists", min_value=0, step=1)
interceptions = st.sidebar.number_input("Interceptions", min_value=0, step=1)

if st.sidebar.button("Save Match & Get Feedback"):
    url = f"http://127.0.0.1:8001/add-match?goals={goals}&assists={assists}&interceptions={interceptions}"
    response = requests.post(url)
    if response.status_code == 200:
        st.sidebar.success("Match Saved!")
        st.info(f"📋 **Coach AI Feedback:** {response.json()['coach_feedback']}")
    else:
        st.sidebar.error("Error saving match.")

# Main area: Performance History
st.write("### Your Season Progress")
history_response = requests.get("http://127.0.0.1:8001/my-performance")

if history_response.status_code == 200:
    data = history_response.json()["stats_history"]
    if data:
        df = pd.DataFrame(data)
        st.line_chart(df.set_index("date")[["goals", "assists"]])
        st.table(df)
    else:
        st.write("No matches recorded yet. Add one in the sidebar!")