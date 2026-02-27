import streamlit as st
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="QuizMaster", layout="wide")

# Initialize Session State
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_question = 0
    st.session_state.game_active = False
    st.session_state.player_name = ''
    st.session_state.selected_category = None
    st.session_state.answers = []
    st.session_state.question_start_time = None

# Load questions
def load_questions():
    with open('data/questions.json', 'r') as f:
        return json.load(f)

# Main page - Home
st.title("🎯 QuizMaster")
st.write("Welcome to QuizMaster! Test your knowledge across multiple categories.")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Get Started")
    
    # Player name input
    player_name = st.text_input("Enter your name:", value=st.session_state.player_name, key="player_input")
    if player_name:
        st.session_state.player_name = player_name
    
    st.write("---")
    
    # Category selection
    st.subheader("Choose a Category")
    questions = load_questions()
    categories = list(questions.keys())
    
    for idx, category in enumerate(categories):
        col_cat1, col_cat2 = st.columns([3, 1])
        with col_cat1:
            if st.button(f"📚 {category}", key=f"cat_{idx}", use_container_width=True):
                st.session_state.selected_category = category
                st.session_state.game_active = True
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.score = 0
                st.session_state.timer_start = None
                st.switch_page("pages/_Quiz.py")
        with col_cat2:
            st.caption(f"{len(questions[category])} Q's")

with col2:
    st.subheader("📊 Stats")
    st.metric("Your Score", st.session_state.score)
    st.metric("Questions", len(questions))
    
    st.write("---")
    st.info("ℹ️ Each correct answer: +10 points")

# Show navigation to other pages
st.write("---")
st.caption("Navigate using the sidebar →")
