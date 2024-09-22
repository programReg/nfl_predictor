import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import logo from "./img/logo.png";

function App() {
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState("");
  const [winPercentage, setWinPercentage] = useState("");
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    // Fetch the list of teams when the component mounts (.. when this section of the page loads up for the first time)
    axios
      .get("https://nfl-predictor.onrender.com/api/teams/")
      .then((response) => setTeams(response.data))
      .catch((error) => console.error("Error fetching teams:", error));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "https://nfl-predictor.onrender.com/api/predict/",
        {
          home_team: homeTeam,
          away_team: awayTeam,
        }
      );
      setPrediction(response.data.prediction);
      setWinPercentage(response.data.win_percentage);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <img src={logo} alt="Logo" className="logo" />
      <h1>NFL Game Predictor</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="home-team">Home Team: </label>
          <select
            id="home-team"
            value={homeTeam}
            onChange={(e) => setHomeTeam(e.target.value)}
            required
          >
            <option value="">Select Home Team</option>
            {teams.map((team) => (
              <option key={`home-${team}`} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>
        <div className="away-label">
          <label htmlFor="away-team">Away Team: </label>
          <select
            id="away-team"
            value={awayTeam}
            onChange={(e) => setAwayTeam(e.target.value)}
            required
          >
            <option value="">Select Away Team</option>
            {teams.map((team) => (
              <option key={`away-${team}`} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>
        <button className="button" type="submit">
          Predict
        </button>
      </form>
      {prediction && (
        <div>
          <p>Prediction: {prediction}</p>
          <p>Win Percentage: {winPercentage}</p>
        </div>
      )}
    </div>
  );
}

export default App;
