import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib

# Load and preprocess data
csv_file_path = os.path.join(os.path.dirname(__file__), 'team_stats_2003_2023.csv')
data = pd.read_csv(csv_file_path)

# Create new columns(features) for point and yard differences
data['points_diff'] = data['points'] - data['points_opp']
data['yards_diff'] = data['total_yards'] - data['plays_offense']

# Specify the input features and the target variable
features = ['wins', 'losses', 'points_diff', 'yards_diff', 'turnovers', 'penalties']
X = data[features]
y = data['win_loss_perc']

#Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the model and scaler
joblib.dump(model, 'nfl_model.joblib')
joblib.dump(scaler, 'nfl_scaler.joblib')

@api_view(['POST'])
def predict(request):
    home_team = request.data.get('home_team')
    away_team = request.data.get('away_team')

    # Load the model and scaler
    loaded_model = joblib.load('nfl_model.joblib')
    loaded_scaler = joblib.load('nfl_scaler.joblib')

    # Get the latest data for both teams
    home_team_data = data[data['team'] == home_team].iloc[-1]
    away_team_data = data[data['team'] == away_team].iloc[-1]

    # Prepare input data
    home_features = home_team_data[features].values
    away_features = away_team_data[features].values

    # Scale input data
    home_features_scaled = loaded_scaler.transform([home_features])
    away_features_scaled = loaded_scaler.transform([away_features])

    # Make predictions
    home_win_perc = loaded_model.predict(home_features_scaled)[0]
    away_win_perc = loaded_model.predict(away_features_scaled)[0]

    # Determine the winner
    if home_win_perc > away_win_perc:
        prediction = f"The {home_team} are more likely to win"
        win_percentage = home_win_perc
    else:
        prediction = f"The {away_team} are more likely to win"
        win_percentage = away_win_perc

    return Response({
        'prediction': prediction,
        'win_percentage': f"{win_percentage:.2%}"
    })

@api_view(['GET'])
def get_teams(request):
    teams = data['team'].unique().tolist()
    return Response(teams)
