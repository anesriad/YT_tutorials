## This section focuses on the step by step approach into turning the overall analysis done in a notebook into modularised Python files to emulate real-world scenarios


### 🗂️ explore_data.py — Data Exploration Module
This module helps you explore the StatsBomb dataset before running any specific analysis. It contains helper functions to:

- List all available competitions with their IDs and seasons
- List all teams in a selected competition + season
- List all players from a list of teams in a specific competition

These functions are useful when you want to make your analysis more flexible — allowing easy switching between tournaments, teams, and players without hardcoding any values.


### To create folders for project, type in the terminal (for this .env):

"
mkdir -p data/raw data/processed src notebooks
touch README.md
"


### 🔧 Project Structure & Setup (Modularization)
To make the project more reusable and production-friendly, we started modularizing the notebook by splitting it into Python scripts inside a src/ folder. So far, we created fetch_data.py to handle data fetching from the StatsBomb API, including functions to get competitions, matches, and filter games by teams. We also added a notebooks/ folder where we use main_script.ipynb to run the project using clean imports. To fix module import issues inside Jupyter, we added sys.path.append(...) at the top of the notebook to include the src/ folder in the Python path.

### 📥 Event Data Loading
We created a new module load_events.py to handle the loading of event-level data for selected matches and players using StatsBomb’s API. This script defines a function load_events_for_players() that takes in a list of match IDs and a list of player names (e.g. Messi, Ronaldo), fetches the event data from each match, filters for the selected players, and returns a combined DataFrame. This allows us to reuse the logic cleanly and keep the notebook focused only on analysis and visualization.

### 📊 Preprocessing & Summary Stats
We created a new module preprocess.py that handles feature selection and aggregation. It contains a function summarize_player_stats() which takes in a player’s event DataFrame and returns a dictionary of key metrics like goals, xG, passes, pressures, and more. This helps standardize how we extract meaningful stats across both players and keeps our analysis pipeline clean and reusable for other players or tournaments.

### 🎯 Visualizations (Heatmaps & Shot Maps)
We added a visualizations.py module inside src/ to keep all plotting logic separate. It includes two functions:

- plot_ball_receipt_heatmaps() for KDE heatmaps showing where each player received the ball
- plot_shot_maps() for shot locations, with xG dots and goal coloring

We used mplsoccer for a clean football pitch layout and added legends and titles for clarity. This separation helps keep the notebook focused only on analysis logic while maintaining reusable, professional visuals.


### 📈 Radar Chart (Messi vs Ronaldo)
We added a radar_chart.py module to generate a clean, normalized radar chart using Plotly. It compares key performance metrics like pass accuracy, key passes, xG per shot, shots on target %, and goals/assists per 90 minutes. The function plot_radar_chart() handles normalization internally using fixed value ranges, then displays an interactive radar chart that clearly shows each player’s strengths. This gives a quick visual summary of performance across multiple dimensions.