import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Highscores", layout="wide")

st.title("🏆 Highscores")

def load_highscores():
    with open('data/highscores.json', 'r') as f:
        return json.load(f)

highscores = load_highscores()

if not highscores:
    st.info("No scores yet! Play a quiz to get on the leaderboard.")
else:
    # Sort by score descending and take top 10
    sorted_scores = sorted(highscores, key=lambda x: x['score'], reverse=True)[:10]
    
    st.subheader("Top 10 Players")
    
    # Display as table
    df = pd.DataFrame(sorted_scores)
    df['Rank'] = range(1, len(df) + 1)
    df = df[['Rank', 'name', 'category', 'score', 'total', 'percentage', 'date']]
    df.columns = ['🥇', 'Player', 'Category', 'Score', 'Total', 'Accuracy %', 'Date']
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Category breakdown
    st.write("---")
    st.subheader("Top Scores by Category")
    
    categories = df['Category'].unique()
    cols = st.columns(len(categories))
    
    for idx, category in enumerate(categories):
        with cols[idx]:
            category_scores = sorted_scores[df['Category'] == category]
            if category_scores:
                top_score = category_scores[0]
                st.metric(
                    category,
                    f"{top_score['score']}/{top_score['total']}",
                    f"{top_score['percentage']}% - {top_score['name']}"
                )
    
    # Personal stats
    st.write("---")
    st.subheader("📊 Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Games Played", len(highscores))
    
    with col2:
        avg_score = sum(s['score'] for s in highscores) / len(highscores)
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col3:
        avg_accuracy = sum(s['percentage'] for s in highscores) / len(highscores)
        st.metric("Average Accuracy", f"{avg_accuracy:.1f}%")
    
    with col4:
        max_score = max(s['score'] for s in highscores)
        st.metric("Best Score", max_score)
