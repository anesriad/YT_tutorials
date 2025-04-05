import streamlit as st
import numpy as np
from src.fetch_data import get_competitions, get_matches, filter_matches_by_teams
from src.load_events import load_events_for_players
from src.visualizations import (
    plot_ball_receipt_heatmaps,
    plot_shot_maps,
    plot_key_pass_arrows  # Key pass arrows for each player
)
from src.radar_chart import plot_radar_chart
from src.preprocess import summarize_player_stats  # Summaries for radar

st.set_page_config(page_title="Player Comparison Tool", layout="wide")
st.title("Player Comparison Tool - World Cup Edition")

# ---------------------------
# 1. Select Competition
# ---------------------------
st.sidebar.header("1. Select Competition")
competitions = get_competitions()
competition_options = [
    f"{row['competition_name']} ({row['season_name']})"
    for _, row in competitions.iterrows()
]
selected_competition = st.sidebar.selectbox("Competition", competition_options)

# Identify comp/season
comp_row = competitions.iloc[competition_options.index(selected_competition)]
competition_id = comp_row["competition_id"]
season_id = comp_row["season_id"]

@st.cache_data(show_spinner=True)
def load_teams(competition_id, season_id):
    """Fetch all teams from selected competition + season."""
    matches_df = get_matches(competition_id, season_id)
    home_teams = matches_df["home_team"].unique().tolist()
    away_teams = matches_df["away_team"].unique().tolist()
    teams = sorted(list(set(home_teams + away_teams)))
    return teams, matches_df

teams, matches_df = load_teams(competition_id, season_id)

# ---------------------------
# 2. Select Teams
# ---------------------------
st.sidebar.header("2. Select Teams")
team1 = st.sidebar.selectbox("Team 1", teams, index=0)
teaminx = teams.index(team1)
team2 = st.sidebar.selectbox("Team 2", teams, index=teaminx + 1 if teaminx + 1 < len(teams) else 0)

# ---------------------------
# 3. Load Data Button
# ---------------------------
if "players" not in st.session_state:
    st.session_state["players"] = []
if "events_df_all" not in st.session_state:
    st.session_state["events_df_all"] = None

load_data_button = st.sidebar.button("Load Data")

if load_data_button:
    # Filter matches for the two chosen teams, gather match_ids
    filtered_matches = filter_matches_by_teams(matches_df, [team1, team2])
    match_ids = filtered_matches["match_id"].tolist()

    @st.cache_data(show_spinner=True)
    def get_available_players(match_ids, team1, team2):
        """Load all events for those matches, filter by the two teams."""
        try:
            all_events = load_events_for_players(match_ids, [])  # load events for all players
            filtered_players = all_events[all_events["team"].isin([team1, team2])]
            return sorted(filtered_players["player"].dropna().unique().tolist()), all_events
        except Exception:
            return [], None

    players, events_df_all = get_available_players(match_ids, team1, team2)
    st.session_state["players"] = players
    st.session_state["events_df_all"] = events_df_all

# ---------------------------
# 4. Player Selection & Plot
# ---------------------------
if st.session_state["players"] and st.session_state["events_df_all"] is not None:
    st.sidebar.header("3. Select Players")
    player1 = st.sidebar.selectbox("Player 1", st.session_state["players"], index=0)
    player2 = st.sidebar.selectbox(
        "Player 2",
        st.session_state["players"],
        index=1 if len(st.session_state["players"]) > 1 else 0,
    )

    plot_button = st.sidebar.button("Plot")

    if plot_button and player1 and player2:
        st.subheader(f"Comparison: {player1} vs {player2}")

        events_df_all = st.session_state["events_df_all"]
        # Filter only these two players' events
        events_df = events_df_all[events_df_all["player"].isin([player1, player2])]

        st.write(events_df.head())

        # ---------------------------
        # BALL RECEIPT HEATMAPS
        # ---------------------------
        p1_locs = np.array([
            loc for loc in events_df[events_df["player"] == player1]["location"].dropna().tolist()
            if isinstance(loc, list) and len(loc) == 2
        ])
        p2_locs = np.array([
            loc for loc in events_df[events_df["player"] == player2]["location"].dropna().tolist()
            if isinstance(loc, list) and len(loc) == 2
        ])

        if len(p1_locs) > 0 and len(p2_locs) > 0:
            st.markdown("### Ball Receipt Heatmaps")
            fig_heat = plot_ball_receipt_heatmaps(p1_locs, p2_locs)
            st.pyplot(fig_heat)

        # ---------------------------
        # SHOT MAPS
        # ---------------------------
        st.markdown("### Shot Maps")
        p1_df = events_df[events_df["player"] == player1]
        p2_df = events_df[events_df["player"] == player2]
        fig_shots = plot_shot_maps(p1_df, p2_df)
        st.pyplot(fig_shots)

        # ---------------------------
        # KEY PASS ARROWS
        # ---------------------------
        st.markdown("### Key Passes")
        fig_kp = plot_key_pass_arrows(p1_df, p2_df)
        st.pyplot(fig_kp)

        # ---------------------------
        # RADAR CHART
        # ---------------------------
        st.markdown("### Radar Chart")

        p1_summary = summarize_player_stats(p1_df)
        p2_summary = summarize_player_stats(p2_df)

        # Just an example for 360 total minutes
        minutes = 360
        p1_values = {
            'Pass Accuracy (%)': p1_summary.get('Pass Accuracy (%)', 0),
            'Key Passes per 90': (p1_summary.get('Key Passes', 0) / minutes) * 90,
            'xG per Shot': p1_summary.get('Avg xG per Shot', 0),
            'Shots on Target %': 0 if p1_summary.get('Total Shots', 0) == 0 else (
                p1_summary['Shots on Target'] / p1_summary['Total Shots'] * 100
            ),
            'Carries per 90': (p1_summary.get('Carries', 0) / minutes) * 90,
            'Pressures per 90': (p1_summary.get('Pressures', 0) / minutes) * 90,
            'Goals per 90': (p1_summary.get('Goals', 0) / minutes) * 90,
            'Assists per 90': (p1_summary.get('Assists', 0) / minutes) * 90,
        }

        p2_values = {
            'Pass Accuracy (%)': p2_summary.get('Pass Accuracy (%)', 0),
            'Key Passes per 90': (p2_summary.get('Key Passes', 0) / minutes) * 90,
            'xG per Shot': p2_summary.get('Avg xG per Shot', 0),
            'Shots on Target %': 0 if p2_summary.get('Total Shots', 0) == 0 else (
                p2_summary['Shots on Target'] / p2_summary['Total Shots'] * 100
            ),
            'Carries per 90': (p2_summary.get('Carries', 0) / minutes) * 90,
            'Pressures per 90': (p2_summary.get('Pressures', 0) / minutes) * 90,
            'Goals per 90': (p2_summary.get('Goals', 0) / minutes) * 90,
            'Assists per 90': (p2_summary.get('Assists', 0) / minutes) * 90,
        }

        fig_radar = plot_radar_chart(p1_values, p2_values)
        st.plotly_chart(fig_radar, use_container_width=True)

else:
    st.info("⚠️ No data loaded yet. Please select your teams and click 'Load Data'.")

