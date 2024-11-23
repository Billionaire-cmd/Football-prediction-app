import streamlit as st
import numpy as np
from scipy.stats import poisson

# Streamlit App Title
st.title("🤖 Advanced Rabiotic Correct Score Prediction Pro")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
st.sidebar.subheader("Team Strengths")
home_attack_strength = st.sidebar.number_input("Home Attack Strength", value=0.54, step=0.01)
home_defense_strength = st.sidebar.number_input("Home Defense Strength", value=1.23, step=0.01)
away_attack_strength = st.sidebar.number_input("Away Attack Strength", value=0.85, step=0.01)
away_defense_strength = st.sidebar.number_input("Away Defense Strength", value=1.46, step=0.01)

st.sidebar.subheader("Expected Goals")
home_expected_goals = st.sidebar.number_input("Home Team Expected Goals", value=1.02, step=0.01)
away_expected_goals = st.sidebar.number_input("Away Team Expected Goals", value=1.35, step=0.01)

st.sidebar.subheader("Odds")
home_odds = st.sidebar.number_input("Odds: Home Win", value=2.59, step=0.01)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.17, step=0.01)
away_odds = st.sidebar.number_input("Odds: Away Win", value=3.17, step=0.01)
over_2_5_odds = st.sidebar.number_input("Over 2.5 Odds", value=2.55, step=0.01)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Odds", value=1.54, step=0.01)

st.sidebar.subheader("Margin Targets")
match_results_margin = st.sidebar.number_input("Match Results Margin", value=2.30, step=0.01)
asian_handicap_margin = st.sidebar.number_input("Asian Handicap Margin", value=5.14, step=0.01)
over_under_margin = st.sidebar.number_input("Over/Under Margin", value=4.15, step=0.01)
exact_goals_margin = st.sidebar.number_input("Exact Goals Margin", value=18.21, step=0.01)
correct_score_margin = st.sidebar.number_input("Correct Score Margin", value=25.76, step=0.01)
ht_ft_margin = st.sidebar.number_input("HT/FT Margin", value=18.02, step=0.01)

st.sidebar.subheader("Prediction Options")
prediction_options = st.sidebar.multiselect(
    "Select Probabilities and Odds to Calculate",
    [
        "Home win", "Draw win", "Away win", "Over 2.5", "Under 2.5",
        "Correct score", "HT/FT", "Exact goals", "Both teams to score (BTTS)"
    ],
    default=["Correct score", "HT/FT"]
)

if st.sidebar.button("Submit Predictions"):
    # Poisson Distribution Function
    def poisson_prob(mean, goals):
        return poisson.pmf(goals, mean)

    # Calculate Scoreline Probabilities
    home_goal_probs = [poisson_prob(home_expected_goals, i) for i in range(6)]
    away_goal_probs = [poisson_prob(away_expected_goals, i) for i in range(6)]
    scoreline_probs = np.outer(home_goal_probs, away_goal_probs)

    # Most Likely Correct Score
    most_likely_score = np.unravel_index(scoreline_probs.argmax(), scoreline_probs.shape)
    most_likely_score_prob = scoreline_probs[most_likely_score] * 100

    # Outcome Probabilities
    home_win_prob = np.sum(np.tril(scoreline_probs, -1)) * 100
    draw_prob = np.sum(np.diag(scoreline_probs)) * 100
    away_win_prob = np.sum(np.triu(scoreline_probs, 1)) * 100

    over_2_5_prob = np.sum(scoreline_probs[3:, 0:]) + np.sum(scoreline_probs[:, 3:]) - np.sum(scoreline_probs[3:, 3:])
    over_2_5_prob *= 100
    under_2_5_prob = 100 - over_2_5_prob

    btts_yes_prob = (1 - (home_goal_probs[0] * away_goal_probs[0])) * 100

    # HT/FT Probabilities
    ht_ft_probs = {
        "1/1": home_win_prob / 2.5,
        "1/X": draw_prob / 3,
        "1/2": away_win_prob / 6,
        "X/1": home_win_prob / 3,
        "X/X": draw_prob / 2.5,
        "X/2": away_win_prob / 4,
        "2/1": home_win_prob / 5,
        "2/X": draw_prob / 4,
        "2/2": away_win_prob / 2,
    }

    # Refined Prediction (4-2 FT, 1-1 HT)
    refined_ft_score = (4, 2)
    refined_ht_score = (1, 1)
    refined_ft_prob = scoreline_probs[refined_ft_score] * 100
    refined_ht_prob = poisson_prob(home_expected_goals / 2, 1) * poisson_prob(away_expected_goals / 2, 1) * 100

    # Output Results
    st.subheader("Prediction Results")
    st.write(f"**Most Likely Scoreline:** {most_likely_score[0]}-{most_likely_score[1]} "
             f"with a probability of {most_likely_score_prob:.2f}%")
    st.write(f"**Refined Full-Time Scoreline:** {refined_ft_score[0]}-{refined_ft_score[1]} "
             f"with a probability of {refined_ft_prob:.2f}%")
    st.write(f"**Refined Half-Time Scoreline:** {refined_ht_score[0]}-{refined_ht_score[1]} "
             f"with a probability of {refined_ht_prob:.2f}%")
    st.write(f"**Home Win Probability:** {home_win_prob:.2f}%")
    st.write(f"**Draw Probability:** {draw_prob:.2f}%")
    st.write(f"**Away Win Probability:** {away_win_prob:.2f}%")
    st.write(f"**Over 2.5 Goals Probability:** {over_2_5_prob:.2f}%")
    st.write(f"**Under 2.5 Goals Probability:** {under_2_5_prob:.2f}%")
    st.write(f"**BTTS (Yes) Probability:** {btts_yes_prob:.2f}%")

    st.subheader("HT/FT Probabilities")
    for scenario, prob in ht_ft_probs.items():
        st.write(f"{scenario}: {prob:.2f}%")
