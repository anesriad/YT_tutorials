import plotly.graph_objects as go

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

def plot_radar_chart(p1_values: dict, p2_values: dict):
    parameters = list(p1_values.keys())

    # Define min/max ranges
    ranges = {
        'Pass Accuracy (%)': (70, 100),
        'Key Passes per 90': (0, 7),
        'xG per Shot': (0, 0.2),
        'Shots on Target %': (0, 100),
        'Carries per 90': (0, 100),
        'Pressures per 90': (0, 30),
        'Goals per 90': (0, 1.5),
        'Assists per 90': (0, 1.5),
    }

    p1_norm = [(normalize(p1_values[param], *ranges[param])) for param in parameters]
    p2_norm = [(normalize(p2_values[param], *ranges[param])) for param in parameters]

    # close the loop
    parameters += [parameters[0]]
    p1_norm += [p1_norm[0]]
    p2_norm += [p2_norm[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=p1_norm,
        theta=parameters,
        fill='toself',
        name='Player 1',
        marker=dict(color='blue')
    ))
    fig.add_trace(go.Scatterpolar(
        r=p2_norm,
        theta=parameters,
        fill='toself',
        name='Player 2',
        marker=dict(color='red')
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Radar Chart: Player 1 vs Player 2 (Normalized)"
    )

    return fig
