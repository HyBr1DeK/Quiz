import streamlit as st
import json
import time
from datetime import datetime

st.set_page_config(page_title="Quiz Game", layout="wide")

# Custom CSS for quiz page - Hello Kitty
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #fffaf0 0%, #fff5e6 50%, #ffe6f0 100%);
        color: #d946a6;
    }
    
    h1 {
        color: #ff69b4;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.2);
    }
    
    h2 {
        color: #ff69b4;
        font-weight: 700;
        margin-top: 1.5rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%) !important;
        border: 2px solid #ffb6d9 !important;
        color: #ff69b4 !important;
        font-weight: 600;
        border-radius: 20px !important;
        padding: 20px !important;
        font-size: 1.1rem !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
    }
    
    /* Hover stays close to default to avoid fake "second selected" look. */
    .stButton>button:hover {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%) !important;
        border-color: #ffb6d9 !important;
        transform: none;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15) !important;
    }

    /* Clicked/focused option gets the selected highlight only. */
    .stButton>button:focus,
    .stButton>button:focus-visible,
    .stButton>button:active {
        background: linear-gradient(135deg, #ffe6f3 0%, #ffd1ea 100%) !important;
        border-color: #ff69b4 !important;
        color: #ff69b4 !important;
        box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.35), 0 8px 20px rgba(255, 105, 180, 0.25) !important;
        outline: none !important;
    }
    
    .stSuccess {
        background: rgba(192, 255, 192, 0.2) !important;
        border: 2px solid #90ee90 !important;
        border-radius: 15px !important;
    }
    
    .stError {
        background: rgba(255, 192, 203, 0.2) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
    }
    
    .stInfo {
        background: rgba(255, 192, 203, 0.15) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
    }
    
    .stMetric {
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        border: 2px solid #ffb6d9;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
        color: #ff69b4 !important;               /* pink text instead of black */
    }
    /* make sure any text inside metrics keeps the pink color */
    .stMetric * {
        color: #ff69b4 !important;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff69b4, #ffc0cb) !important;
    }
    
    .stWarning {
        background: rgba(255, 192, 203, 0.2) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
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

# Track completion/save state to avoid missing or duplicate leaderboard entries.
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'score_saved' not in st.session_state:
    st.session_state.score_saved = False

# Check if game is active
if ((not st.session_state.get('game_active', False)) or (st.session_state.get('selected_category') is None)) and (not st.session_state.get('quiz_completed', False)):
    questions = load_questions()
    total_questions = sum(len(q) for q in questions.values())
    total_categories = len(questions)

    st.markdown("<h1 style='text-align: center; color: #ff69b4;'>🎮 QUIZ INFORMATION 🎀</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Categories", total_categories)
    with col2:
        st.metric("Total Questions", total_questions)
    with col3:
        st.metric("Points per Correct Answer", "10")

    st.write("---")
    st.subheader("How Quiz Mode Works")
    st.markdown("- Each question has a 30-second timer.")
    st.markdown("- If time runs out, the answer is marked wrong and gives 0 points.")
    st.markdown("- One answer per question. Only your selected answer is highlighted.")
    st.markdown("- Final score is saved automatically to Highscores.")

    st.write("---")
    st.subheader("Available Quiz Categories")
    detail_cols = st.columns(2)
    for idx, (category, q_list) in enumerate(questions.items()):
        with detail_cols[idx % 2]:
            st.markdown(f"**📚 {category}**")
            st.caption(f"Questions: {len(q_list)} | Max Score: {len(q_list) * 10}")

    st.stop()

# Initialize timer state
if 'timer_start' not in st.session_state or st.session_state.timer_start is None:
    st.session_state.timer_start = time.time()
# make sure we always have a current question counter (older versions used
# "question_index" which is now deprecated).  This guards against cases
# where the user somehow lands on the quiz page without the state having
# been set by the categories/home page.
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Game interface
st.markdown(f"<h1 style='text-align: center; color: #ff69b4;'>🎀 {st.session_state.selected_category.upper()} 🎀</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #ff69b4; font-size: 1.1rem;'>👤 Player: <span style='color: #ff1493;'>{st.session_state.player_name}</span> 💕</p>", unsafe_allow_html=True)

questions = load_questions()
# ensure the selected category exists in the data (user could have
# manipulated session state or the data file changed)
if st.session_state.selected_category not in questions:
    # the error message was split across lines which produced a syntax
    # error; keep it on one line or use triple quotes
    st.error("🚫 The selected category was not found – please go back and choose a different one.")
    st.stop()
category_questions = questions[st.session_state.selected_category]
current_q_index = st.session_state.current_question

# Progress bar
total_questions = len(category_questions)
if total_questions == 0:
    st.error("🚫 This category has no questions configured.")
    st.stop()

# Streamlit progress accepts only values in [0.0, 1.0].
display_q_index = min(current_q_index, total_questions)
progress = display_q_index / total_questions
st.progress(progress)
st.caption(f"Question {display_q_index} of {total_questions}")

# create placeholders so that any previous feedback/explanation is
# explicitly cleared each time we render a new question.  using
# containers prevents stray messages from the prior run from lingering.
feedback_ph = st.empty()
explanation_ph = st.empty()

# ensure we have a flag to indicate whether an answer click is currently
# being handled; this prevents the automatic timer refresh from
# interrupting while we're waiting to show feedback.
if 'answer_in_progress' not in st.session_state:
    st.session_state.answer_in_progress = False

if current_q_index < total_questions:
    question_data = category_questions[current_q_index]
    
    # Calculate remaining time
    elapsed = time.time() - st.session_state.timer_start
    remaining_time = max(0, int(30 - elapsed))
    # We intentionally delay rerunning until *after* the UI is rendered
    # below; the previous placement caused the page to refresh repeatedly
    # before ever drawing the question or timer, leaving the user staring
    # at an empty screen until the countdown reached zero.
    
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
    
    # Display question (fall back gracefully if the question text is
    # unexpectedly missing).  It was reported that sometimes the user "did
    # not see a question" – this guard helps make the problem evident and
    # avoids rendering an empty header.
    question_text = question_data.get('question', '').strip()
    if not question_text:
        st.warning("⚠️ Question text is missing for this entry. Please review your data file or choose another category.")
    else:
        st.subheader(f"Q: {question_text}")
    
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
        
        if st.session_state.current_question >= total_questions:
            st.session_state.game_active = False
            st.session_state.quiz_completed = True
        
        st.rerun()
    
    # Use a single-choice selector to guarantee that only one answer can
    # be highlighted/selected at any time.
    selected_answer = st.radio(
        "Pick one answer:",
        question_data['options'],
        key=f"answer_choice_{current_q_index}",
        index=None
    )

    if st.button("Submit Answer", key=f"submit_answer_{current_q_index}", use_container_width=True):
        if selected_answer is None:
            st.warning("Please select an answer first.")
            st.stop()

        # start processing; stop timer-based reruns
        st.session_state.answer_in_progress = True

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
            feedback_ph.success("✅ Correct!")
        else:
            feedback_ph.error(f"❌ Incorrect! The correct answer is: **{question_data['correct']}**")

        explanation_ph.info(f"📖 {question_data['explanation']}")

        # give user a moment to read; extended per request
        time.sleep(5)
        # clear the placeholders before moving on so the next run
        # doesn’t inadvertently show them
        feedback_ph.empty()
        explanation_ph.empty()
        st.session_state.answer_in_progress = False

        # Move to next question
        st.session_state.current_question += 1
        st.session_state.timer_start = time.time()

        if st.session_state.current_question >= total_questions:
            st.session_state.game_active = False
            st.session_state.quiz_completed = True

        st.rerun()

else:
    # Quiz finished
    st.success("🎉 Quiz Completed!")
    st.write(f"Final Score: **{st.session_state.score}/{total_questions * 10}**")
    
    # Calculate percentage
    percentage = (st.session_state.score / (total_questions * 10)) * 100
    st.metric("Accuracy", f"{percentage:.1f}%")
    
    # Save to highscores once.
    if not st.session_state.score_saved:
        highscores = load_highscores()
        new_score = {
            'name': st.session_state.player_name,
            'category': st.session_state.selected_category,
            'score': st.session_state.score,
            'total': total_questions * 10,
            'percentage': round(percentage, 1),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        highscores.append(new_score)
        save_highscores(highscores)
        st.session_state.score_saved = True
        st.info("✅ Score saved to Highscores!")
    else:
        st.info("✅ This score is already saved in Highscores.")
    
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
        st.session_state.quiz_completed = False
        st.session_state.score_saved = False
        st.session_state.selected_category = None
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.rerun()

# At the very end of the question-handling block we schedule an
# automatic page refresh every second while the timer is still running.
# Placing it here ensures the question and timer are visible before the
# rerun occurs.  We also skip the refresh if an answer is currently being
# processed; otherwise a background rerun might collide with the 2‑second
# feedback pause and leave stale messages around.
if current_q_index < total_questions:
    # only rerun when there is still time remaining and we're not waiting
    # on feedback from a just‑clicked option.
    if remaining_time > 0 and not st.session_state.answer_in_progress:
        time.sleep(1)
        st.rerun()
