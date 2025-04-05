import matplotlib.pyplot as plt
from mplsoccer import Pitch

def plot_ball_receipt_heatmaps(p1_locs, p2_locs):
    pitch = Pitch(pitch_type='statsbomb', line_color='black')
    fig, axs = pitch.grid(ncols=2, figheight=6)

    axs['pitch'][0].set_title("Player 1 - Ball Receipts", fontsize=14)
    pitch.kdeplot(
        x=p1_locs[:, 0], y=p1_locs[:, 1],
        ax=axs['pitch'][0], cmap='Blues', fill=True, bw_adjust=0.8, alpha=0.8
    )

    axs['pitch'][1].set_title("Player 2 - Ball Receipts", fontsize=14)
    pitch.kdeplot(
        x=p2_locs[:, 0], y=p2_locs[:, 1],
        ax=axs['pitch'][1], cmap='Reds', fill=True, bw_adjust=0.8, alpha=0.8
    )

    plt.tight_layout()
    plt.close(fig)
    return fig


def plot_shot_maps(p1_df, p2_df):
    pitch = Pitch(pitch_type='statsbomb', line_color='black')
    fig, axs = pitch.grid(ncols=2, figheight=6)

    # Player 1 Shots
    p1_shots = p1_df[p1_df['type'] == 'Shot']
    p1_x = p1_shots['location'].apply(lambda x: x[0] if isinstance(x, list) and len(x) == 2 else None)
    p1_y = p1_shots['location'].apply(lambda x: x[1] if isinstance(x, list) and len(x) == 2 else None)
    p1_xg = p1_shots['shot_statsbomb_xg']
    p1_goal = p1_shots['shot_outcome'] == 'Goal'

    axs['pitch'][0].set_title("Player 1 - Shot Map (xG)", fontsize=14)
    axs['pitch'][0].scatter(
        p1_x[~p1_goal], p1_y[~p1_goal],
        s=p1_xg[~p1_goal]*1000, color='blue', edgecolors='black'
    )
    axs['pitch'][0].scatter(
        p1_x[p1_goal], p1_y[p1_goal],
        s=p1_xg[p1_goal]*1000, color='green', edgecolors='black'
    )

    # Player 2 Shots
    p2_shots = p2_df[p2_df['type'] == 'Shot']
    p2_x = p2_shots['location'].apply(lambda x: x[0] if isinstance(x, list) and len(x) == 2 else None)
    p2_y = p2_shots['location'].apply(lambda x: x[1] if isinstance(x, list) and len(x) == 2 else None)
    p2_xg = p2_shots['shot_statsbomb_xg']
    p2_goal = p2_shots['shot_outcome'] == 'Goal'

    axs['pitch'][1].set_title("Player 2 - Shot Map (xG)", fontsize=14)
    axs['pitch'][1].scatter(
        p2_x[~p2_goal], p2_y[~p2_goal],
        s=p2_xg[~p2_goal]*1000, color='red', edgecolors='black'
    )
    axs['pitch'][1].scatter(
        p2_x[p2_goal], p2_y[p2_goal],
        s=p2_xg[p2_goal]*1000, color='green', edgecolors='black'
    )

    axs['pitch'][1].legend(["Missed/Blocked", "Goal"], loc='upper center', bbox_to_anchor=(0.5, 1.15))
    plt.tight_layout()
    plt.close(fig)
    return fig


def plot_key_pass_arrows(p1_df, p2_df):
    """
    Show passes that led to a shot (key passes) for each player on separate subplots.
    Player 1 in BLUE, Player 2 in RED.
    """
    pitch = Pitch(pitch_type='statsbomb', line_color='black')
    fig, axs = pitch.grid(ncols=2, figheight=6)

    # --- Player 1 Key Passes ---
    p1_kp = p1_df[(p1_df['type'] == 'Pass') & (p1_df['pass_shot_assist'] == True)]
    p1_start_x = p1_kp['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
    p1_start_y = p1_kp['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
    p1_end_x = p1_kp['pass_end_location'].apply(lambda x: x[0] if isinstance(x, list) else None)
    p1_end_y = p1_kp['pass_end_location'].apply(lambda x: x[1] if isinstance(x, list) else None)

    axs['pitch'][0].set_title("Player 1 Key Passes", fontsize=14)
    pitch.arrows(
        p1_start_x, p1_start_y,
        p1_end_x,   p1_end_y,
        ax=axs['pitch'][0],
        color='blue', width=2, headwidth=5, alpha=0.6
    )

    # --- Player 2 Key Passes ---
    p2_kp = p2_df[(p2_df['type'] == 'Pass') & (p2_df['pass_shot_assist'] == True)]
    p2_start_x = p2_kp['location'].apply(lambda x: x[0] if isinstance(x, list) else None)
    p2_start_y = p2_kp['location'].apply(lambda x: x[1] if isinstance(x, list) else None)
    p2_end_x = p2_kp['pass_end_location'].apply(lambda x: x[0] if isinstance(x, list) else None)
    p2_end_y = p2_kp['pass_end_location'].apply(lambda x: x[1] if isinstance(x, list) else None)

    axs['pitch'][1].set_title("Player 2 Key Passes", fontsize=14)
    pitch.arrows(
        p2_start_x, p2_start_y,
        p2_end_x,   p2_end_y,
        ax=axs['pitch'][1],
        color='red', width=2, headwidth=5, alpha=0.6
    )

    plt.tight_layout()
    plt.close(fig)
    return fig
