import streamlit as st
import numpy as np
from scipy.stats import poisson

# Set up the Streamlit App
st.set_page_config(
    page_title="🤖 Advanced Rabiotic Correct Score Prediction Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description
st.title("🤖 Advanced Rabiotic Correct Score Prediction Pro")
st.markdown("""
This app calculates probabilities and odds for football (soccer) match outcomes using Poisson and Skellam distributions, 
and provides realistic predictions for match results, correct scores, and more.
""")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
st.sidebar.markdown("### Team Strength")
home_attack = st.sidebar.number_input("Home Attack Strength", value=1.00)
home_defense = st.sidebar.number_input("Home Defense Strength", value=0.80)
away_attack = st.sidebar.number_input("Away Attack Strength", value=0.80)
away_defense = st.sidebar.number_input("Away Defense Strength", value=0.87)

st.sidebar.markdown("### Expected Goals")
home_expected_goals = st.sidebar.number_input("Home Team Expected Goals", value=1.30)
away_expected_goals = st.sidebar.number_input("Away Team Expected Goals", value=0.96)

st.sidebar.markdown("### Odds")
home_odds = st.sidebar.number_input("Odds: Home", value=2.20)
draw_odds = st.sidebar.number_input("Odds: Draw", value=3.20)
away_odds = st.sidebar.number_input("Odds: Away", value=2.70)
over_odds = st.sidebar.number_input("Over 2.5 Odds", value=2.50)
under_odds = st.sidebar.number_input("Under 2.5 Odds", value=1.40)

st.sidebar.markdown("### Margin Targets")
match_results_margin = st.sidebar.number_input("Match Results Margin", value=5.20)
asian_handicap_margin = st.sidebar.number_input("Asian Handicap Margin", value=6.00)
over_under_margin = st.sidebar.number_input("Over/Under Margin", value=7.50)
exact_goals_margin = st.sidebar.number_input("Exact Goals Margin", value=19.56)
correct_score_margin = st.sidebar.number_input("Correct Score Margin", value=20.78)
ht_ft_margin = st.sidebar.number_input("HT/FT Margin", value=26.01)

st.sidebar.markdown("### Select Points for Probabilities and Odds")
selected_points = st.sidebar.multiselect(
    "Select Points",
    ["Home win", "Draw win", "Away win", "Over 2.5", "Under 2.5", "Correct score", "HT/FT", "Exact goals", "Both teams to score"],
    default=["Home win", "Draw win", "Away win"]
)

if st.sidebar.button("Submit Predictions"):
    # Calculate Probabilities
    def poisson_prob(avg_goals, k):
        return poisson.pmf(k, avg_goals)

    def calculate_outcomes(home_exp, away_exp):
        home_probs = [poisson_prob(home_exp, i) for i in range(6)]
        away_probs = [poisson_prob(away_exp, i) for i in range(6)]
        probabilities = np.outer(home_probs, away_probs)
        return probabilities

    probabilities = calculate_outcomes(home_expected_goals, away_expected_goals)

    # Win Probabilities
    home_win_prob = np.sum(np.tril(probabilities, -1)) * 100
    draw_prob = np.sum(np.diag(probabilities)) * 100
    away_win_prob = np.sum(np.triu(probabilities, 1)) * 100

    # Over/Under 2.5 Goals
    over_2_5_prob = (1 - np.sum(probabilities[:3, :3])) * 100
    under_2_5_prob = np.sum(probabilities[:3, :3]) * 100

    # Correct Score Probabilities
    correct_scores = [(i, j, probabilities[i, j] * 100) for i in range(6) for j in range(6)]
    correct_scores = sorted(correct_scores, key=lambda x: x[2], reverse=True)

    # HT/FT Probabilities
    ht_ft_probs = {
        "1/1": home_win_prob * 0.6,  # Example adjustment
        "1/X": home_win_prob * 0.2,
        "1/2": home_win_prob * 0.2,
        "X/1": draw_prob * 0.4,
        "X/X": draw_prob * 0.6,
        "X/2": draw_prob * 0.4,
        "2/1": away_win_prob * 0.2,
        "2/X": away_win_prob * 0.2,
        "2/2": away_win_prob * 0.6,
    }

    # Both Teams to Score
    btts_yes_prob = np.sum(probabilities[1:, 1:]) * 100
    btts_no_prob = (1 - np.sum(probabilities[1:, 1:])) * 100

    # Most Likely Outcome
    most_likely_score = max(correct_scores, key=lambda x: x[2])

    # Display Outputs
    st.header("Prediction Results")
    st.write(f"### Home Win Probability: {home_win_prob:.2f}%")
    st.write(f"### Draw Probability: {draw_prob:.2f}%")
    st.write(f"### Away Win Probability: {away_win_prob:.2f}%")
    st.write(f"### Over 2.5 Probability: {over_2_5_prob:.2f}%")
    st.write(f"### Under 2.5 Probability: {under_2_5_prob:.2f}%")

    st.markdown("### HT/FT Probabilities")
    for k, v in ht_ft_probs.items():
        st.write(f"{k}: {v:.2f}%")

    st.markdown("### Correct Score Probabilities")
    for score in correct_scores[:5]:
        st.write(f"{score[0]}-{score[1]}: {score[2]:.2f}%")

    st.markdown("### Both Teams to Score")
    st.write(f"Yes: {btts_yes_prob:.2f}%, No: {btts_no_prob:.2f}%")

    st.markdown("### Recommendation")
    st.write(f"The most likely scoreline is {most_likely_score[0]}-{most_likely_score[1]} with a probability of {most_likely_score[2]:.2f}%.")
