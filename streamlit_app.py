import streamlit as st
import numpy as np

# App Title
st.title("🤖 Rabiotic Advanced HT/FT Prediction Pro")

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

if st.sidebar.button("Submit Prediction"):
    st.header("Predicted Outcomes and Recommendations")

    # Convert input probabilities to normalized values
    total_ht_ft = sum(ht_ft_probs.values())
    normalized_ht_ft = {k: v / total_ht_ft for k, v in ht_ft_probs.items()}

    # Convert exact goals probabilities to normalized values
    total_exact_goals = sum(exact_goals_probs.values())
    normalized_exact_goals = {k: v / total_exact_goals for k, v in exact_goals_probs.items()}

    # Mock Machine Learning Calculation for HT/FT Recommendation
    # This is a placeholder for an advanced model that uses inputs to predict outcomes
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
    
    st.write("### HT/FT Probabilities")
    for key, value in ht_ft_probs.items():
        st.write(f"{key}: {value:.2f}%")

    st.write("### Exact Goals Probabilities")
    for key, value in exact_goals_probs.items():
        st.write(f"Exact {key} Goals: {value:.2f}%")

    st.write("### Recommendations")
    st.write(f"**Most Realistic HT/FT Result:** {recommended_ht_ft}")
    st.write(f"**Most Likely Exact Goals:** {recommended_exact_goals}")

    st.write("### Prediction Summary")
    st.write(f"Based on the inputs, the most realistic outcome is an HT/FT result of **{recommended_ht_ft}** "
             f"and an exact goal count of **{recommended_exact_goals} goals**.")
