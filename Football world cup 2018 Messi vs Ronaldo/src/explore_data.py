from statsbombpy import sb
import pandas as pd

def list_competitions():
    """Return all available competitions with ID and season."""
    comps = sb.competitions()
    return comps[['competition_name', 'competition_id', 'season_name', 'season_id']]

def list_teams(competition_id: int, season_id: int):
    """List all teams in a competition + season."""
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    home_teams = matches['home_team'].unique()
    away_teams = matches['away_team'].unique()
    all_teams = sorted(set(home_teams) | set(away_teams))
    return all_teams

def list_players_from_teams(competition_id: int, season_id: int, team_list: list):
    """List all unique players from selected teams."""
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    match_ids = matches[
        (matches['home_team'].isin(team_list)) | (matches['away_team'].isin(team_list))
    ]['match_id'].tolist()

    all_players = set()
    for match_id in match_ids:
        events = sb.events(match_id=match_id)
        players = events['player'].dropna().unique().tolist()
        all_players.update(players)

    return sorted(all_players)