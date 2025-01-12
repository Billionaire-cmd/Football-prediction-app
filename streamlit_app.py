import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Function to calculate the probability of a specific score using Poisson distribution
def poisson_predict(home_goals, away_goals, home_lambda, away_lambda):
    home_prob = poisson.pmf(home_goals, home_lambda)
    away_prob = poisson.pmf(away_goals, away_lambda)
    return home_prob * away_prob

# Function to calculate probabilities from odds
def predict_outcome(home_odds, draw_odds, away_odds):
    home_prob = 1 / home_odds
    draw_prob = 1 / draw_odds
    away_prob = 1 / away_odds
    total = home_prob + draw_prob + away_prob
    return {
        "Home Win Probability": (home_prob / total) * 100,
        "Draw Probability": (draw_prob / total) * 100,
        "Away Win Probability": (away_prob / total) * 100,
    }

# Function to calculate double chance probabilities
def predict_double_chance(home_draw_odds, home_away_odds, draw_away_odds):
    home_draw_prob = 1 / home_draw_odds
    home_away_prob = 1 / home_away_odds
    draw_away_prob = 1 / draw_away_odds
    total = home_draw_prob + home_away_prob + draw_away_prob
    return {
        "Home/Draw Probability": (home_draw_prob / total) * 100,
        "Home/Away Probability": (home_away_prob / total) * 100,
        "Draw/Away Probability": (draw_away_prob / total) * 100,
    }

# Function to calculate over/under probabilities
def predict_over_under(over_1_5_odds, under_1_5_odds, over_2_5_odds, under_2_5_odds):
    over_1_5_prob = 1 / over_1_5_odds
    under_1_5_prob = 1 / under_1_5_odds
    over_2_5_prob = 1 / over_2_5_odds
    under_2_5_prob = 1 / under_2_5_odds
    total_1_5 = over_1_5_prob + under_1_5_prob
    total_2_5 = over_2_5_prob + under_2_5_prob
    return {
        "Over 1.5 Probability": (over_1_5_prob / total_1_5) * 100,
        "Under 1.5 Probability": (under_1_5_prob / total_1_5) * 100,
        "Over 2.5 Probability": (over_2_5_prob / total_2_5) * 100,
        "Under 2.5 Probability": (under_2_5_prob / total_2_5) * 100,
    }

# Streamlit app setup
st.title("🤖Rabiotic HT/FT Correct score Predictor")

# Inputs for Team A and Team B
team_a = st.text_input("Enter Team A Name", "Team A")
team_b = st.text_input("Enter Team B Name", "Team B")

# Inputs for average goals and win percentage
team_a_avg_goals = st.number_input(f"Enter {team_a} Average Goals", min_value=0.0, step=0.1, value=1.3)
team_a_win_percentage = st.number_input(f"Enter {team_a} Win Percentage (as decimal, e.g., 0.73 for 73%)", min_value=0.0, max_value=1.0, step=0.01, value=0.73)
team_b_avg_goals = st.number_input(f"Enter {team_b} Average Goals", min_value=0.0, step=0.1, value=1.7)
team_b_win_percentage = st.number_input(f"Enter {team_b} Win Percentage (as decimal, e.g., 0.80 for 80%)", min_value=0.0, max_value=1.0, step=0.01, value=0.80)

# Inputs for match odds
home_odds = st.number_input("Enter Home Win Odds", min_value=1.0, step=0.01, value=2.5)
draw_odds = st.number_input("Enter Draw Odds", min_value=1.0, step=0.01, value=3.2)
away_odds = st.number_input("Enter Away Win Odds", min_value=1.0, step=0.01, value=3.0)

# Inputs for double chance odds
home_draw_odds = st.number_input("Enter Home/Draw Odds", min_value=1.0, step=0.01, value=1.5)
home_away_odds = st.number_input("Enter Home/Away Odds", min_value=1.0, step=0.01, value=1.7)
draw_away_odds = st.number_input("Enter Draw/Away Odds", min_value=1.0, step=0.01, value=1.9)

# Inputs for Over/Under odds
over_1_5_odds = st.number_input("Enter Over 1.5 Odds", min_value=1.0, step=0.01, value=1.4)
under_1_5_odds = st.number_input("Enter Under 1.5 Odds", min_value=1.0, step=0.01, value=2.9)
over_2_5_odds = st.number_input("Enter Over 2.5 Odds", min_value=1.0, step=0.01, value=1.9)
under_2_5_odds = st.number_input("Enter Under 2.5 Odds", min_value=1.0, step=0.01, value=2.1)

# Prediction button
if st.button("Predict Match Outcome"):
    # Calculate Poisson lambda values
    home_lambda = team_a_avg_goals
    away_lambda = team_b_avg_goals

    # Generate all possible HT/FT predictions
    ht_ft_predictions = []
    for ht_home in range(3):  # Half-time goals for home team
        for ht_away in range(3):  # Half-time goals for away team
            for ft_home in range(ht_home, ht_home + 3):  # Full-time goals for home team
                for ft_away in range(ht_away, ht_away + 3):  # Full-time goals for away team
                    ht_prob = poisson_predict(ht_home, ht_away, home_lambda / 2, away_lambda / 2)
                    ft_prob = poisson_predict(ft_home, ft_away, home_lambda, away_lambda)
                    combined_prob = ht_prob * ft_prob
                    ht_ft_predictions.append({
                        "HT": f"{ht_home}:{ht_away}",
                        "FT": f"{ft_home}:{ft_away}",
                        "Probability": combined_prob * 100,
                    })

    # Sort HT/FT predictions by probability
    ht_ft_predictions = sorted(ht_ft_predictions, key=lambda x: x["Probability"], reverse=True)

    # Display top HT/FT predictions
    st.write("### Top HT/FT Predictions:")
    for i, prediction in enumerate(ht_ft_predictions[:5]):  # Display top 5 predictions
        st.write(
            f"#{i+1}: HT {prediction['HT']} - FT {prediction['FT']} "
            f"with Probability: {prediction['Probability']:.2f}%"
        )

    # Recommendation based on highest HT/FT probability
    top_recommendation = ht_ft_predictions[0]
    st.write("### Recommendation:")
    st.write(
        f"The most likely HT/FT result is **HT {top_recommendation['HT']} - FT {top_recommendation['FT']}** "
        f"with a probability of **{top_recommendation['Probability']:.2f}%**."
    )

    # Optional: Plotting probabilities
    fig, ax = plt.subplots(figsize=(10, 6))
    top_scores = [f"HT {x['HT']} - FT {x['FT']}" for x in ht_ft_predictions[:5]]
    top_probs = [x["Probability"] for x in ht_ft_predictions[:5]]
    ax.bar(top_scores, top_probs, color="skyblue")
    ax.set_title("Top HT/FT Predictions")
    ax.set_ylabel("Probability (%)")
    ax.set_xlabel("HT/FT Scoreline")
    plt.xticks(rotation=45)
    st.pyplot(fig)
