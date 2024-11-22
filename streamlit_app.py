import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial
from scipy.stats import poisson

# Streamlit Application Title
st.title("🤖 Advanced Rabiotic Football Outcome Predictor")
st.markdown("""
Predict football match outcomes using advanced metrics like:
- **Poisson Distribution**
- **Machine Learning**
- **Odds Analysis**
- **Margin Calculations**
- **Straight Home, Draw, and Away Win**
- **Correct Score**
- **Halftime/Full-time (HT/FT) ℅**
""")

# Sidebar Input
st.sidebar.header("Input Parameters")
st.sidebar.subheader("Home Team")
avg_home_goals_scored = st.sidebar.number_input("Average Goals Scored (Home)", min_value=0.0, value=1.5, step=0.1)
avg_home_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Home)", min_value=0.0, value=1.2, step=0.1)
avg_home_points = st.sidebar.number_input("Average Points (Home)", min_value=0.0, value=1.8, step=0.1)

st.sidebar.subheader("Away Team")
avg_away_goals_scored = st.sidebar.number_input("Average Goals Scored (Away)", min_value=0.0, value=1.2, step=0.1)
avg_away_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Away)", min_value=0.0, value=1.3, step=0.1)
avg_away_points = st.sidebar.number_input("Average Points (Away)", min_value=0.0, value=1.4, step=0.1)

st.sidebar.subheader("League Averages")
league_avg_goals_scored = st.sidebar.number_input("League Avg Goals Scored per Match", min_value=0.1, value=1.5, step=0.1)
league_avg_goals_conceded = st.sidebar.number_input("League Avg Goals Conceded per Match", min_value=0.1, value=1.5, step=0.1)

# Odds Input
home_win_odds = st.sidebar.number_input("Odds: Home Win", value=2.50, step=0.01)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20, step=0.01)
away_win_odds = st.sidebar.number_input("Odds: Away Win", value=3.10, step=0.01)
over_odds = st.sidebar.number_input("Over 2.5 Odds", value=2.40, step=0.01)
under_odds = st.sidebar.number_input("Under 2.5 Odds", value=1.55, step=0.01)

# Sidebar Multiselect
selected_points = st.sidebar.multiselect(
    "Select Points for Probabilities and Odds",
    options=["Home Win", "Draw", "Away Win", "Over 2.5", "Under 2.5", 
             "Correct Score", "HT/FT", "BTTS", "Exact Goals"]
)

st.subheader("Selected Points for Prediction")
st.write(selected_points)

# Mock Calculation Functions
def calculate_ht_ft_probabilities():
    data = {"Half Time / Full Time": ["1/1", "1/X", "1/2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"],
            "Probabilities (%)": [26.0, 4.8, 1.6, 16.4, 17.4, 11.2, 2.2, 4.8, 15.5]}
    return pd.DataFrame(data)

def calculate_correct_score_probabilities():
    data = {"Score": ["1:0", "2:0", "2:1", "3:0", "3:1", "3:2", "4:0", "4:1", "5:0"],
            "Probabilities (%)": [12.4, 8.5, 8.8, 3.9, 4.0, 2.1, 1.3, 1.4, 0.4]}
    return pd.DataFrame(data)

def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)

# Calculations for Probabilities
home_attack_strength = avg_home_goals_scored / league_avg_goals_scored
away_attack_strength = avg_away_goals_scored / league_avg_goals_scored
home_defense_strength = avg_home_goals_conceded / league_avg_goals_conceded
away_defense_strength = avg_away_goals_conceded / league_avg_goals_conceded

home_expected_goals = home_attack_strength * away_defense_strength * league_avg_goals_scored
away_expected_goals = away_attack_strength * home_defense_strength * league_avg_goals_scored

st.subheader("Expected Goals")
st.write(f"**Home Expected Goals:** {home_expected_goals:.2f}")
st.write(f"**Away Expected Goals:** {away_expected_goals:.2f}")

# Score Probabilities
st.subheader("Scoreline Probabilities")
max_goals = st.slider("Max Goals to Display", min_value=3, max_value=10, value=5)

for home_goals in range(max_goals + 1):
    for away_goals in range(max_goals + 1):
        prob = poisson_prob(home_expected_goals, home_goals) * poisson_prob(away_expected_goals, away_goals)
        st.write(f"{home_goals} - {away_goals}: {prob:.2%}")

# Final Predictions
if selected_points:
    st.subheader("Prediction Results")
    if "Correct Score" in selected_points:
        st.table(calculate_correct_score_probabilities())
    if "HT/FT" in selected_points:
        st.table(calculate_ht_ft_probabilities())
