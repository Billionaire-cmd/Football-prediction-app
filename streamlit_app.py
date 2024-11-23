import streamlit as st
import pandas as pd
import numpy as np

# App Title
st.title("🤖 Advanced Rabiotic HT/FT Prediction App")

# Sidebar Inputs
st.sidebar.header("Input Parameters")

st.sidebar.subheader("Match Probabilities (%)")
home_prob = st.sidebar.number_input("Home Win Probability (%)", min_value=0.0, max_value=100.0, value=40.0)
draw_prob = st.sidebar.number_input("Draw Probability (%)", min_value=0.0, max_value=100.0, value=30.0)
away_prob = st.sidebar.number_input("Away Win Probability (%)", min_value=0.0, max_value=100.0, value=30.0)

st.sidebar.subheader("HT/FT Probabilities (%)")
ht_ft_probs = {}
ht_ft_keys = ["1/1", "1/X", "1/2", "X/1", "X/X", "X/2", "2/1", "2/X", "2/2"]
for key in ht_ft_keys:
    ht_ft_probs[key] = st.sidebar.number_input(f"HT/FT Probability {key} (%)", min_value=0.0, max_value=100.0, value=10.0)

st.sidebar.subheader("Exact Goals Probabilities (%)")
exact_goals_probs = []
for i in range(1, 6):
    prob = st.sidebar.number_input(f"Exact {i} Goals Probability (%)", min_value=0.0, max_value=100.0, value=10.0)
    exact_goals_probs.append(prob)

# Submit Button
if st.sidebar.button("Submit Predictions"):
    st.header("Recommended HT/FT Result")

    # Data Preparation
    ht_ft_df = pd.DataFrame({
        "HT/FT": ht_ft_keys,
        "Probability": [ht_ft_probs[key] for key in ht_ft_keys]
    })

    exact_goals_df = pd.DataFrame({
        "Goals": [1, 2, 3, 4, 5],
        "Probability": exact_goals_probs
    })

    # Normalize Probabilities
    ht_ft_df["Normalized Probability"] = ht_ft_df["Probability"] / ht_ft_df["Probability"].sum()
    exact_goals_df["Normalized Probability"] = exact_goals_df["Probability"] / exact_goals_df["Probability"].sum()

    # Machine Learning-Like Scoring (Weighted Average)
    # Weights for HT/FT and Exact Goals
    ht_ft_weight = 0.7
    goals_weight = 0.3

    # Combine probabilities
    ht_ft_df["Weighted Score"] = ht_ft_df["Normalized Probability"] * ht_ft_weight
    exact_goals_df["Weighted Score"] = exact_goals_df["Normalized Probability"] * goals_weight

    # Aggregate Results
    combined_scores = ht_ft_df.merge(
        exact_goals_df, how="outer", left_index=True, right_index=True
    ).fillna(0)
    combined_scores["Total Score"] = combined_scores["Weighted Score_x"] + combined_scores["Weighted Score_y"]

    # Recommendation
    recommended_ht_ft = ht_ft_df.loc[ht_ft_df["Normalized Probability"].idxmax(), "HT/FT"]
    recommended_ht_ft_prob = ht_ft_df.loc[ht_ft_df["Normalized Probability"].idxmax(), "Probability"]
    
    st.write("### HT/FT Recommendation")
    st.write(f"The most realistic HT/FT result is **{recommended_ht_ft}** with a probability of **{recommended_ht_ft_prob:.2f}%**.")

    # Display Probability Tables
    st.write("### HT/FT Probabilities")
    st.table(ht_ft_df)

    st.write("### Exact Goals Probabilities")
    st.table(exact_goals_df)

    st.write("### Combined Scoring (HT/FT + Goals)")
    st.table(combined_scores)

    st.write("### Note")
    st.write(
        "This recommendation is based on mathematical scoring derived from the input probabilities. "
        "For the best prediction accuracy, ensure input values are based on thorough analysis or historical data."
    )
