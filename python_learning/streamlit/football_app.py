# Link to project kaggle: https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset
# link to specific dataset: https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset?select=players_22.csv

import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('players_22.csv', low_memory=False)
    
    # Keep only relevant columns
    df = df[['short_name', 'club_name', 'overall', 'value_eur', 'nationality_name',
             'player_positions', 'dribbling', 'passing', 'shooting', 'pace', 'defending']]
    
    # Drop rows missing club name or any skill attribute
    df = df.dropna(subset=['club_name', 'dribbling', 'passing', 'shooting', 'pace', 'defending'])
    
    # Convert attributes to int
    for skill in ['dribbling', 'passing', 'shooting', 'pace', 'defending']:
        df[skill] = df[skill].astype(int)

    return df

# Load it once
df = load_data()

# Sidebar skill selector
st.sidebar.title("⚙️ Customize")
selected_skill = st.sidebar.selectbox(
    "Choose a skill to rank players by:",
    ['dribbling', 'passing', 'shooting', 'pace', 'defending', 'value_eur']
)

# App Title
st.title("⚽ Top 5 Players by Skill")
st.markdown(f"Explore **FIFA 22** data and find the best players based on *{selected_skill.capitalize()}*.")

# Club selector with 'Real Madrid' selected by default (if it's in the list)
clubs = sorted(df['club_name'].unique())
default_index = clubs.index("Real Madrid CF") if "Real Madrid CF" in clubs else 0
selected_club = st.selectbox("Select a club", clubs, index=default_index)


# Filter + sort
club_df = df[df['club_name'] == selected_club]
top_players = club_df.sort_values(by=selected_skill, ascending=False).head(5)

# Show table
st.subheader(f"Top 5 in {selected_club} for {selected_skill.capitalize()}")
st.dataframe(top_players[['short_name', selected_skill, 'overall', 'player_positions']])

# Chart
st.bar_chart(top_players.set_index('short_name')[selected_skill])