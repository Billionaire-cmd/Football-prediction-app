import streamlit as st
from scipy.stats import poisson
import numpy as np

# Title of the App
st.title("🤖 Rabiotic Football Match Outcome Predictor")

# Sidebar Input
st.sidebar.header("Input Team Data")

st.sidebar.subheader("Home Team")
avg_home_goals_scored = st.sidebar.number_input("Average Goals Scored (Home)", min_value=0.0, value=1.5, step=0.1)
avg_home_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Home)", min_value=0.0, value=1.2, step=0.1)
avg_home_points = st.sidebar.number_input("Average Points (Home)", min_value=0.0, value=1.8, step=0.1)

st.sidebar.subheader("Away Team")
avg_away_goals_scored = st.sidebar.number_input("Average Goals Scored (Away)", min_value=0.0, value=1.2, step=0.1)
avg_away_goals_conceded = st.sidebar.number_input("Average Goals Conceded (Away)", min_value=0.0, value=1.3, step=0.1)
avg_away_points = st.sidebar.number_input("Average Points (Away)", min_value=0.0, value=1.4, step=0.1)

st.sidebar.subheader("League Averages")
league_avg_goals_scored = st.sidebar.number_input("League Average Goals Scored per Match", min_value=0.1, value=1.5, step=0.1)
league_avg_goals_conceded = st.sidebar.number_input("League Average Goals Conceded per Match", min_value=0.1, value=1.5, step=0.1)

# Calculate Attack and Defense Strengths
home_attack_strength = avg_home_goals_scored / league_avg_goals_scored
home_defense_strength = avg_home_goals_conceded / league_avg_goals_conceded

away_attack_strength = avg_away_goals_scored / league_avg_goals_scored
away_defense_strength = avg_away_goals_conceded / league_avg_goals_conceded

# Calculate Expected Goals
home_expected_goals = home_attack_strength * away_defense_strength * league_avg_goals_scored
away_expected_goals = away_attack_strength * home_defense_strength * league_avg_goals_scored

# Display Calculated Strengths and Expected Goals
st.subheader("Calculated Strengths")
st.write(f"**Home Attack Strength:** {home_attack_strength:.2f}")
st.write(f"**Home Defense Strength:** {home_defense_strength:.2f}")
st.write(f"**Away Attack Strength:** {away_attack_strength:.2f}")
st.write(f"**Away Defense Strength:** {away_defense_strength:.2f}")

st.subheader("Expected Goals")
st.write(f"**Home Team Expected Goals:** {home_expected_goals:.2f}")
st.write(f"**Away Team Expected Goals:** {away_expected_goals:.2f}")

# Function to Calculate Score Probabilities
def calculate_score_probabilities(home_goals, away_goals):
    home_probs = poisson.pmf(home_goals, home_expected_goals)
    away_probs = poisson.pmf(away_goals, away_expected_goals)
    return home_probs * away_probs

# Predict Probabilities for Scorelines
st.subheader("Score Probabilities for Match Outcome")
for home_goals in range(int(home_expected_goals) - 2, int(home_expected_goals) + 3):
    for away_goals in range(int(away_expected_goals) - 2, int(away_expected_goals) + 3):
        prob = calculate_score_probabilities(home_goals, away_goals)
        st.write(f"{home_goals} - {away_goals}: {prob:.2%}")

# Displaying halftime and full-time probabilities based on Poisson
home_ht_goals = home_attack_strength * away_defense_strength * 0.5
away_ht_goals = away_attack_strength * home_defense_strength * 0.5
ft_probs = poisson.pmf(home_ft_goals, home_expected_goals) * poisson.pmf(away_ft_goals, away_expected_goals)

st.subheader("Halftime and Fulltime Probabilities")
st.write("Halftime Probabilities:")
for i in range(3):  # 0 to 2 goals for halftime
    for j in range(3):  # 0 to 2 goals for away team
        st.write(f"HT: {i} - FT: {j}: {poisson.pmf(i, home_ht_goals) * poisson.pmf(j, away_ht_goals):.2%}")

st.write("Fulltime Probabilities:")
for i in range(6):  # 0 to 5 goals for home team
    for j in range(6):  # 0 to 5 goals for away team
        st.write(f"FT: {i} - {j}: {ft_probs[i, j]:.2%}")

# Sidebar for bookmaker odds and value bet calculation
st.sidebar.header("Bookmaker Odds")
odds_1_1 = st.sidebar.number_input("Odds for HT Home / FT Home", min_value=1.0, value=4.50)
odds_1_X = st.sidebar.number_input("Odds for HT Home / FT Draw", min_value=1.0, value=5.00)
odds_1_2 = st.sidebar.number_input("Odds for HT Home / FT Away", min_value=1.0, value=15.00)

bookmaker_odds = {
    "1/1": odds_1_1,  # Odds for HT Home / FT Home
    "1/X": odds_1_X,  # Odds for HT Home / FT Draw
    "1/2": odds_1_2,  # Odds for HT Home / FT Away
}

# Function to identify value bets
def identify_value_bets(predicted_prob, bookmaker_odds, risk_factor=0.05):
    implied_prob = 1 / bookmaker_odds * 100  # Calculate implied probability
    margin = predicted_prob - implied_prob
    value_bet = margin > risk_factor * implied_prob  # Only bet if margin exceeds threshold
    return value_bet, margin

# Identify value bets based on predictions
st.subheader("Value Bets")
for outcome, odds in bookmaker_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100  # Convert to percentage
    is_value_bet, value_margin = identify_value_bets(predicted_prob, odds)
    st.write(f"{outcome}: {predicted_prob:.2f}% (Bookmaker Odds: {odds})")
    if is_value_bet:
        st.write(f"  🔥 **Value Bet!** Margin: {value_margin:.2f}%")

# Display the best recommended bet
best_bet = max(bookmaker_odds.keys(), key=lambda x: ht_ft_probs[x] - 1 / bookmaker_odds[x])
st.write(f"💡 **Recommended Bet:** {best_bet} (Probability: {ht_ft_probs[best_bet]*100:.2f}%, Odds: {bookmaker_odds[best_bet]})")
