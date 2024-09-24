import pandas as pd
import numpy as np
import os
from django.shortcuts import render
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
from django.conf import settings

# Define paths
DATA_DIR = os.path.join(settings.BASE_DIR, 'datafile')
MODEL_DIR = os.path.join(settings.BASE_DIR, 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Load and preprocess data
csv_file_path = os.path.join(DATA_DIR, 'team_stats_2003_2023.csv')
data = pd.read_csv(csv_file_path)

# Create new columns(features) for point and yard differences
data['points_diff'] = data['points'] - data['points_opp']
data['yards_diff'] = data['total_yards'] - data['plays_offense']

# Specify the input features and the target variable
features = ['wins', 'losses', 'points_diff', 'yards_diff', 'turnovers', 'penalties']
X = data[features]
y = data['win_loss_perc']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features & Fix StandardScaler feature names warning
if not hasattr(X_train, 'columns'):
    feature_names = [f'feature_{i}' for i in range(X_train.shape[1])]
else:
    feature_names = X_train.columns

scaler = StandardScaler()
scaler.fit(X_train, feature_names=feature_names)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the model and scaler
joblib.dump(model, os.path.join(MODEL_DIR, 'nfl_model.joblib'))
joblib.dump(scaler, os.path.join(MODEL_DIR, 'nfl_scaler.joblib'))

@api_view(['POST'])
def predict(request):
    try:
        home_team = request.data.get('home_team')
        away_team = request.data.get('away_team')

        # Load the model and scaler
        loaded_model = joblib.load(os.path.join(MODEL_DIR, 'nfl_model.joblib'))
        loaded_scaler = joblib.load(os.path.join(MODEL_DIR, 'nfl_scaler.joblib'))

        # Get the latest data for both teams
        home_team_data = data[data['team'] == home_team].iloc[-1]
        away_team_data = data[data['team'] == away_team].iloc[-1]

        # Prepare input data
        home_features = home_team_data[features].values
        away_features = away_team_data[features].values

        # Fix StandardScaler feature names warning
        if not hasattr(home_features, 'shape'):
            home_feature_names = [f'feature_{i}' for i in range(home_features.shape[0])]
        else:
            home_feature_names = home_features.columns

        if not hasattr(away_features, 'shape'):
            away_feature_names = [f'feature_{i}' for i in range(away_features.shape[0])]
        else:
            away_feature_names = away_features.columns

        # Scale input data
        home_features_scaled = loaded_scaler.transform([home_features], feature_names=home_feature_names)
        away_features_scaled = loaded_scaler.transform([away_features], feature_names=away_feature_names)

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
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_teams(request):
    teams = data['team'].unique().tolist()
    return Response(teams)