import streamlit as st
from scipy.stats import poisson

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
st.subheader("Predicted Probabilities for Scorelines")
score_probabilities = {}
for home_goals in range(6):
    for away_goals in range(6):
        score_probabilities[f"{home_goals}-{away_goals}"] = calculate_score_probabilities(home_goals, away_goals)

# Display Predicted Probabilities
for scoreline, prob in score_probabilities.items():
    st.write(f"**{scoreline}**: {prob * 100:.2f}%")

# Function to Calculate Halftime/Fulltime Probabilities
def calculate_ht_ft_probs(home_ht, away_ht, home_ft, away_ft):
    # Halftime Poisson probabilities (0-2 goals assumed)
    ht_probs = np.outer(
        [poisson.pmf(i, home_ht) for i in range(3)], 
        [poisson.pmf(i, away_ht) for i in range(3)]
    )

    # Fulltime Poisson probabilities (0-5 goals assumed)
    ft_probs = np.outer(
        [poisson.pmf(i, home_ft) for i in range(6)], 
        [poisson.pmf(i, away_ft) for i in range(6)]
    )

    # HT -> FT transition probabilities
    ht_ft_probs = {
        "1/1": np.sum(np.tril(ft_probs, -1)) * 0.6,  # Halftime Home, Fulltime Home
        "1/X": np.sum(np.diag(ft_probs)) * 0.4,      # Halftime Home, Fulltime Draw
        "1/2": np.sum(np.triu(ft_probs, 1)) * 0.2,   # Halftime Home, Fulltime Away
        "X/1": np.sum(np.tril(ft_probs, -1)) * 0.4,  # Halftime Draw, Fulltime Home
        "X/X": np.sum(np.diag(ft_probs)) * 0.6,      # Halftime Draw, Fulltime Draw
        "X/2": np.sum(np.triu(ft_probs, 1)) * 0.4,   # Halftime Draw, Fulltime Away
    }

    return ht_probs, ft_probs, ht_ft_probs

# Calculate halftime and fulltime goals
home_ht_goals = home_attack_strength * away_defense_strength * 0.5  # Adjusted halftime goals
away_ht_goals = away_attack_strength * home_defense_strength * 0.5
home_ft_goals = home_attack_strength * away_defense_strength
away_ft_goals = away_attack_strength * home_defense_strength

# Generate probabilities for HT/FT
ht_probs, ft_probs, ht_ft_probs = calculate_ht_ft_probs(home_ht_goals, away_ht_goals, home_ft_goals, away_ft_goals)

# Display HT/FT Probabilities
st.subheader("HT/FT Probabilities")
for outcome, prob in ht_ft_probs.items():
    st.write(f"**{outcome}:** {prob * 100:.2f}%")

# Function to identify value bets based on odds and predicted probabilities
def identify_value_bets(predicted_prob, bookmaker_odds, risk_factor=0.05):
    implied_prob = 1 / bookmaker_odds * 100  # Calculate implied probability
    margin = predicted_prob - implied_prob
    value_bet = margin > risk_factor * implied_prob  # Only bet if margin exceeds threshold
    return value_bet, margin

# Example bookmaker odds for HT/FT outcomes
bookmaker_odds = {
    "1/1": 4.50,  # Odds for HT Home / FT Home
    "1/X": 5.00,  # Odds for HT Home / FT Draw
    "1/2": 15.00, # Odds for HT Home / FT Away
    "X/1": 6.00,  # Odds for HT Draw / FT Home
    "X/X": 3.50,  # Odds for HT Draw / FT Draw
    "X/2": 7.00,  # Odds for HT Draw / FT Away
}

# Display value bets
st.subheader("Value Bets")
for outcome, odds in bookmaker_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100  # Convert to percentage
    is_value_bet, value_margin = identify_value_bets(predicted_prob, odds)
    st.write(f"{outcome}: {predicted_prob:.2f}% (Bookmaker Odds: {odds})")
    if is_value_bet:
        st.write(f"  🔥 **Value Bet!** Margin: {value_margin:.2f}%")
