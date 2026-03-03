import streamlit as st
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(page_title="QuizMaster", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for modern gaming design
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #00d4ff;
        --secondary: #ff006e;
        --dark-bg: #0a0e27;
        --card-bg: #1a1f3a;
        --text-light: #e0e7ff;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a0f35 100%);
        color: #e0e7ff;
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(90deg, #00d4ff, #ff006e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        font-size: 3.5rem !important;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        margin-bottom: 0.5rem;
    }
    
    /* Subheadings */
    h2, h3 {
        color: #00d4ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }
    
    /* Category button styling */
    .category-btn {
        background: linear-gradient(135deg, #1a1f3a 0%, #2a2555 100%) !important;
        border: 2px solid #00d4ff !important;
        color: #e0e7ff !important;
        padding: 20px !important;
        border-radius: 15px !important;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    .category-btn:hover {
        background: linear-gradient(135deg, #00d4ff15 0%, #ff006e15 100%) !important;
        border-color: #ff006e !important;
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.5) !important;
        transform: translateY(-2px);
    }
    
    /* Stat cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #2a2555 100%);
        border: 1px solid #00d4ff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
    }
    
    /* Input styling */
    input[type="text"] {
        background-color: #1a1f3a !important;
        border: 2px solid #00d4ff !important;
        color: #e0e7ff !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    input[type="text"]:focus {
        border-color: #ff006e !important;
        box-shadow: 0 0 10px rgba(255, 0, 110, 0.3) !important;
    }
    
    /* General text */
    p {
        color: #e0e7ff;
    }
    
    /* Divider */
    hr {
        border-color: #00d4ff;
        opacity: 0.3;
    }
    
    /* Info box */
    .stInfo {
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid #00d4ff !important;
        border-radius: 10px !important;
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

# Header with custom design
col_title1, col_title2 = st.columns([3, 1])
with col_title1:
    st.title("🎮 QUIZMASTER")
    st.write("<p style='font-size: 1.2rem; color: #00d4ff;'>Master Your Knowledge. Conquer Each Challenge.</p>", unsafe_allow_html=True)

with col_title2:
    st.empty()

st.markdown("<hr style='border-color: #00d4ff; opacity: 0.3;'>", unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1.2])

with col1:
    st.markdown("<h2 style='color: #00d4ff;'>⚡ Get Started</h2>", unsafe_allow_html=True)
    
    # Player name input
    player_name = st.text_input("👤 Enter your name:", value=st.session_state.player_name, key="player_input", placeholder="Enter your gamer tag...")
    if player_name:
        st.session_state.player_name = player_name
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Category selection
    st.markdown("<h3 style='color: #ff006e; margin-top: 2rem;'>🎯 Choose Your Battle</h3>", unsafe_allow_html=True)
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
            if st.button(f"{emoji} {category}", key=f"cat_{idx}", use_container_width=True, help=f"Test your knowledge with 20 {category} questions!"):
                st.session_state.selected_category = category
                st.session_state.game_active = True
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.score = 0
                st.session_state.timer_start = None
                st.switch_page("pages/_Quiz.py")
        with col_cat2:
            st.markdown(f"<div style='text-align: center; padding: 8px; background: rgba(0, 212, 255, 0.1); border-radius: 8px; border: 1px solid #00d4ff;'><span style='color: #00d4ff; font-weight: bold;'>{len(questions[category])}</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<h2 style='color: #00d4ff; text-align: center;'>📊 STATS</h2>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; border-radius: 12px; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #ff006e; margin: 0;'>{st.session_state.score}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00d4ff; margin: 5px 0 0 0; font-size: 0.9rem;'>YOUR SCORE</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: rgba(255, 0, 110, 0.1); border: 1px solid #ff006e; border-radius: 12px; padding: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #00d4ff; margin: 0;'>{sum(len(q) for q in questions.values())}</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #ff006e; margin: 5px 0 0 0; font-size: 0.9rem;'>TOTAL QUESTIONS</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<div style='background: rgba(0, 212, 255, 0.1); border: 1px solid #00d4ff; border-radius: 12px; padding: 15px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00d4ff; margin: 0; font-size: 0.85rem;'>⭐ +10 points per correct answer</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border-color: #00d4ff; opacity: 0.3; margin-top: 3rem;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00d4ff; font-size: 0.9rem;'>← Navigate using the sidebar for Categories, Highscores, and Quiz info</p>", unsafe_allow_html=True)
