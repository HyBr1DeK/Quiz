# QuizMaster 🎯

A fun and interactive quiz application built with Streamlit.

## Features
- Multiple quiz categories
- Real-time scoring with time tracking
- Highscores leaderboard
- Player name tracking
- Category selection

## Installation

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
streamlit run Home.py
```

## Deployment

This app is deployed on [Streamlit Cloud](https://streamlit.io/cloud).

## Requirements
- Python 3.8+
- Streamlit
- Pandas

## Project Structure
```
├── Home.py
├── requirements.txt
├── data/
│   ├── questions.json
│   └── highscores.json
└── pages/
    ├── _Categories.py
    ├── _Highscores.py
    └── _Quiz.py
```
