import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import poisson

# Title of the app
st.title("🤖Rabiotic HT/FT Correct score Predictor")

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

# Inputs for double chance odds
home_draw_odds = st.number_input("Enter Home/Draw Odds", min_value=0.0, step=0.01, value=1.5)
home_away_odds = st.number_input("Enter Home/Away Odds", min_value=0.0, step=0.01, value=1.7)
draw_away_odds = st.number_input("Enter Draw/Away Odds", min_value=0.0, step=0.01, value=1.9)

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

# Inputs for HT/FT odds
ht_home_home_odds = st.number_input("Enter HT Home/Home Odds", min_value=0.0, step=0.01, value=4.5)
ht_home_draw_odds = st.number_input("Enter HT Home/Draw Odds", min_value=0.0, step=0.01, value=4.5)
ht_home_away_odds = st.number_input("Enter HT Home/Away Odds", min_value=0.0, step=0.01, value=9.0)
ht_draw_draw_odds = st.number_input("Enter HT Home/Draw Odds", min_value=1.0, step=0.01, value=4.5)
ht_draw_home_odds = st.number_input("Enter HT Draw/Home Odds", min_value=0.0, step=0.01, value=6.0)
ht_draw_away_odds = st.number_input("Enter HT Draw/Away Odds", min_value=0.0, step=0.01, value=8.0)
ht_away_home_odds = st.number_input("Enter HT Away/Home Odds", min_value=0.0, step=0.01, value=10.0)
ht_away_draw_odds = st.number_input("Enter HT Away/Draw Odds", min_value=0.0, step=0.01, value=7.0)
ht_away_away_odds = st.number_input("Enter HT Away/Away Odds", min_value=0.0, step=0.01, value=4.5)

# Function to convert odds to probability
def odds_to_probability(odds):
    return 1 / odds

# Calculate probabilities based on HT/FT odds
ht_ft_odds = {
    "HT Home/Home": ht_home_home_odds,
    "HT Home/Draw": ht_home_draw_odds,
    "HT Home/Away": ht_home_away_odds,
    "HT Draw/Draw": ht_draw_draw_odds,
    "HT Draw/Home": ht_draw_home_odds,
    "HT Draw/Away": ht_draw_away_odds,
    "HT Away/Home": ht_away_home_odds,
    "HT Away/Draw": ht_away_draw_odds,
    "HT Away/Away": ht_away_away_odds,
}

ht_ft_probabilities = {key: odds_to_probability(odds) * 100 for key, odds in ht_ft_odds.items()}

# Function to calculate Poisson probabilities
def poisson_predict(goals_home, goals_away, lambda_home, lambda_away):
    return poisson.pmf(goals_home, lambda_home) * poisson.pmf(goals_away, lambda_away)

# You need to define home_lambda and away_lambda
home_lambda = st.number_input("Enter Home Team Expected Goals (λ)", min_value=0.0, step=0.01, value=1.5)
away_lambda = st.number_input("Enter Away Team Expected Goals (λ)", min_value=0.0, step=0.01, value=1.2)

# Generate all possible HT/FT predictions
ht_ft_predictions = []
correct_score_predictions = []
for ht_home in range(3):  # Half-time goals for home team
    for ht_away in range(3):  # Half-time goals for away team
        for ft_home in range(6):  # Full-time goals for home team
            for ft_away in range(6):  # Full-time goals for away team
                ht_prob = poisson_predict(ht_home, ht_away, home_lambda / 2, away_lambda / 2)
                ft_prob = poisson_predict(ft_home, ft_away, home_lambda, away_lambda)
                combined_prob = ht_prob * ft_prob
                ht_ft_predictions.append({
                    "HT": f"{ht_home}:{ht_away}",
                    "FT": f"{ft_home}:{ft_away}",
                    "Probability": combined_prob * 100,
                })
                if ht_home == 0 and ht_away == 0:  # Filter full-time scores only
                    correct_score_predictions.append({
                        "Scoreline": f"{ft_home}:{ft_away}",
                        "Probability": ft_prob * 100,
                    })

# Sort HT/FT predictions by probability
ht_ft_predictions = sorted(ht_ft_predictions, key=lambda x: x["Probability"], reverse=True)
correct_score_predictions = sorted(correct_score_predictions, key=lambda x: x["Probability"], reverse=True)

# Display top HT/FT predictions
st.write("### Top HT/FT Predictions:")
for i, prediction in enumerate(ht_ft_predictions[:5]):  # Display top 5 predictions
    st.write(
        f"#{i+1}: HT {prediction['HT']} - FT {prediction['FT']} "
        f"with Probability: {prediction['Probability']:.2f}%"
    )

# Display HT/FT odds-adjusted probabilities
st.write("### HT/FT Odds-Adjusted Probabilities:")
for key, value in ht_ft_probabilities.items():
    st.write(f"{key}: {value:.2f}%")

# Recommendation based on highest HT/FT probability
top_recommendation = ht_ft_predictions[0]
st.write("### HT/FT Recommendation:")
st.write(
    f"The most likely HT/FT result is **HT {top_recommendation['HT']} - FT {top_recommendation['FT']}** "
    f"with a probability of **{top_recommendation['Probability']:.2f}%**"
)

# Display top 5 correct score predictions
st.write("### Top 5 Correct Score Predictions:")
for i, prediction in enumerate(correct_score_predictions[:5]):  # Display top 5 correct scores
    st.write(
        f"#{i+1}: Scoreline {prediction['Scoreline']} "
        f"with Probability: {prediction['Probability']:.2f}%"
    )
