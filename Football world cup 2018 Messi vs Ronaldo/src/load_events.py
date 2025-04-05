import pandas as pd
from statsbombpy import sb

def load_events_for_players(match_ids, player_names=None):
    all_events = []
    for match_id in match_ids:
        events = sb.events(match_id=match_id)
        if player_names:
            events = events[events['player'].isin(player_names)]
        all_events.append(events)

    if not all_events:
        return pd.DataFrame()  # prevent concat error if no events

    return pd.concat(all_events, ignore_index=True)

