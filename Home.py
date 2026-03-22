import streamlit as st
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="QuizMaster", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Hello Kitty design
st.markdown("""
    <style>
    /* Hello Kitty Color Palette */
    :root {
        --pink: #ff69b4;
        --light-pink: #ffc0cb;
        --pastel-pink: #ffb6d9;
        --purple: #e6b3ff;
        --light-purple: #f0e6ff;
        --light-blue: #b3e5fc;
        --white: #fffaf0;
        --accent: #ff1493;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #fffaf0 0%, #fff5e6 50%, #ffe6f0 100%);
        color: #d946a6;
    }
    
    /* Title styling - Hello Kitty style */
    h1 {
        color: #ff69b4;
        font-weight: 900;
        font-size: 3.5rem !important;
        text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.2);
        margin-bottom: 0.5rem;
        font-family: 'Arial', sans-serif;
    }
    
    /* Subheadings */
    h2, h3 {
        color: #ff69b4;
        font-weight: 700;
        font-family: 'Arial', sans-serif;
    }
    
    /* Category button styling */
    .category-btn {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%) !important;
        border: 3px solid #ffb6d9 !important;
        color: #d946a6 !important;
        padding: 20px !important;
        border-radius: 25px !important;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.2);
    }
    
    .category-btn:hover {
        background: linear-gradient(135deg, #ffc0cb 0%, #ffb6d9 100%) !important;
        border-color: #ff69b4 !important;
        box-shadow: 0 8px 20px rgba(255, 105, 180, 0.4) !important;
        transform: translateY(-3px);
    }
    
    /* Input styling */
    input[type="text"] {
        background-color: #ffffff !important;
        border: 2px solid #ffb6d9 !important;
        color: #d946a6 !important;
        border-radius: 20px !important;
        padding: 12px 15px !important;
        font-family: 'Arial', sans-serif;
    }
    
    input[type="text"]:focus {
        border-color: #ff69b4 !important;
        box-shadow: 0 0 15px rgba(255, 105, 180, 0.3) !important;
    }
    
    /* General text */
    p {
        color: #d946a6;
        font-family: 'Arial', sans-serif;
    }
    
    /* Divider */
    hr {
        border-color: #ffb6d9;
        opacity: 0.5;
    }
    
    /* Info box */
    .stInfo {
        background: rgba(255, 192, 203, 0.3) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 20px !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%) !important;
        border: 2px solid #ffb6d9 !important;
        color: #ff69b4 !important;
        border-radius: 20px !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #ffc0cb 0%, #ffb6d9 100%) !important;
        border-color: #ff69b4 !important;
        box-shadow: 0 6px 18px rgba(255, 105, 180, 0.3) !important;
    }
    
    /* Metric box */
    .stMetric {
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        border: 2px solid #ffb6d9;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

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

# Header with Hello Kitty design
col_title1, col_title2 = st.columns([3, 1])
with col_title1:
    st.title("🎀 QUIZMASTER 🎀")
    st.write("<p style='font-size: 1.2rem; color: #ff69b4;'>✨ Master Your Knowledge with Cuteness! ✨</p>", unsafe_allow_html=True)

with col_title2:
    st.empty()

st.markdown("<hr style='border-color: #ffb6d9; opacity: 0.5;'>", unsafe_allow_html=True)

# Hello Kitty Images Section
st.markdown("<h3 style='text-align: center; color: #ff69b4; margin: 1.5rem 0;'>🎀 Hello Piggy says Servus 🎀</h3>", unsafe_allow_html=True)

hk_col1, hk_col2, hk_col3 = st.columns([1, 2, 1])

# Empty left column
with hk_col1:
    st.empty()

# Center - Hello Kitty image
with hk_col2:
    try:
        st.image("assets/hello_kitty.svg", use_column_width=True)
    except:
        st.markdown("<p style='text-align: center; color: #ff69b4; font-size: 3rem;'>🎀</p>", unsafe_allow_html=True)

# Empty right column
with hk_col3:
    st.empty()

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1.2])

with col1:
    st.markdown("<h2 style='color: #ff69b4;'>💖 Get Started</h2>", unsafe_allow_html=True)
    
    # Player name input
    player_name = st.text_input("👤 Enter your name:", value=st.session_state.player_name, key="player_input", placeholder="Your cute name here 💕")
    if player_name:
        st.session_state.player_name = player_name
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Category selection
    st.markdown("<h3 style='color: #ff69b4;'>🎮 Choose Your Challenge</h3>", unsafe_allow_html=True)
    questions = load_questions()
    categories = list(questions.keys())
    
    for idx, category in enumerate(categories):
        # Get emoji based on category
        emoji_map = {
            "Witcher 3: The Wild Hunt": "🧙",
            "Cyberpunk 2077": "🤖",
            "Red Dead Redemption 1": "🤠",
            "Red Dead Redemption 2": "🤠",
            "Dying Light 1-3": "🧟"
        }
        emoji = emoji_map.get(category, "🎮")
        
        col_cat1, col_cat2 = st.columns([3.5, 0.7])
        with col_cat1:
            if st.button(f"{emoji} {category}", key=f"cat_{idx}", use_container_width=True, help=f"Test your knowledge with {len(questions[category])} {category} questions!"):
                st.session_state.selected_category = category
                st.session_state.game_active = True
                st.session_state.quiz_completed = False
                st.session_state.score_saved = False
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.score = 0
                st.session_state.timer_start = None
                st.switch_page("pages/03_Quiz.py")
        with col_cat2:
            st.markdown(f"<div style='text-align: center; padding: 8px; background: linear-gradient(135deg, #ffc0cb 0%, #ffb6d9 100%); border-radius: 15px; border: 2px solid #ffb6d9;'><span style='color: #ff69b4; font-weight: bold;'>{len(questions[category])}</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<h2 style='color: #ff69b4; text-align: center;'>💕 STATS</h2>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%); border: 2px solid #ffb6d9; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #ff69b4; margin: 0;'>💎 {st.session_state.score}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ff69b4; margin: 5px 0 0 0; font-size: 0.9rem;'>YOUR SCORE</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: linear-gradient(135deg, #ffe6f0 0%, #fff0f5 100%); border: 2px solid #ffb6d9; border-radius: 20px; padding: 20px; text-align: center; box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #ff69b4; margin: 0;'>🎯 {sum(len(q) for q in questions.values())}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ff69b4; margin: 5px 0 0 0; font-size: 0.9rem;'>QUESTIONS</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: linear-gradient(135deg, #ffcceb 0%, #fff0f5 100%); border: 2px solid #ffb6d9; border-radius: 20px; padding: 15px; text-align: center; box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ff69b4; margin: 0; font-size: 0.85rem;'>💖 +10 points per correct answer</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border-color: #ffb6d9; opacity: 0.5; margin-top: 3rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ff69b4; font-size: 0.9rem;'>← Navigate using the sidebar for Categories, Highscores, and more! 🎀</p>", unsafe_allow_html=True)
