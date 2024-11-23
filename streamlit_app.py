import numpy as np
from scipy.stats import poisson
import streamlit as st

# Function to calculate halftime and full-time probabilities
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

# Function to calculate value bets
def identify_value_bets(predicted_prob, bookmaker_odds):
    implied_prob = 1 / bookmaker_odds * 100  # Calculate implied probability
    return predicted_prob > implied_prob, predicted_prob - implied_prob

# Input parameters (can be replaced with user inputs)
home_attack = 1.8  # Home team attack strength
away_defense = 1.3  # Away team defensive strength
away_attack = 1.5  # Away team attack strength
home_defense = 1.4  # Home team defensive strength

# Calculate halftime and fulltime goals
home_ht_goals = home_attack * away_defense * 0.5  # Adjusted halftime goals
away_ht_goals = away_attack * home_defense * 0.5
home_ft_goals = home_attack * away_defense
away_ft_goals = away_attack * home_defense

# Generate probabilities
ht_probs, ft_probs, ht_ft_probs = calculate_ht_ft_probs(home_ht_goals, away_ht_goals, home_ft_goals, away_ft_goals)

# Example bookmaker odds
bookmaker_odds = {
    "1/1": 4.50,  # Odds for HT Home / FT Home
    "1/X": 5.00,  # Odds for HT Home / FT Draw
    "1/2": 15.00, # Odds for HT Home / FT Away
    "X/1": 6.00,  # Odds for HT Draw / FT Home
    "X/X": 3.50,  # Odds for HT Draw / FT Draw
    "X/2": 7.00,  # Odds for HT Draw / FT Away
}

# Display probabilities and identify value bets
st.markdown("### HT/FT Probabilities and Value Bets")
for outcome, odds in bookmaker_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100  # Convert to percentage
    is_value_bet, value_margin = identify_value_bets(predicted_prob, odds)
    st.write(f"{outcome}: {predicted_prob:.2f}% (Bookmaker Odds: {odds})")
    if is_value_bet:
        st.write(f"  🔥 Value Bet! Margin: {value_margin:.2f}%")

# Custom recommendation based on highest value margin
best_bet = max(bookmaker_odds.keys(), key=lambda x: ht_ft_probs[x] - 1 / bookmaker_odds[x])
st.write(f"💡 Recommended Bet: {best_bet} (Probability: {ht_ft_probs[best_bet]*100:.2f}%, Odds: {bookmaker_odds[best_bet]})")
