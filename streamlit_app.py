import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial  # Correct import for factorial
from scipy.stats import poisson

# Title and Description
st.title("🤖 Advanced Rabiotic Football Outcome Predictor")
st.markdown("""
Predict football match outcomes using advanced metrics such as:
- **Poisson Distribution**
- **Machine Learning**
- **Odds Analysis**
- **Margin Calculations**
- **Straight Home, Draw, and Away Win**
- **Correct Score**
- **Halftime/Full-time (HT/FT)℅**
""")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

# Team Data Inputs
st.sidebar.subheader("Home Team")
avg_home_goals_scored = st.sidebar.number_input("Avg Goals Scored (Home)", min_value=0.0, value=1.5, step=0.1)
avg_home_goals_conceded = st.sidebar.number_input("Avg Goals Conceded (Home)", min_value=0.0, value=1.2, step=0.1)
avg_home_points = st.sidebar.number_input("Avg Points (Home)", min_value=0.0, value=1.8, step=0.1)

st.sidebar.subheader("Away Team")
avg_away_goals_scored = st.sidebar.number_input("Avg Goals Scored (Away)", min_value=0.0, value=1.2, step=0.1)
avg_away_goals_conceded = st.sidebar.number_input("Avg Goals Conceded (Away)", min_value=0.0, value=1.3, step=0.1)
avg_away_points = st.sidebar.number_input("Avg Points (Away)", min_value=0.0, value=1.4, step=0.1)

st.sidebar.subheader("League Averages")
league_avg_goals_scored = st.sidebar.number_input("League Avg Goals per Match", min_value=0.1, value=1.5, step=0.1)
league_avg_goals_conceded = st.sidebar.number_input("League Avg Goals Conceded per Match", min_value=0.1, value=1.5, step=0.1)

# Odds Inputs
st.sidebar.subheader("Odds")
home_win_odds = st.sidebar.number_input("Odds: Home Win", value=2.50, step=0.01)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20, step=0.01)
away_win_odds = st.sidebar.number_input("Odds: Away Win", value=3.10, step=0.01)
over_odds = st.sidebar.number_input("Over 2.5 Odds", value=2.40, step=0.01)
under_odds = st.sidebar.number_input("Under 2.5 Odds", value=1.55, step=0.01)

# Margin Targets
st.sidebar.subheader("Margin Targets")
margin_targets = {
    "Match Results": st.sidebar.number_input("Match Results Margin", value=4.95, step=0.01),
    "Asian Handicap": st.sidebar.number_input("Asian Handicap Margin", value=5.90, step=0.01),
    "Over/Under": st.sidebar.number_input("Over/Under Margin", value=6.18, step=0.01),
    "Exact Goals": st.sidebar.number_input("Exact Goals Margin", value=20.0, step=0.01),
    "Correct Score": st.sidebar.number_input("Correct Score Margin", value=57.97, step=0.01),
    "HT/FT": st.sidebar.number_input("HT/FT Margin", value=20.0, step=0.01),
}

# Selected Points
selected_points = st.sidebar.multiselect(
    "Select Points for Probabilities and Odds",
    options=[
        "Home Win", "Draw", "Away Win",
        "Over 2.5", "Under 2.5",
        "Correct Score", "HT/FT",
        "BTTS", "Exact Goals"
    ]
)

# Display Selected Points
st.subheader("Selected Points for Prediction")
st.write(selected_points)

# Functions for Probability Calculations
def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)

def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    return [
        (i, j, home_probs[i] * away_probs[j])
        for i in range(max_goals + 1)
        for j in range(max_goals + 1)
    ]

def calculate_margin_difference(odds, margin_target):
    return round(margin_target - odds, 2)

# Attack and Defense Strengths
home_attack_strength = avg_home_goals_scored / league_avg_goals_scored
home_defense_strength = avg_home_goals_conceded / league_avg_goals_conceded
away_attack_strength = avg_away_goals_scored / league_avg_goals_scored
away_defense_strength = avg_away_goals_conceded / league_avg_goals_conceded

# Expected Goals
home_expected_goals = home_attack_strength * away_defense_strength * league_avg_goals_scored
away_expected_goals = away_attack_strength * home_defense_strength * league_avg_goals_scored

# Display Calculated Strengths
st.subheader("Calculated Strengths")
st.write(f"**Home Attack Strength:** {home_attack_strength:.2f}")
st.write(f"**Home Defense Strength:** {home_defense_strength:.2f}")
st.write(f"**Away Attack Strength:** {away_attack_strength:.2f}")
st.write(f"**Away Defense Strength:** {away_defense_strength:.2f}")

# Expected Goals Display
st.subheader("Expected Goals")
st.write(f"**Home Team Expected Goals:** {home_expected_goals:.2f}")
st.write(f"**Away Team Expected Goals:** {away_expected_goals:.2f}")

# Scoreline Probabilities
st.subheader("Scoreline Probabilities")
max_goals = st.slider("Max Goals to Display", min_value=3, max_value=10, value=5)
probabilities = calculate_probabilities(home_expected_goals, away_expected_goals, max_goals)

# Display Scoreline Probabilities
prob_table = {
    "Home Goals": [],
    "Away Goals": [],
    "Probability (%)": [],
}

for home_goals, away_goals, prob in probabilities:
    prob_table["Home Goals"].append(home_goals)
    prob_table["Away Goals"].append(away_goals)
    prob_table["Probability (%)"].append(round(prob * 100, 2))

prob_df = pd.DataFrame(prob_table)
st.table(prob_df)

# Submit Button
if st.sidebar.button("Submit Prediction"):
    st.success("Prediction submitted successfully!")
