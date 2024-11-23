import streamlit as st
import numpy as np

# App Title
st.title("🤖 Rabiotic Strategic HT/FT Prediction Focus")

# Sidebar Inputs
st.sidebar.header("Input Probabilities")
st.sidebar.subheader("Match Outcome Probabilities")
home_prob = st.sidebar.number_input("Home Win Probability (%)", value=50.00, min_value=0.0, max_value=100.0)
draw_prob = st.sidebar.number_input("Draw Probability (%)", value=30.00, min_value=0.0, max_value=100.0)
away_prob = st.sidebar.number_input("Away Win Probability (%)", value=20.00, min_value=0.0, max_value=100.0)

st.sidebar.subheader("HT/FT Probabilities")
ht_ft_probs = {
    "1/1": st.sidebar.number_input("1/1 (%)", value=40.00),
    "1/X": st.sidebar.number_input("1/X (%)", value=5.00),
    "1/2": st.sidebar.number_input("1/2 (%)", value=2.00),
    "X/1": st.sidebar.number_input("X/1 (%)", value=15.00),
    "X/X": st.sidebar.number_input("X/X (%)", value=20.00),
    "X/2": st.sidebar.number_input("X/2 (%)", value=8.00),
    "2/1": st.sidebar.number_input("2/1 (%)", value=4.00),
    "2/X": st.sidebar.number_input("2/X (%)", value=3.00),
    "2/2": st.sidebar.number_input("2/2 (%)", value=3.00),
}

st.sidebar.subheader("Exact Goals Probabilities")
exact_goals_probs = {
    1: st.sidebar.number_input("Exact 1 Goal Probability (%)", value=36.78),
    2: st.sidebar.number_input("Exact 2 Goals Probability (%)", value=18.76),
    3: st.sidebar.number_input("Exact 3 Goals Probability (%)", value=6.38),
    4: st.sidebar.number_input("Exact 4 Goals Probability (%)", value=1.63),
    5: st.sidebar.number_input("Exact 5 Goals Probability (%)", value=0.33),
}

st.sidebar.subheader("Over/Under and BTTS Probabilities")
over_2_5_prob = st.sidebar.number_input("Over 2.5 Probability (%)", value=15.26)
under_2_5_prob = st.sidebar.number_input("Under 2.5 Probability (%)", value=84.74)
btts_yes_prob = st.sidebar.number_input("BTTS (Yes) Probability (%)", value=90.65)
btts_no_prob = st.sidebar.number_input("BTTS (No) Probability (%)", value=9.35)

if st.sidebar.button("Submit Prediction"):
    st.header("Predicted Outcomes and Recommendations")

    # Normalize HT/FT probabilities
    total_ht_ft = sum(ht_ft_probs.values())
    normalized_ht_ft = {k: v / total_ht_ft for k, v in ht_ft_probs.items()}

    # Normalize exact goals probabilities
    total_exact_goals = sum(exact_goals_probs.values())
    normalized_exact_goals = {k: v / total_exact_goals for k, v in exact_goals_probs.items()}

    # Define a scoring function for a 1-1 result
    def calculate_1_1_score(normalized_ht_ft, normalized_exact_goals):
        # Prioritize X/X HT/FT and exact goals for 1-1
        ht_ft_score = normalized_ht_ft.get("X/X", 0) + 0.5 * (
            normalized_ht_ft.get("1/X", 0) + normalized_ht_ft.get("X/1", 0)
        )
        exact_goal_score = normalized_exact_goals.get(1, 0) ** 2  # Both teams scoring 1 goal
        # Combine scores strategically
        combined_score = ht_ft_score * exact_goal_score
        return combined_score

    # Calculate likelihood of a 1-1 score
    score_1_1 = calculate_1_1_score(normalized_ht_ft, normalized_exact_goals)

    # Get the most likely HT/FT result and exact goals as a backup
    def recommend_ht_ft(normalized_ht_ft):
        return max(normalized_ht_ft, key=normalized_ht_ft.get)

    def recommend_exact_goals(normalized_exact_goals):
        return max(normalized_exact_goals, key=normalized_exact_goals.get)

    recommended_ht_ft = recommend_ht_ft(normalized_ht_ft)
    recommended_exact_goals = recommend_exact_goals(normalized_exact_goals)

    # Output
    st.write("### Probabilities Overview")
    st.write(f"Home Win Probability: {home_prob:.2f}%")
    st.write(f"Draw Probability: {draw_prob:.2f}%")
    st.write(f"Away Win Probability: {away_prob:.2f}%")
    st.write(f"Over 2.5 Probability: {over_2_5_prob:.2f}%")
    st.write(f"Under 2.5 Probability: {under_2_5_prob:.2f}%")
    st.write(f"BTTS (Yes) Probability: {btts_yes_prob:.2f}%")
    st.write(f"BTTS (No) Probability: {btts_no_prob:.2f}%")

    st.write("### HT/FT Probabilities")
    for key, value in ht_ft_probs.items():
        st.write(f"{key}: {value:.2f}%")

    st.write("### Exact Goals Probabilities")
    for key, value in exact_goals_probs.items():
        st.write(f"Exact {key} Goals: {value:.2f}%")

    st.write("### Recommendations")
    st.write(f"**1-1 Score Strategic Likelihood Score:** {score_1_1:.4f}")
    st.write(f"**Most Realistic HT/FT Result:** {recommended_ht_ft}")
    st.write(f"**Most Likely Exact Goals:** {recommended_exact_goals}")

    st.write("### Prediction Summary")
    st.write(
        f"Based on the inputs, the strategic calculation highlights a **1-1 draw (HT: 1-1, FT: 1-1)** "
        f"with the HT/FT recommendation of **X/X**, "
        f"indicating both teams scoring and staying equal throughout the match."
    )
