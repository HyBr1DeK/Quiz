import streamlit as st

st.set_page_config(page_title="Information", layout="wide")

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

    .info-card {
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        border: 2px solid #ffb6d9;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(255, 105, 180, 0.15);
        color: #d946a6;
        font-size: 1.1rem;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>ℹ️ INFORMATION 🎀</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-card">
    Hello fellows! This multi-game quiz application was developed by a Georgian creator under the pseudonym
    <b>Red_Tr1ssMerigold</b>.<br><br>
    Whether you are a casual player or a pro, you can find a quiz here to test your gaming knowledge.<br><br>
    Good luck and enjoy your time!
    </div>
    """,
    unsafe_allow_html=True
)
