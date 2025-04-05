from statsbombpy import sb
import pandas as pd

def get_competitions():
    """Load all available competitions from StatsBomb."""
    competitions = sb.competitions()
    return competitions

def get_matches(competition_id: int, season_id: int) -> pd.DataFrame:
    """Load all matches for a specific competition and season."""
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    return matches

def filter_matches_by_teams(matches_df: pd.DataFrame, team_list: list) -> pd.DataFrame:
    """Return matches where either home or away team is in the team_list."""
    return matches_df[
        matches_df['home_team'].isin(team_list) |
        matches_df['away_team'].isin(team_list)
    ]