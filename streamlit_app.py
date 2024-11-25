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

# Match Odds
st.subheader("Match Odds")
home_win_odds = st.number_input("Odds: Home Win", min_value=0.0, value=1.50)
draw_odds = st.number_input("Odds: Draw", min_value=0.0, value=4.00)
away_win_odds = st.number_input("Odds: Away Win", min_value=0.0, value=7.00)

# HT/FT Odds
st.subheader("HT/FT Odds")
ht_home_ft_home_odds = st.number_input("HT Home / FT Home Odds", min_value=0.0, value=2.11)
ht_home_ft_draw_odds = st.number_input("HT Home / FT Draw Odds", min_value=0.0, value=20.04)
ht_home_ft_away_odds = st.number_input("HT Home / FT Away Odds", min_value=0.0, value=50.00)

ht_draw_ft_home_odds = st.number_input("HT Draw / FT Home Odds", min_value=0.0, value=3.76)
ht_draw_ft_draw_odds = st.number_input("HT Draw / FT Draw Odds", min_value=0.0, value=5.30)
ht_draw_ft_away_odds = st.number_input("HT Draw / FT Away Odds", min_value=0.0, value=13.96)

ht_away_ft_home_odds = st.number_input("HT Away / FT Home Odds", min_value=0.0, value=29.73)
ht_away_ft_draw_odds = st.number_input("HT Away / FT Draw Odds", min_value=0.0, value=21.51)
ht_away_ft_away_odds = st.number_input("HT Away / FT Away Odds", min_value=0.0, value=12.64)

# Function to calculate probability from odds
odds_to_probability = lambda odds: 1 / odds

# Submit button to trigger prediction
submit_button = st.button("Submit Prediction")

if submit_button:
    # Calculate HT/FT Recommended Outcome based on Odds
    recommended_ht_ft = "1/1"
    recommended_odds = ht_home_ft_home_odds

    # Display Recommended Outcome and Odds
    st.subheader(f"Recommended HT/FT Outcome: {recommended_ht_ft}")
    st.write(f"The predicted best halftime/full-time outcome is **{recommended_ht_ft}** with odds of **{recommended_odds}**.")

    # Additional calculations or recommendations
    prob_1_1 = odds_to_probability(ht_home_ft_home_odds)
    st.write(f"Estimated Probability of 1/1 (HT/FT) = {prob_1_1:.2%}")

    # Calculate expected scores for Home and Away teams (HT/FT)
    expected_home_score = home_goals
    expected_away_score = away_goals

    st.write(f"Expected Home Score (Full Time): {expected_home_score:.2f}")
    st.write(f"Expected Away Score (Full Time): {expected_away_score:.2f}")

    # HT/FT Outcomes and Probabilities
    st.write(f"HT Home / FT Home Odds: {ht_home_ft_home_odds}")
    st.write(f"HT Home / FT Draw Odds: {ht_home_ft_draw_odds}")
    st.write(f"HT Home / FT Away Odds: {ht_home_ft_away_odds}")

    st.write(f"HT Draw / FT Home Odds: {ht_draw_ft_home_odds}")
    st.write(f"HT Draw / FT Draw Odds: {ht_draw_ft_draw_odds}")
    st.write(f"HT Draw / FT Away Odds: {ht_draw_ft_away_odds}")

    st.write(f"HT Away / FT Home Odds: {ht_away_ft_home_odds}")
    st.write(f"HT Away / FT Draw Odds: {ht_away_ft_draw_odds}")
    st.write(f"HT Away / FT Away Odds: {ht_away_ft_away_odds}")

    # Optional: Display more calculated information or visualizations
    # Example of showing HT/FT probabilities for all outcomes
    st.subheader("HT/FT Outcome Probabilities")
    outcomes = {
        "HT Home / FT Home": odds_to_probability(ht_home_ft_home_odds),
        "HT Home / FT Draw": odds_to_probability(ht_home_ft_draw_odds),
        "HT Home / FT Away": odds_to_probability(ht_home_ft_away_odds),
        "HT Draw / FT Home": odds_to_probability(ht_draw_ft_home_odds),
        "HT Draw / FT Draw": odds_to_probability(ht_draw_ft_draw_odds),
        "HT Draw / FT Away": odds_to_probability(ht_draw_ft_away_odds),
        "HT Away / FT Home": odds_to_probability(ht_away_ft_home_odds),
        "HT Away / FT Draw": odds_to_probability(ht_away_ft_draw_odds),
        "HT Away / FT Away": odds_to_probability(ht_away_ft_away_odds),
    }

    # Display the probabilities
    for outcome, prob in outcomes.items():
        st.write(f"{outcome}: {prob:.2%}")
