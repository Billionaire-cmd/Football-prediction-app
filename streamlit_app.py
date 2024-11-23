import streamlit as st
import pandas as pd

# App Title
st.title("🤖Rabiotic HT/FT Prediction with Advanced Probabilities")

# Sidebar Inputs
st.sidebar.header("Input Parameters")
st.sidebar.subheader("Win Probabilities (%)")
home_prob = st.sidebar.number_input("Home Win Probability (%)", value=50.00)
draw_prob = st.sidebar.number_input("Draw Probability (%)", value=30.00)
away_prob = st.sidebar.number_input("Away Win Probability (%)", value=20.00)

st.sidebar.subheader("HT/FT Probabilities (%)")
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

st.sidebar.subheader("Exact Goals Probabilities (%)")
exact_goals_probs = {
    1: st.sidebar.number_input("Exact 1 Goal (%)", value=36.78),
    2: st.sidebar.number_input("Exact 2 Goals (%)", value=18.76),
    3: st.sidebar.number_input("Exact 3 Goals (%)", value=6.38),
    4: st.sidebar.number_input("Exact 4 Goals (%)", value=1.63),
    5: st.sidebar.number_input("Exact 5 Goals (%)", value=0.33),
}

# Submit Button
if st.sidebar.button("Submit Predictions"):
    st.header("Calculated Recommendations")

    # Processing: Placeholder for a Machine Learning Model
    # For now, this uses a mathematical approach to determine the most likely outcome.
    # Real-world applications can integrate ML models here.

    # Determine the most realistic HT/FT based on input probabilities
    ht_ft_df = pd.DataFrame(list(ht_ft_probs.items()), columns=["HT/FT", "Probability (%)"])
    ht_ft_df["Probability (%)"] = ht_ft_df["Probability (%)"].astype(float)
    most_likely_ht_ft = ht_ft_df.loc[ht_ft_df["Probability (%)"].idxmax()]

    # Determine the most realistic Exact Goals result
    exact_goals_df = pd.DataFrame(list(exact_goals_probs.items()), columns=["Goals", "Probability (%)"])
    exact_goals_df["Probability (%)"] = exact_goals_df["Probability (%)"].astype(float)
    most_likely_exact_goals = exact_goals_df.loc[exact_goals_df["Probability (%)"].idxmax()]

    # Determine overall most realistic outcome using a weighted approach
    overall_probabilities = {
        "Home": home_prob,
        "Draw": draw_prob,
        "Away": away_prob,
    }
    most_realistic_outcome = max(overall_probabilities, key=overall_probabilities.get)

    # Display Recommendations
    st.write("### Recommendations")
    st.write(f"**Most Realistic HT/FT Result:** {most_likely_ht_ft['HT/FT']} with a probability of {most_likely_ht_ft['Probability (%)']:.2f}%")
    st.write(f"**Most Realistic Exact Goals:** {int(most_likely_exact_goals['Goals'])} with a probability of {most_likely_exact_goals['Probability (%)']:.2f}%")
    st.write(f"**Overall Most Realistic Outcome:** {most_realistic_outcome}")

    # Winning Strategy Output
    st.success("Based on the probabilities provided, the recommended HT/FT result for victory is **{0}** with an emphasis on ensuring **{1} goals**.".format(
        most_likely_ht_ft["HT/FT"], int(most_likely_exact_goals["Goals"])
    ))
