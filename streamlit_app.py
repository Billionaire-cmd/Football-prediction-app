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
st.set_page_config(page_title="🤖 Advanced Rabiotic Prediction", layout="wide")

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

# HT/FT Odds
ht_ft_odds = {
    "1/1": st.sidebar.number_input("HT Home / FT Home Odds", value=3.00, step=0.01),
    "1/X": st.sidebar.number_input("HT Home / FT Draw Odds", value=4.00, step=0.01),
    "1/2": st.sidebar.number_input("HT Home / FT Away Odds", value=6.00, step=0.01),
    "X/1": st.sidebar.number_input("HT Draw / FT Home Odds", value=4.50, step=0.01),
    "X/X": st.sidebar.number_input("HT Draw / FT Draw Odds", value=4.00, step=0.01),
    "X/2": st.sidebar.number_input("HT Draw / FT Away Odds", value=4.20, step=0.01),
    "2/1": st.sidebar.number_input("HT Away / FT Home Odds", value=8.00, step=0.01),
    "2/X": st.sidebar.number_input("HT Away / FT Draw Odds", value=8.50, step=0.01),
    "2/2": st.sidebar.number_input("HT Away / FT Away Odds", value=5.00, step=0.01),
}

# Functions

def calculate_margin_difference(odds, margin_target):
    return round(margin_target - odds, 2)

def poisson_prob(mean, goal):
    return (np.exp(-mean) * mean**goal) / factorial(goal)

def calculate_probabilities(home_mean, away_mean, max_goals=5):
    home_probs = [poisson_prob(home_mean, g) for g in range(max_goals + 1)]
    away_probs = [poisson_prob(away_mean, g) for g in range(max_goals + 1)]
    return home_probs, away_probs

def calculate_ht_ft_probs(home_ht, away_ht, home_ft, away_ft):
    # Halftime Poisson probabilities
    ht_probs = np.outer(
        [poisson.pmf(i, home_ht) for i in range(3)], 
        [poisson.pmf(i, away_ht) for i in range(3)]
    )

    # Fulltime Poisson probabilities
    ft_probs = np.outer(
        [poisson.pmf(i, home_ft) for i in range(6)], 
        [poisson.pmf(i, away_ft) for i in range(6)]
    )

    # HT -> FT transition probabilities
    ht_ft_probs = {
        "1/1": np.sum(np.tril(ft_probs, -1)) * 0.6,  # HT Home, FT Home
        "1/X": np.sum(np.diag(ft_probs)) * 0.4,      # HT Home, FT Draw
        "1/2": np.sum(np.triu(ft_probs, 1)) * 0.2,   # HT Home, FT Away
        "X/1": np.sum(np.tril(ft_probs, -1)) * 0.4,  # HT Draw, FT Home
        "X/X": np.sum(np.diag(ft_probs)) * 0.6,      # HT Draw, FT Draw
        "X/2": np.sum(np.triu(ft_probs, 1)) * 0.4,   # HT Draw, FT Away
        "2/1": np.sum(np.tril(ft_probs, -1)) * 0.3,  # HT Away, FT Home
        "2/X": np.sum(np.diag(ft_probs)) * 0.5,      # HT Away, FT Draw
        "2/2": np.sum(np.triu(ft_probs, 1)) * 0.7,   # HT Away, FT Away
    }

    return ht_probs, ft_probs, ht_ft_probs

def identify_value_bets(predicted_prob, bookmaker_odds, risk_factor=0.05):
    implied_prob = 1 / bookmaker_odds * 100
    margin = predicted_prob - implied_prob
    value_bet = margin > risk_factor * implied_prob
    return value_bet, margin

# Generate probabilities
home_ht_goals = goals_home_mean * 0.5
away_ht_goals = goals_away_mean * 0.5
home_ft_goals = goals_home_mean
away_ft_goals = goals_away_mean

ht_probs, ft_probs, ht_ft_probs = calculate_ht_ft_probs(home_ht_goals, away_ht_goals, home_ft_goals, away_ft_goals)

# Display HT/FT probabilities and identify value bets
st.markdown("### HT/FT Probabilities and Value Bets")
for outcome, odds in ht_ft_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100  # Convert to percentage
    is_value_bet, value_margin = identify_value_bets(predicted_prob, odds)
    st.write(f"{outcome}: {predicted_prob:.2f}% (Bookmaker Odds: {odds})")
    if is_value_bet:
        st.write(f"  🔥 **Value Bet!** Margin: {value_margin:.2f}%")

# Best bet recommendation
best_bet = max(ht_ft_odds.keys(), key=lambda x: ht_ft_probs[x] - 1 / ht_ft_odds[x])
st.write(f"\n### Best Recommended Bet: {best_bet}")
