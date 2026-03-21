import streamlit as st

st.set_page_config(page_title="Upcoming Quizzes", layout="wide")

# Custom CSS styling - match current dark/pink quiz theme
st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle at 20% 10%, #141b33 0%, #090d1f 40%, #050815 100%);
        color: #ffd6ec;
    }

    h1 {
        color: #ff69b4;
        font-weight: 900;
        font-size: 3rem !important;
        text-shadow: 0 0 18px rgba(255, 105, 180, 0.35);
        text-align: center;
    }

    .upcoming-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%);
        border: 2px solid rgba(255, 182, 217, 0.7);
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(255, 105, 180, 0.18);
        color: #ffd6ec;
        margin-top: 0.75rem;
    }

    .quiz-item {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        border: 2px solid #ffb6d9;
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 12px;
        color: #ff4fa8;
        font-weight: 700;
        line-height: 1.6;
    }

    .subtext {
        color: #ffc8e7;
        font-weight: 500;
    }

    .pink {
        color: #ff69b4;
        font-weight: 800;
    }

    .tip {
        color: #ffd6ec;
        font-size: 0.98rem;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🗓️ UPCOMING QUIZZES 🎀</h1>", unsafe_allow_html=True)

left, right = st.columns([1.4, 1], gap="large")

with left:
    st.markdown("<div class='upcoming-card'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="quiz-item">
            🎮 The Witcher 3: Adding the new DLC<br>
            <span class="subtext">Release date: Unknown</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="quiz-item">
            ⚔️ The Witcher 4<br>
            <span class="subtext">Release date: Also unknown</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="quiz-item">
            🧟 Resident Evil Requiem<br>
            <span class="subtext">Now raising funds to actually buy the game - it is 70 EUR.</span><br>
            <span class="subtext">You can find payment details in the <span class="pink">Donations</span> tab.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    try:
        st.image("assets/hello_kitty.svg", use_container_width=True)
    except Exception:
        st.markdown("<p style='text-align:center; font-size: 4rem; color:#ff69b4;'>🎀</p>", unsafe_allow_html=True)

st.markdown("<p class='tip'>💖 More quizzes are coming soon. Thank you for supporting development!</p>", unsafe_allow_html=True)
