# src/preprocess.py

import pandas as pd

def summarize_player_stats(df: pd.DataFrame) -> dict:
    """
    Summarize key statistics from a player's event dataframe.

    Args:
        df (pd.DataFrame): Event data for a single player.

    Returns:
        dict: A dictionary of aggregated performance metrics.
    """
    total_passes = df[df['type'] == 'Pass'].shape[0]
    accurate_passes = df[(df['type'] == 'Pass') & (df['pass_outcome'].isna())].shape[0]
    pass_accuracy = accurate_passes / total_passes * 100 if total_passes else 0

    summary = {
        'Total Passes': total_passes,
        'Pass Accuracy (%)': round(pass_accuracy, 2),
        'Forward Passes': df[(df['type'] == 'Pass') & (df['pass_angle'] < 90)].shape[0],
        'Key Passes': df['pass_shot_assist'].notna().sum(),
        'Assists': df['pass_goal_assist'].notna().sum(),
        'Total Shots': df[df['type'] == 'Shot'].shape[0],
        'Goals': df[df['shot_outcome'] == 'Goal'].shape[0],
        'Shots on Target': df[df['shot_outcome'] == 'Saved'].shape[0] + df[df['shot_outcome'] == 'Goal'].shape[0],
        'Total xG': round(df['shot_statsbomb_xg'].sum(), 3),
        'Avg xG per Shot': round(df['shot_statsbomb_xg'].mean(), 3) if df[df['type'] == 'Shot'].shape[0] > 0 else 0,
        'Carries': df[df['type'] == 'Carry'].shape[0],
        'Dribbles Attempted': df[df['type'] == 'Dribble'].shape[0],
        'Pressures': df[df['type'] == 'Pressure'].shape[0],
        'Duels Attempted': df[df['type'] == 'Duel'].shape[0],
        'Duels Won': df[df['duel_outcome'] == 'Won'].shape[0],
        'Ball Recoveries': df[df['type'] == 'Ball Recovery'].shape[0],
        'Dispossessed': df[df['type'] == 'Dispossessed'].shape[0],
        'Miscontrols': df[df['type'] == 'Miscontrol'].shape[0],
        'Ball Receipts': df[df['type'] == 'Ball Receipt*'].shape[0],
        'Fouls Won (Advantage)': df[df['foul_won_advantage'] == True].shape[0],
        'Fouls Won (Defensive)': df[df['foul_won_defensive'] == True].shape[0],
        'Fouls Won (Penalty)': df[df['foul_won_penalty'] == True].shape[0],
        'Aerial Passes Won': df[df['pass_aerial_won'] == True].shape[0],
        'Pass Miscommunications': df[df['pass_miscommunication'] == True].shape[0],
        'Bad Behaviour Cards': df[df['bad_behaviour_card'].notna()].shape[0]
    }

    return summary