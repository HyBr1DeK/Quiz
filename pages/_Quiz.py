import streamlit as st
import json
import time
from datetime import datetime

st.set_page_config(page_title="Quiz Game", layout="wide")

# Custom CSS for quiz page
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a0f35 100%);
        color: #e0e7ff;
    }
    
    h1 {
        background: linear-gradient(90deg, #00d4ff, #ff006e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
    }
    
    h2 {
        color: #ff006e;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #1a3a52 0%, #2a1f55 100%) !important;
        border: 2px solid #00d4ff !important;
        color: #e0e7ff !important;
        font-weight: 600;
        border-radius: 12px !important;
        padding: 20px !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #00d4ff20 0%, #ff006e20 100%) !important;
        border-color: #ff006e !important;
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.6) !important;
        transform: translateY(-3px);
    }
    
    .stSuccess {
        background: rgba(0, 200, 100, 0.15) !important;
        border: 1px solid #00c864 !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: rgba(255, 0, 110, 0.15) !important;
        border: 1px solid #ff006e !important;
        border-radius: 10px !important;
    }
    
    .stInfo {
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid #00d4ff !important;
        border-radius: 10px !important;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #1a1f3a 0%, #2a2555 100%);
        border: 1px solid #00d4ff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00d4ff, #ff006e) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Load questions and highscores
def load_questions():
    with open('data/questions.json', 'r') as f:
        return json.load(f)

def load_highscores():
    with open('data/highscores.json', 'r') as f:
        return json.load(f)

def save_highscores(scores):
    with open('data/highscores.json', 'w') as f:
        json.dump(scores, f, indent=2)

# Check if game is active
if not st.session_state.game_active or st.session_state.selected_category is None:
    st.warning("Please select a category from the home page to start playing!")
    st.stop()

# Initialize timer state
if 'timer_start' not in st.session_state or st.session_state.timer_start is None:
    st.session_state.timer_start = time.time()
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

# Game interface
st.markdown(f"<h1 style='text-align: center;'>🎮 {st.session_state.selected_category.upper()}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-size: 1.1rem;'>👤 Player: <span style='color: #ff006e;'>{st.session_state.player_name}</span></p>", unsafe_allow_html=True)

questions = load_questions()
category_questions = questions[st.session_state.selected_category]
current_q_index = st.session_state.current_question

# Progress bar
progress = (current_q_index + 1) / len(category_questions)
st.progress(progress)
st.caption(f"Question {current_q_index + 1} of {len(category_questions)}")

if current_q_index < len(category_questions):
    question_data = category_questions[current_q_index]
    
    # Calculate remaining time
    elapsed = time.time() - st.session_state.timer_start
    remaining_time = max(0, int(30 - elapsed))
    
    # Timer and Score Display
    col_timer, col_score = st.columns([1, 1])
    with col_timer:
        # Color code the timer
        if remaining_time > 10:
            st.metric("⏱️ Time Remaining", f"{remaining_time}s", delta="", delta_color="off")
        elif remaining_time > 0:
            st.warning(f"⏱️ **{remaining_time} seconds left!**")
        else:
            st.error("⏱️ **Time's Up!**")
    with col_score:
        st.metric("📊 Current Score", f"{st.session_state.score} pts")
    
    st.write("---")
    
    # Display question
    st.subheader(f"Q: {question_data['question']}")
    
    # Check if time is up
    if remaining_time <= 0:
        st.error("⏰ Time's up! Moving to next question...")
        
        # Mark as unanswered
        st.session_state.answers.append({
            'question': question_data['question'],
            'user_answer': 'No answer (Time expired)',
            'correct_answer': question_data['correct'],
            'is_correct': False
        })
        
        # Move to next question without points
        time.sleep(2)
        st.session_state.current_question += 1
        st.session_state.timer_start = time.time()
        
        if st.session_state.current_question >= len(category_questions):
            st.session_state.game_active = False
        
        st.rerun()
    
    # Display options as buttons
    selected_answer = None
    cols = st.columns(2)
    for idx, option in enumerate(question_data['options']):
        with cols[idx % 2]:
            if st.button(option, key=f"answer_{idx}", use_container_width=True):
                selected_answer = option
                
                # Check answer and provide feedback
                is_correct = selected_answer == question_data['correct']
                
                # Store answer
                st.session_state.answers.append({
                    'question': question_data['question'],
                    'user_answer': selected_answer,
                    'correct_answer': question_data['correct'],
                    'is_correct': is_correct
                })
                
                # Update score
                if is_correct:
                    st.session_state.score += 10
                
                # Show feedback
                if is_correct:
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect! The correct answer is: **{question_data['correct']}**")
                
                st.info(f"📖 {question_data['explanation']}")
                
                # Move to next question
                time.sleep(2)
                st.session_state.current_question += 1
                st.session_state.timer_start = time.time()
                
                if st.session_state.current_question >= len(category_questions):
                    st.session_state.game_active = False
                
                st.rerun()

else:
    # Quiz finished
    st.success("🎉 Quiz Completed!")
    st.write(f"Final Score: **{st.session_state.score}/{len(category_questions) * 10}**")
    
    # Calculate percentage
    percentage = (st.session_state.score / (len(category_questions) * 10)) * 100
    st.metric("Accuracy", f"{percentage:.1f}%")
    
    # Save to highscores
    highscores = load_highscores()
    new_score = {
        'name': st.session_state.player_name,
        'category': st.session_state.selected_category,
        'score': st.session_state.score,
        'total': len(category_questions) * 10,
        'percentage': round(percentage, 1),
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    highscores.append(new_score)
    save_highscores(highscores)
    
    st.info("✅ Score saved to Highscores!")
    
    # Show answer review
    st.write("---")
    st.subheader("Answer Review")
    for idx, answer in enumerate(st.session_state.answers):
        with st.expander(f"Q{idx+1}: {answer['question']}"):
            if answer['is_correct']:
                st.success(f"✅ Your answer: {answer['user_answer']}")
            else:
                st.error(f"❌ Your answer: {answer['user_answer']}")
                st.info(f"Correct answer: {answer['correct_answer']}")
    
    # Reset game for new round
    if st.button("Play Again", use_container_width=True):
        st.session_state.game_active = False
        st.session_state.selected_category = None
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.rerun()
