import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Categories", layout="wide")

# Custom CSS styling - Hello Kitty
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #fffaf0 0%, #fff5e6 50%, #ffe6f0 100%);
        color: #d946a6;
    }
    
    h1 {
        color: #ff69b4;
        font-weight: 900;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.2);
    }
    
    h2, h3 {
        color: #ff69b4;
        font-weight: 700;
    }
    
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
    
    .stMetric {
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        border: 2px solid #ffb6d9;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
        color: #ff69b4 !important;           /* pink text instead of black */
    }
    .stMetric * {
        color: #ff69b4 !important;
    }

    .stDataFrame {
        background: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
    }

    .stExpander {
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        color: #ff69b4 !important;               /* expander header text pink */
    }
    .stExpander * {
        color: #ff69b4 !important;               /* expander inner content pink */
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎀 CATEGORIES OVERVIEW 🎀</h1>", unsafe_allow_html=True)

def load_questions():
    with open('data/questions.json', 'r') as f:
        return json.load(f)

questions = load_questions()

# Display categories with question count
st.subheader("Available Categories")

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for idx, (category, q_list) in enumerate(questions.items()):
    with cols[idx % 3]:
        st.markdown(f"### 📖 {category}")
        st.markdown(f"**Questions:** {len(q_list)}")
        
        # Show difficulty estimate based on question count
        difficulty = "Easy" if len(q_list) < 5 else "Medium" if len(q_list) < 8 else "Hard"
        st.caption(f"Difficulty: {difficulty}")
        
        if st.button(f"Play {category}", key=f"play_{category}", use_container_width=True):
            st.session_state.selected_category = category
            st.session_state.game_active = True
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.score = 0
            # navigate to quiz page; must match what Home.py does so the
            # proper script runs.
            try:
                st.switch_page("pages/03_Quiz.py")
            except Exception:
                # older Streamlit versions may not support switch_page,
                # fallback to rerun which keeps the user on the same page –
                # they'll have to click quiz in sidebar manually.
                st.rerun()

# Detailed category breakdown
st.write("---")
st.subheader("📊 Category Details")

# Create table
category_data = []
for category, q_list in questions.items():
    category_data.append({
        'Category': category,
        'Number of Questions': len(q_list),
        'Max Score': len(q_list) * 10
    })

df = pd.DataFrame(category_data)
st.dataframe(df, use_container_width=True, hide_index=True)

# Show sample questions
st.write("---")
st.subheader("📝 Sample Questions")

for category, q_list in questions.items():
    with st.expander(f"**{category}** - Sample Questions ({len(q_list)} total)"):
        for idx, question in enumerate(q_list[:3], 1):
            st.write(f"{idx}. {question['question']}")
            st.caption(f"Options: {', '.join(question['options'])}")
        
        if len(q_list) > 3:
            st.caption(f"... and {len(q_list) - 3} more questions")

# Statistics
st.write("---")
st.subheader("📈 Overall Statistics")

total_questions = sum(len(q) for q in questions.values())
avg_per_category = total_questions / len(questions)
max_questions = max(len(q) for q in questions.values())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Categories", len(questions))

with col2:
    st.metric("Total Questions", total_questions)

with col3:
    st.metric("Average per Category", f"{avg_per_category:.1f}")

with col4:
    st.metric("Max Score Possible", total_questions * 10)
