import streamlit as st
import json
import time
from datetime import datetime

st.set_page_config(page_title="Quiz Game", layout="wide")

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

# Game interface
st.title(f"🎮 {st.session_state.selected_category} Quiz")
st.write(f"Player: **{st.session_state.player_name}**")

questions = load_questions()
category_questions = questions[st.session_state.selected_category]
current_q_index = st.session_state.current_question

# Progress bar
progress = (current_q_index + 1) / len(category_questions)
st.progress(progress)
st.caption(f"Question {current_q_index + 1} of {len(category_questions)}")

if current_q_index < len(category_questions):
    question_data = category_questions[current_q_index]
    
    # Timer (Optional Bonus)
    col_timer, col_score = st.columns([1, 1])
    with col_timer:
        st.metric("⏱️ Time", "30 sec (bonus feature)")
    with col_score:
        st.metric("📊 Current Score", f"{st.session_state.score} pts")
    
    st.write("---")
    
    # Display question
    st.subheader(f"Q: {question_data['question']}")
    
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
