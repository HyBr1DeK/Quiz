import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Highscores", layout="wide")

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
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
    }
    
    .stInfo {
        background: rgba(255, 192, 203, 0.2) !important;
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
    }
    
    .stExpander {
        border: 2px solid #ffb6d9 !important;
        border-radius: 15px !important;
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
    }

    .podium-card {
        text-align: center;
        border-radius: 18px;
        border: 2px solid #ffb6d9;
        padding: 16px 14px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
        box-shadow: 0 6px 18px rgba(255, 105, 180, 0.18);
    }

    .podium-rank {
        font-size: 1.2rem;
        font-weight: 800;
        color: #ff1493;
        margin-bottom: 6px;
    }

    .podium-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #d946a6;
    }

    .podium-score {
        font-size: 1.1rem;
        font-weight: 800;
        color: #ff69b4;
        margin: 4px 0;
    }

    .podium-quiz {
        font-size: 0.9rem;
        color: #c2185b;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🏆 LEADERBOARD 🎀</h1>", unsafe_allow_html=True)

def load_highscores():
    with open('data/highscores.json', 'r') as f:
        return json.load(f)

highscores = load_highscores()

if not highscores:
    st.info("No scores yet! Play a quiz to get on the leaderboard.")
else:
    normalized_scores = []
    for entry in highscores:
        score = int(entry.get('score', 0))
        total = int(entry.get('total', 0))
        percentage = entry.get('percentage')
        if percentage is None:
            percentage = round((score / total) * 100, 1) if total else 0.0

        normalized_scores.append({
            'name': entry.get('name', 'Unknown Player'),
            'category': entry.get('category', 'Unknown Quiz'),
            'score': score,
            'total': total,
            'percentage': float(percentage),
            'date': entry.get('date', 'Unknown')
        })

    # Sort by score, then accuracy as tiebreaker.
    sorted_scores = sorted(
        normalized_scores,
        key=lambda x: (x['score'], x['percentage']),
        reverse=True
    )

    st.subheader("Leaderboard Pedestal")
    top_three = sorted_scores[:3]
    podium_cols = st.columns(3)
    medals = ["🥇 #1", "🥈 #2", "🥉 #3"]

    for idx in range(3):
        with podium_cols[idx]:
            if idx < len(top_three):
                player = top_three[idx]
                st.markdown(
                    f"""
                    <div class="podium-card">
                        <div class="podium-rank">{medals[idx]}</div>
                        <div class="podium-name">{player['name']}</div>
                        <div class="podium-score">{player['score']} / {player['total']}</div>
                        <div class="podium-quiz">🎮 {player['category']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="podium-card">
                        <div class="podium-rank">Empty</div>
                        <div class="podium-name">No player yet</div>
                        <div class="podium-score">0 / 0</div>
                        <div class="podium-quiz">🎮 Waiting for a quiz</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.write("---")
    st.subheader("Top 10 Players")

    top_ten = sorted_scores[:10]
    df = pd.DataFrame(top_ten)
    df['Rank'] = range(1, len(df) + 1)
    df = df[['Rank', 'name', 'category', 'score', 'total', 'percentage', 'date']]
    df.columns = ['Rank', 'Nickname', 'Quiz', 'Score', 'Total', 'Accuracy %', 'Date']

    st.dataframe(df, use_container_width=True, hide_index=True)

    # Personal stats
    st.write("---")
    st.subheader("📊 Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Games Played", len(normalized_scores))
    
    with col2:
        avg_score = sum(s['score'] for s in normalized_scores) / len(normalized_scores)
        st.metric("Average Score", f"{avg_score:.1f}")
    
    with col3:
        avg_accuracy = sum(s['percentage'] for s in normalized_scores) / len(normalized_scores)
        st.metric("Average Accuracy", f"{avg_accuracy:.1f}%")
    
    with col4:
        max_score = max(s['score'] for s in normalized_scores)
        st.metric("Best Score", max_score)
