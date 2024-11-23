import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.ensemble import RandomForestClassifier

# Function to calculate weighted Poisson means
def calculate_weighted_means(team_stats, weights):
    weighted_avg = np.average(team_stats, weights=weights)
    return weighted_avg

# Function to calculate halftime and full-time probabilities
def calculate_ht_ft_probs(home_ht, away_ht, home_ft, away_ft, historical_transitions):
    ht_probs = np.outer(
        [poisson.pmf(i, home_ht) for i in range(3)],
        [poisson.pmf(i, away_ht) for i in range(3)]
    )
    ft_probs = np.outer(
        [poisson.pmf(i, home_ft) for i in range(6)],
        [poisson.pmf(i, away_ft) for i in range(6)]
    )

    # Historical transitions override static probabilities
    ht_ft_probs = {
        "1/1": np.sum(np.tril(ft_probs, -1)) * historical_transitions.get("1/1", 0.6),
        "1/X": np.sum(np.diag(ft_probs)) * historical_transitions.get("1/X", 0.4),
        "1/2": np.sum(np.triu(ft_probs, 1)) * historical_transitions.get("1/2", 0.2),
        "X/1": np.sum(np.tril(ft_probs, -1)) * historical_transitions.get("X/1", 0.4),
        "X/X": np.sum(np.diag(ft_probs)) * historical_transitions.get("X/X", 0.6),
        "X/2": np.sum(np.triu(ft_probs, 1)) * historical_transitions.get("X/2", 0.4),
    }

    return ht_probs, ft_probs, ht_ft_probs

# Value bet identification
def identify_value_bets(predicted_prob, bookmaker_odds):
    implied_prob = 1 / bookmaker_odds * 100
    return predicted_prob > implied_prob, predicted_prob - implied_prob

# Example data inputs
home_attack = 1.8
away_defense = 1.3
away_attack = 1.5
home_defense = 1.4

# Adjusted weights for recent form
recent_form = [2, 1.5, 1.0]  # Example recent form goals
weights = [0.5, 0.3, 0.2]
home_weighted_goals = calculate_weighted_means(recent_form, weights)
away_weighted_goals = calculate_weighted_means(recent_form[::-1], weights)

# Calculate goals
home_ht_goals = home_weighted_goals * away_defense * 0.5
away_ht_goals = away_weighted_goals * home_defense * 0.5
home_ft_goals = home_weighted_goals * away_defense
away_ft_goals = away_weighted_goals * home_defense

# Historical HT/FT transition data
historical_transitions = {
    "1/1": 0.5, "1/X": 0.3, "1/2": 0.2,
    "X/1": 0.4, "X/X": 0.6, "X/2": 0.3,
}

# Calculate probabilities
ht_probs, ft_probs, ht_ft_probs = calculate_ht_ft_probs(home_ht_goals, away_ht_goals, home_ft_goals, away_ft_goals, historical_transitions)

# Bookmaker odds example
bookmaker_odds = {"1/1": 4.50, "1/X": 5.00, "1/2": 15.00, "X/1": 6.00, "X/X": 3.50, "X/2": 7.00}

# Value bet detection
value_bets = {}
for outcome, odds in bookmaker_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100
    is_value, margin = identify_value_bets(predicted_prob, odds)
    value_bets[outcome] = {"Probability": predicted_prob, "Value Bet": is_value, "Margin": margin}

# Display recommendations
print("### HT/FT Probabilities and Value Bets")
for outcome, data in value_bets.items():
    print(f"{outcome}: {data['Probability']:.2f}% (Value Bet: {data['Value Bet']}, Margin: {data['Margin']:.2f}%)")

# Recommend best bet
best_bet = max(value_bets, key=lambda x: value_bets[x]["Margin"] if value_bets[x]["Value Bet"] else -1)
print(f"💡 Recommended Bet: {best_bet} (Probability: {value_bets[best_bet]['Probability']:.2f}%, Odds: {bookmaker_odds[best_bet]})")
