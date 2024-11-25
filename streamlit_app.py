import streamlit as st
import numpy as np

# App title
st.title("🤖 Rabiotic Realistic Halftime/Full-time Predictor")

# Input section
st.header("Input Parameters")

# Home and Away Team
home_team = st.text_input("Home Team", "Team A")
away_team = st.text_input("Away Team", "Team B")

# Expected Goals for Home and Away
home_goals = st.number_input("Expected Goals (Home)", min_value=0.0, value=1.21)
away_goals = st.number_input("Expected Goals (Away)", min_value=0.0, value=1.64)

# Odds for the outcomes
st.subheader("Match Outcome Odds")
home_win_odds = st.number_input("Odds: Home Win", min_value=0.0, value=1.50)
draw_odds = st.number_input("Odds: Draw", min_value=0.0, value=4.00)
away_win_odds = st.number_input("Odds: Away Win", min_value=0.0, value=7.00)

# HT/FT Odds
st.subheader("Halftime/Full-time Odds")
ht_home_ft_home_odds = st.number_input("HT Home / FT Home Odds", min_value=0.0, value=2.11)
ht_home_ft_draw_odds = st.number_input("HT Home / FT Draw Odds", min_value=0.0, value=20.04)
ht_home_ft_away_odds = st.number_input("HT Home / FT Away Odds", min_value=0.0, value=50.00)

ht_draw_ft_home_odds = st.number_input("HT Draw / FT Home Odds", min_value=0.0, value=3.76)
ht_draw_ft_draw_odds = st.number_input("HT Draw / FT Draw Odds", min_value=0.0, value=5.30)
ht_draw_ft_away_odds = st.number_input("HT Draw / FT Away Odds", min_value=0.0, value=13.96)

ht_away_ft_home_odds = st.number_input("HT Away / FT Home Odds", min_value=0.0, value=29.73)
ht_away_ft_draw_odds = st.number_input("HT Away / FT Draw Odds", min_value=0.0, value=21.51)
ht_away_ft_away_odds = st.number_input("HT Away / FT Away Odds", min_value=0.0, value=12.64)

# Logic to calculate Halftime/Full-time Correct Outcome Recommendation
# Here we assume the model recommends 1/1 (Home win in both HT and FT) as the most likely outcome
recommended_ht_ft = "1/1"
recommended_odds = ht_home_ft_home_odds

# Display the recommended HT/FT outcome and its odds
st.subheader(f"Recommended Halftime/Full-time Outcome: {recommended_ht_ft}")
st.write(f"The predicted best halftime/full-time outcome is **{recommended_ht_ft}** with odds of **{recommended_odds}**.")

# Additional calculations or recommendations can go here
st.subheader("Additional Information & Insights")

# Example: Estimated probability of 1/1 based on odds
odds_to_probability = lambda odds: 1 / odds
prob_1_1 = odds_to_probability(ht_home_ft_home_odds)

st.write(f"Estimated Probability of 1/1 (HT/FT) = {prob_1_1:.2%}")

# Display some additional metrics or insights
# Example: Home Team strength and Away Team weaknesses interaction
home_attack_strength = home_goals * 1.0  # assuming strength is proportional to expected goals
away_defense_strength = away_goals * 0.8  # assuming defense strength inversely correlates with goals

st.write(f"Home Team Attack Strength (HT): {home_attack_strength:.2f}")
st.write(f"Away Team Defense Weakness (HT): {away_defense_strength:.2f}")

# Calculate expected HT/FT probabilities for 1/1
expected_home_score = home_goals * home_attack_strength / away_defense_strength
expected_away_score = away_goals * away_attack_strength / home_defense_strength

st.write(f"Expected Home Score (HT): {expected_home_score:.2f}")
st.write(f"Expected Away Score (HT): {expected_away_score:.2f}")

# Example of adjusted odds for HT/FT based on current inputs
adjusted_ht_home_ft_home_odds = ht_home_ft_home_odds * (home_attack_strength / away_defense_strength)
st.write(f"Adjusted Odds for HT Home / FT Home (adjusted): {adjusted_ht_home_ft_home_odds:.2f}")
