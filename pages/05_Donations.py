import streamlit as st

st.set_page_config(page_title="Donations", layout="wide")

# Custom CSS styling - match dark/pink quiz theme
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

    .donation-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.03) 100%);
        border: 2px solid rgba(255, 182, 217, 0.7);
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 8px 24px rgba(255, 105, 180, 0.18);
        color: #ffd6ec;
        font-size: 1.08rem;
        line-height: 1.75;
        margin-top: 0.75rem;
    }

    .pink {
        color: #ff69b4;
        font-weight: 800;
    }

    .contact-badge {
        display: inline-block;
        margin-top: 1rem;
        background: linear-gradient(135deg, #ffffff 0%, #fff0f5 100%);
        color: #ff4fa8;
        border: 1.5px solid #ffb6d9;
        border-radius: 999px;
        padding: 10px 16px;
        font-size: 1rem;
        font-weight: 800;
    }

    .subtle {
        color: #ffc8e7;
        opacity: 0.95;
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>💖 DONATIONS 🎀</h1>", unsafe_allow_html=True)

left, right = st.columns([1.4, 1], gap="large")

with left:
    st.markdown(
        """
        <div class="donation-card">
        Since we are all human and money makes the world go around, I am asking for a little support for the
        <span class="pink">starving developer</span> of this masterpiece.<br><br>

        He spent his last dime on utility bills and cannot even afford a cup of coffee.<br><br>

        For those who care: I would give you my bank details, but I did not even have enough money to open an account!<br>
        So, it is either cash in person or via phone number:

        <div class="contact-badge">📱 +49 1577 0882213</div>

        <p class="subtle">Thank you for your support and for playing the quiz. 💕</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    try:
        st.image("assets/hello_kitty.svg", use_container_width=True)
    except Exception:
        st.markdown("<p style='text-align:center; font-size: 4rem; color:#ff69b4;'>🎀</p>", unsafe_allow_html=True)

st.caption("Support keeps updates coming: more games, more questions, and better features.")
