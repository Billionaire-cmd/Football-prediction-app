import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import streamlit as st
import matplotlib.pyplot as plt
from math import factorial

# Set up the Streamlit page configuration
st.set_page_config(page_title="🤖 Rabiotic Advanced Prediction", layout="wide")

# Streamlit Application Title
st.title("🤖 Advanced Rabiotic Football Outcome Predictor")
st.markdown("""
Predict football match outcomes using advanced metrics like:
- **Poisson Distribution**
- **Machine Learning**
- **Odds Analysis**
- **Margin Calculations**
""")

# Sidebar for Input Parameters
st.sidebar.header("Input Parameters")

# Match and Odds Input
home_team = st.sidebar.text_input("Home Team", "Team A")
away_team = st.sidebar.text_input("Away Team", "Team B")
goals_home_mean = st.sidebar.number_input("Expected Goals (Home)", min_value=0.1, value=1.2, step=0.1)
goals_away_mean = st.sidebar.number_input("Expected Goals (Away)", min_value=0.1, value=1.1, step=0.1)

# Odds Input
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

# Select Points for Probabilities and Odds
selected_points = st.sidebar.multiselect(
    "Select Points for Probabilities and Odds",
    options=["Home Win", "Draw", "Away Win", "Over 2.5", "Under 2.5", "Correct Score", "HT/FT", "BTTS", "Exact Goals"]
)

# Submit Button
submit_button = st.sidebar.button("Submit Prediction")

# Functions

def calculate_margin_difference(odds, margin_target):
    return round(margin_target - odds, 2)

def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)  # Using `factorial` from `math`

def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    return home_probs, away_probs

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

def identify_value_bets(predicted_prob, bookmaker_odds, risk_factor=0.05):
    implied_prob = 1 / bookmaker_odds * 100  # Calculate implied probability
    margin = predicted_prob - implied_prob
    value_bet = margin > risk_factor * implied_prob  # Only bet if margin exceeds threshold
    return value_bet, margin

# Machine Learning Model for Additional Refinement
def train_ml_model(historical_data):
    # Features: [home_attack, away_defense, home_defense, away_attack, etc.]
    X = historical_data[['home_attack', 'away_defense', 'home_defense', 'away_attack']]
    y = historical_data['outcome']  # Target: [1 for Home Win, 0 for Draw, -1 for Away Win]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

# Historical Data for Training
historical_data = {
    'home_attack': [1.8, 2.0, 1.6],
    'away_defense': [1.3, 1.4, 1.2],
    'home_defense': [1.4, 1.3, 1.6],
    'away_attack': [1.5, 1.7, 1.4],
    'outcome': [1, 0, -1]  # 1 = Home Win, 0 = Draw, -1 = Away Win
}

historical_data = pd.DataFrame(historical_data)

# Train the machine learning model
model, accuracy = train_ml_model(historical_data)

# Display Model Accuracy
st.write(f"Model Accuracy: {accuracy * 100:.2f}%")

# Calculate Home and Away Probabilities
home_probs, away_probs = calculate_probabilities(goals_home_mean, goals_away_mean)

# Generate HT/FT Probabilities
home_ht_goals = goals_home_mean * 0.5  # Adjusted halftime goals
away_ht_goals = goals_away_mean * 0.5
home_ft_goals = goals_home_mean
away_ft_goals = goals_away_mean

ht_probs, ft_probs, ht_ft_probs = calculate_ht_ft_probs(home_ht_goals, away_ht_goals, home_ft_goals, away_ft_goals)

# Example bookmaker odds
bookmaker_odds = {
    "1/1": home_win_odds,  # Odds for HT Home / FT Home
    "1/X": draw_odds,      # Odds for HT Home / FT Draw
    "1/2": away_win_odds,  # Odds for HT Home / FT Away
    "X/1": home_win_odds,  # Odds for HT Draw / FT Home
    "X/X": draw_odds,      # Odds for HT Draw / FT Draw
    "X/2": away_win_odds,  # Odds for HT Draw / FT Away
}

# Display probabilities and identify value bets
st.markdown("### HT/FT Probabilities and Value Bets")
for outcome, odds in bookmaker_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100  # Convert to percentage
    is_value_bet, value_margin = identify_value_bets(predicted_prob, odds)
    st.write(f"{outcome}: {predicted_prob:.2f}% (Bookmaker Odds: {odds})")
    if is_value_bet:
        st.write(f"  🔥 **Value Bet!** Margin: {value_margin:.2f}%")

# Custom recommendation based on highest value margin
best_bet = max(bookmaker_odds.keys(), key=lambda x: ht_ft_probs[x] - 1 / bookmaker_odds[x])
st.write(f"\n### Best Recommended Bet: {best_bet}")
