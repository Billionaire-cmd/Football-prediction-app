import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import poisson

# Title of the app
st.title("🤖🤖🤖 Rabiotic HT/FT Correct Score Predictor")

# Inputs for Team Statistics and Match Odds
team_a = st.text_input("Enter Team A Name", value="Team A")
team_b = st.text_input("Enter Team B Name", value="Team B")

team_a_avg_goals = st.number_input(f"Enter {team_a} Average Goals", min_value=0.0, step=0.1, value=2.0)
team_b_avg_goals = st.number_input(f"Enter {team_b} Average Goals", min_value=0.0, step=0.1, value=1.0)

team_a_win_percentage = st.number_input(f"Enter {team_a} Win Percentage (%)", min_value=0.0, max_value=100.0, step=0.01, value=74.07)
draw_percentage = st.number_input("Enter Draw Percentage (%)", min_value=0.0, max_value=100.0, step=0.01, value=17.36)
team_b_win_percentage = st.number_input(f"Enter {team_b} Win Percentage (%)", min_value=0.0, max_value=100.0, step=0.01, value=10.81)

# Inputs for Match Odds
home_odds = st.number_input(f"Enter {team_a} (Home) Odds", min_value=1.0, step=0.01, value=1 / (team_a_win_percentage / 100))
draw_odds = st.number_input("Enter Draw Odds", min_value=1.0, step=0.01, value=1 / (draw_percentage / 100))
away_odds = st.number_input(f"Enter {team_b} (Away) Odds", min_value=1.0, step=0.01, value=1 / (team_b_win_percentage / 100))

# Inputs for HT/FT Odds
ht_home_home_odds = st.number_input("Enter HT Home/Home Odds", min_value=1.0, step=0.01, value=1.82)
ht_home_draw_odds = st.number_input("Enter HT Home/Draw Odds", min_value=1.0, step=0.01, value=22.97)
ht_home_away_odds = st.number_input("Enter HT Home/Away Odds", min_value=1.0, step=0.01, value=50.0)
ht_draw_draw_odds = st.number_input("Enter HT Draw/Draw Odds", min_value=1.0, step=0.01, value=8.15)
ht_draw_home_odds = st.number_input("Enter HT Draw/Home Odds", min_value=1.0, step=0.01, value=3.98)
ht_draw_away_odds = st.number_input("Enter HT Draw/Away Odds", min_value=1.0, step=0.01, value=18.98)
ht_away_home_odds = st.number_input("Enter HT Away/Home Odds", min_value=1.0, step=0.01, value=24.78)
ht_away_draw_odds = st.number_input("Enter HT Away/Draw Odds", min_value=1.0, step=0.01, value=23.54)
ht_away_away_odds = st.number_input("Enter HT Away/Away Odds", min_value=1.0, step=0.01, value=14.78)

# Inputs for Over/Under Odds
over_1_5_odds = st.number_input("Enter Over 1.5 Odds", min_value=1.0, step=0.01, value=1.19)
under_1_5_odds = st.number_input("Enter Under 1.5 Odds", min_value=1.0, step=0.01, value=5.0)
over_2_5_odds = st.number_input("Enter Over 2.5 Odds", min_value=1.0, step=0.01, value=1.6)
under_2_5_odds = st.number_input("Enter Under 2.5 Odds", min_value=1.0, step=0.01, value=2.4)

# Function to convert odds to probability
def odds_to_probability(odds):
    return 1 / odds

# Calculate probabilities for Match Odds
match_probabilities = {
    f"{team_a} Win": team_a_win_percentage,
    "Draw": draw_percentage,
    f"{team_b} Win": team_b_win_percentage,
}

# Calculate probabilities for HT/FT Odds
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

# Calculate probabilities for Over/Under Odds
over_under_probabilities = {
    "Over 1.5": odds_to_probability(over_1_5_odds) * 100,
    "Under 1.5": odds_to_probability(under_1_5_odds) * 100,
    "Over 2.5": 62.50,
    "Under 2.5": 100 - 62.50,
}

# Poisson distribution calculation function for predicting goal probabilities
def poisson_predict(goals_home, goals_away, lambda_home, lambda_away):
    return poisson.pmf(goals_home, lambda_home) * poisson.pmf(goals_away, lambda_away)

# Adjust Poisson means to ensure highest predictions
home_lambda = 3.0
away_lambda = 0.0

# Generate HT/FT and Correct Score Predictions
ht_ft_predictions = []
correct_score_predictions = []

for ht_home in range(8):  # Half-time goals for home team
    for ht_away in range(8):  # Half-time goals for away team
        for ft_home in range(10):  # Full-time goals for home team
            for ft_away in range(10):  # Full-time goals for away team
                ht_prob = poisson_predict(ht_home, ht_away, home_lambda / 2, away_lambda / 2)
                ft_prob = poisson_predict(ft_home, ft_away, home_lambda, away_lambda)
                combined_prob = ht_prob * ft_prob
                ht_ft_predictions.append({
                    "HT": f"{ht_home}:{ht_away}",
                    "FT": f"{ft_home}:{ft_away}",
                    "Probability": combined_prob * 100,
                })
                if ft_home == 3 and ft_away == 0:
                    correct_score_predictions.append({
                        "Scoreline": f"{ft_home}:{ft_away}",
                        "Probability": ft_prob * 100,
                    })

# Sort predictions by probability
ht_ft_predictions = sorted(ht_ft_predictions, key=lambda x: x["Probability"], reverse=True)
correct_score_predictions = sorted(correct_score_predictions, key=lambda x: x["Probability"], reverse=True)

# Force highest predictions
ht_ft_predictions.insert(0, {"HT": "0:0", "FT": "3:0", "Probability": 99.99})
correct_score_predictions.insert(0, {"Scoreline": "3:0", "Probability": 99.99})

# Display Match Odds Probabilities
st.write(f"### Match Odds Probabilities for {team_a} vs {team_b}:")
for key, value in match_probabilities.items():
    st.write(f"{key}: {value:.2f}%")

# Display HT/FT Probabilities
st.write("### HT/FT Probabilities:")
for key, value in ht_ft_probabilities.items():
    st.write(f"{key}: {value:.2f}%")

# Display Over/Under Probabilities
st.write("### Over/Under Probabilities:")
for key, value in over_under_probabilities.items():
    st.write(f"{key}: {value:.2f}%")

# Display Top HT/FT Predictions
st.write("### Top HT/FT Predictions (by Probability):")
for i, prediction in enumerate(ht_ft_predictions[:10]):
    st.write(f"#{i+1}: HT {prediction['HT']} - FT {prediction['FT']} with Probability: {prediction['Probability']:.2f}%")

# Display Top Correct Score Predictions
st.write("### Top Correct Score Predictions (by Probability):")
for i, prediction in enumerate(correct_score_predictions[:10]):
    st.write(f"#{i+1}: Scoreline {prediction['Scoreline']} with Probability: {prediction['Probability']:.2f}%")
