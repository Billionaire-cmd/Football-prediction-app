import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Define functions for Poisson distribution, machine learning model, etc.

def poisson_predict(home_goals, away_goals, home_lambda, away_lambda):
    """
    Predict the probability of a specific score using Poisson distribution.
    """
    home_prob = poisson.pmf(home_goals, home_lambda)
    away_prob = poisson.pmf(away_goals, away_lambda)
    return home_prob * away_prob

def regression_model(team_a_stats, team_b_stats):
    """
    Simple placeholder function for regression or ML model prediction.
    You can replace this with any model you want to use.
    """
    # Example: Simple linear regression (can be expanded with better models)
    X = np.array([team_a_stats, team_b_stats]).reshape(-1, 1)
    y = np.array([1])  # Placeholder, needs actual results
    model = LinearRegression().fit(X, y)
    return model.predict(X)

def predict_outcome(home_odds, draw_odds, away_odds):
    """
    Calculate outcome probabilities based on the odds and historical analysis.
    """
    home_prob = 1 / home_odds
    draw_prob = 1 / draw_odds
    away_prob = 1 / away_odds
    total = home_prob + draw_prob + away_prob
    return {
        "Home Win Probability": home_prob / total,
        "Draw Probability": draw_prob / total,
        "Away Win Probability": away_prob / total
    }

# Set up the Streamlit UI

st.title('🤖💯Rabiotic Instant Virtuals Football Match Prediction App')

# User inputs for Team A and Team B
team_a = st.text_input("Enter Team A Name")
team_b = st.text_input("Enter Team B Name")

# User inputs for Double Chance odds
home_odds = st.number_input("Enter Home Win Odds", min_value=1.0, step=0.01)
draw_odds = st.number_input("Enter Draw Odds", min_value=1.0, step=0.01)
away_odds = st.number_input("Enter Away Win Odds", min_value=1.0, step=0.01)

# Prediction button
if st.button("Predict Match Outcome"):
    # Placeholder: Use real statistics for these values
    team_a_stats = {
        "average_goals": 1.3,
        "win_percentage": 0.73,
    }
    team_b_stats = {
        "average_goals": 1.7,
        "win_percentage": 0.80,
    }
    
    # Poisson model prediction for HT/FT scores
    home_lambda = team_a_stats["average_goals"]
    away_lambda = team_b_stats["average_goals"]

    predicted_outcome = predict_outcome(home_odds, draw_odds, away_odds)

    st.write("Predicted Outcome Probabilities:")
    st.write(f"Home Win Probability: {predicted_outcome['Home Win Probability']:.2f}")
    st.write(f"Draw Probability: {predicted_outcome['Draw Probability']:.2f}")
    st.write(f"Away Win Probability: {predicted_outcome['Away Win Probability']:.2f}")

    # Calculate Poisson probabilities for HT and FT scores
    ht_predictions = []
    for i in range(4):  # Home team goals range (0-3)
        for j in range(4):  # Away team goals range (0-3)
            ht_prob = poisson_predict(i, j, home_lambda, away_lambda)
            ht_predictions.append((i, j, ht_prob))

    # Display HT/FT predictions
    st.write("HT/FT Predictions (Goals by Home - Goals by Away):")
    for ht_pred in ht_predictions:
        st.write(f"HT {ht_pred[0]} - FT {ht_pred[1]} with Probability: {ht_pred[2]:.5f}")

    # Optional: Plotting (can be expanded for better visualizations)
    fig, ax = plt.subplots()
    ax.bar([f"HT {x[0]} - FT {x[1]}" for x in ht_predictions], [x[2] for x in ht_predictions])
    ax.set_title("HT/FT Predictions")
    ax.set_xticklabels([f"HT {x[0]} - FT {x[1]}" for x in ht_predictions], rotation=45)
    st.pyplot(fig)

