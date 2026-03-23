import streamlit as st

st.set_page_config(page_title="Information", layout="wide")

# Custom CSS styling - match current dark/pink quiz theme
st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle at 20% 10%, #141b33 0%, #090d1f 40%, #050815 100%);
        color: #ff69b4;
    }

    h1 {
        color: #ff69b4;
        font-weight: 900;
        font-size: 3rem !important;
        text-shadow: 0 0 18px rgba(255, 105, 180, 0.35);
    }

    .info-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%);
        border: 2px solid rgba(255, 182, 217, 0.7);
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 8px 24px rgba(255, 105, 180, 0.18);
        color: #ff69b4;
        font-size: 1.1rem;
        line-height: 1.7;
        margin-top: 0.5rem;
    }

    .pink {
        color: #ff69b4;
        font-weight: 700;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 1rem;
    }

    .badge {
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        color: #ff4fa8;
        border: 1.5px solid #ffb6d9;
        border-radius: 999px;
        padding: 7px 14px;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .hello-wrap {
        border: 2px solid rgba(255, 182, 217, 0.75);
        border-radius: 24px;
        padding: 12px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        box-shadow: 0 8px 22px rgba(255, 105, 180, 0.2);
        color: #ff69b4;
    }
    
    .hello-wrap * {
        color: #ff69b4 !important;
    }
    
    /* Sidebar navigation styling - keep pink on all states */
    .stSidebar [data-testid="stSidebarNav"] a {
        color: #ff69b4 !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] a:hover {
        color: #ff69b4 !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] a:active {
        color: #ff69b4 !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] a:visited {
        color: #ff69b4 !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] a:focus {
        color: #ff69b4 !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] [aria-selected="true"] {
        color: #ff69b4 !important;
        background: rgba(255, 105, 180, 0.15) !important;
    }
    
    .stSidebar [data-testid="stSidebarNav"] [aria-selected="true"] * {
        color: #ff69b4 !important;
    }
    
    .stSidebar a {
        color: #ff69b4 !important;
    }
    
    .stSidebar a:hover,
    .stSidebar a:active,
    .stSidebar a:visited,
    .stSidebar a:focus {
        color: #ff69b4 !important;
    }
    
    .stSidebar [role="button"][aria-selected="true"] {
        background: rgba(255, 105, 180, 0.2) !important;
        color: #ff69b4 !important;
    }
    
    .stSidebar [role="button"][aria-selected="true"] * {
        color: #ff69b4 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>ℹ️ INFORMATION 🎀</h1>", unsafe_allow_html=True)

left, right = st.columns([1.35, 1], gap="large")

with left:
    st.markdown(
        """
        <div class="info-card">
        Hello fellows! This multi-game quiz application was developed by a Georgian creator under the pseudonym
        <span class="pink">Red_Tr1ssMerigold</span>.<br><br>
        Whether you are a casual player or a pro, you can find a quiz here to test your gaming knowledge.<br><br>
        Good luck and enjoy your time!<br><br>
        <div class="badge-row">
            <span class="badge">🎮 Multi-Game Trivia</span>
            <span class="badge">⏱️ 30s Per Question</span>
            <span class="badge">🏆 Highscore Tracking</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    st.markdown("<div class='hello-wrap'>", unsafe_allow_html=True)
    try:
        st.image("assets/hello_kitty.svg", use_container_width=True)
    except Exception:
        st.markdown("<p style='text-align:center; font-size: 4rem; color:#ff69b4;'>🎀</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("💖 Keep playing, climb the leaderboard, and have fun!")
