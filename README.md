# NFL Game Predictor

This project is a web application that predicts the outcome of NFL games using machine learning techniques. It consists of a Django backend for data processing and predictions, and a React frontend for user interaction.

## Features

- Predicts the outcome of NFL games based on team statistics
- Allows users to select home and away teams for prediction
- Displays win probabilities for selected teams
- Uses a Random Forest Regressor model for predictions

## Technology Stack

- Backend: Django, Django Rest Framework, Scikit-learn
- Frontend: React, Axios
- Data: CSV file containing NFL team statistics from 2003 to 2023

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- Node.js 14+
- pip and npm package managers

## Installation

### Backend Setup

1. Clone the repository:

   ```
   git clone <your-repository-url>
   cd nfl-predictor
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

4. Navigate to the Django project directory and run migrations:

   ```
   cd backend
   python manage.py migrate
   ```

5. Start the Django development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the React app directory:

   ```
   cd frontend
   ```

2. Install the required npm packages:

   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

## Usage

1. Open your web browser and go to `http://localhost:3000` to access the React frontend.
2. Select a home team and an away team from the dropdown menus.
3. Click the "Predict" button to see the prediction results.
4. The application will display the predicted winner and the win percentage.

## API Endpoints

- `GET /api/teams/`: Returns a list of all NFL teams
- `POST /api/predict/`: Accepts home and away team names and returns a prediction

## Data

The project uses NFL team statistics from 2003 to 2023, stored in a CSV file.
