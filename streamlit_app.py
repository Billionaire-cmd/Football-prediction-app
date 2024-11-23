import numpy as np
import pandas as pd
from scipy.stats import poisson
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Set up the Streamlit page configuration
st.set_page_config(page_title="🤖 Rabiotic Advanced Prediction", layout="wide")

# Function to calculate halftime and full-time probabilities
def calculate_ht_ft_probs(home_ht, away_ht, home_ft, away_ft):
    # Halftime Poisson probabilities (0-2 goals assumed)
    ht_probs = np.outer(
        [poisson.pmf(i, home_ht) for i in range(3)], 
        [poisson.pmf(i, away_ht) for i in range(3)]
    )

    # Fulltime Poisson probabilities (0-5 goals assumed)
    ft_probs = np.outer(
        [poisson.pmf(i, home_ft) for i in range(6)], 
        [poisson.pmf(i, away_ft) for i in range(6)]
    )

    # HT -> FT transition probabilities
    ht_ft_probs = {
        "1/1": np.sum(np.tril(ft_probs, -1)) * 0.6,  # Halftime Home, Fulltime Home
        "1/X": np.sum(np.diag(ft_probs)) * 0.4,      # Halftime Home, Fulltime Draw
        "1/2": np.sum(np.triu(ft_probs, 1)) * 0.2,   # Halftime Home, Fulltime Away
        "X/1": np.sum(np.tril(ft_probs, -1)) * 0.4,  # Halftime Draw, Fulltime Home
        "X/X": np.sum(np.diag(ft_probs)) * 0.6,      # Halftime Draw, Fulltime Draw
        "X/2": np.sum(np.triu(ft_probs, 1)) * 0.4,   # Halftime Draw, Fulltime Away
    }

    return ht_probs, ft_probs, ht_ft_probs

# Function to calculate value bets
def identify_value_bets(predicted_prob, bookmaker_odds, risk_factor=0.05):
    implied_prob = 1 / bookmaker_odds * 100  # Calculate implied probability
    margin = predicted_prob - implied_prob
    value_bet = margin > risk_factor * implied_prob  # Only bet if margin exceeds threshold
    return value_bet, margin

# Machine Learning Model for Additional Refinement
def train_ml_model(historical_data):
    # Features: [home_attack, away_defense, home_defense, away_attack, etc.]
    X = historical_data[['home_attack', 'away_defense', 'home_defense', 'away_attack']]
    y = historical_data['outcome']  # Target: [1 for Home Win, 0 for Draw, -1 for Away Win]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

# Set up Streamlit interface
st.title("🤖 Rabiotic Advanced Prediction")

st.markdown("""
    Welcome to **Rabiotic Advanced Prediction**, the ultimate football match prediction tool.
    Here, you'll find Poisson-based predictions, value bet identification, and more.
    Adjust inputs to see real-time predictions and recommendations for your next bet.
""")

# Input parameters (can be replaced with user inputs in the Streamlit app)
home_attack = st.slider('Home Attack Strength', 0.5, 3.0, 1.8)  # Home team attack strength
away_defense = st.slider('Away Defense Strength', 0.5, 3.0, 1.3)  # Away team defensive strength
away_attack = st.slider('Away Attack Strength', 0.5, 3.0, 1.5)  # Away team attack strength
home_defense = st.slider('Home Defense Strength', 0.5, 3.0, 1.4)  # Home team defensive strength

# Calculate halftime and fulltime goals
home_ht_goals = home_attack * away_defense * 0.5  # Adjusted halftime goals
away_ht_goals = away_attack * home_defense * 0.5
home_ft_goals = home_attack * away_defense
away_ft_goals = away_attack * home_defense

# Generate probabilities
ht_probs, ft_probs, ht_ft_probs = calculate_ht_ft_probs(home_ht_goals, away_ht_goals, home_ft_goals, away_ft_goals)

# Example bookmaker odds
bookmaker_odds = {
    "1/1": 4.50,  # Odds for HT Home / FT Home
    "1/X": 5.00,  # Odds for HT Home / FT Draw
    "1/2": 15.00, # Odds for HT Home / FT Away
    "X/1": 6.00,  # Odds for HT Draw / FT Home
    "X/X": 3.50,  # Odds for HT Draw / FT Draw
    "X/2": 7.00,  # Odds for HT Draw / FT Away
}

# Display probabilities and identify value bets
st.markdown("### HT/FT Probabilities and Value Bets")
for outcome, odds in bookmaker_odds.items():
    predicted_prob = ht_ft_probs[outcome] * 100  # Convert to percentage
    is_value_bet, value_margin = identify_value_bets(predicted_prob, odds)
    st.write(f"{outcome}: {predicted_prob:.2f}% (Bookmaker Odds: {odds})")
    if is_value_bet:
        st.write(f"  🔥 **Value Bet!** Margin: {value_margin:.2f}%")

# Custom recommendation based on highest value margin
best_bet = max(bookmaker_odds.keys(), key=lambda x: ht_ft_probs[x] - 1 / bookmaker_odds[x])
st.write(f"💡 **Recommended Bet:** {best_bet} (Probability: {ht_ft_probs[best_bet]*100:.2f}%, Odds: {bookmaker_odds[best_bet]})")

# Example historical data for training the model
historical_data = {
    'home_attack': [1.8, 2.0, 1.6],
    'away_defense': [1.3, 1.4, 1.2],
    'home_defense': [1.4, 1.3, 1.6],
    'away_attack': [1.5, 1.7, 1.4],
    'outcome': [1, 0, -1]  # 1 = Home Win, 0 = Draw, -1 = Away Win
}

historical_data = pd.DataFrame(historical_data)

# Train the machine learning model
model, accuracy = train_ml_model(historical_data)

st.write(f"Model Accuracy: {accuracy * 100:.2f}%")

# Use the trained model to refine the predictions for the next match
match_features = np.array([home_attack, away_defense, home_defense, away_attack]).reshape(1, -1)
predicted_outcome = model.predict(match_features)
st.write(f"Predicted Match Outcome: {'Home Win' if predicted_outcome == 1 else 'Draw' if predicted_outcome == 0 else 'Away Win'}")
