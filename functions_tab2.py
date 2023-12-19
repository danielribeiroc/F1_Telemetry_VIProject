import pandas as pd
from timple.timedelta import strftimedelta
import fastf1.plotting
from fastf1.core import Laps
import plotly.express as px
import plotly.graph_objs as go


def plot_fastests_laps(YEAR, RACE):
    fastest_laps_df = pd.read_csv(f"./data_tab_2/{YEAR}/qualif/{RACE}_fastest_laps.csv")
    pole_lap_df = pd.read_csv(f"./data_tab_2/{YEAR}/qualif/{RACE}_pole_lap.csv")

    # Create an empty figure
    fig = go.Figure()

    # Add a bar to the figure for each team
    for team in fastest_laps_df['Team'].unique():
        df_team = fastest_laps_df[fastest_laps_df['Team'] == team]
        fig.add_trace(go.Bar(
            y=df_team['Driver'],
            x=df_team['LapTimeDeltaSeconds'],
            name=team,
            orientation='h',
            marker=dict(color=df_team['Color'].iloc[0]),  # Assuming each team has a unique color
            text=df_team['LapTimeDeltaSeconds'],
            textposition='outside'
        ))

    # Add annotation for the fastest lap
    if not pole_lap_df.empty:
        fig.add_annotation(
            text=f"Tour le plus rapide: {pole_lap_df['LapTime'].iloc[0]} {pole_lap_df['Driver'].iloc[0]}, {pole_lap_df['Team'].iloc[0]}",
            xref="paper", yref="paper",
            x=-0.01, y=1.15,
            showarrow=False,
            font=dict(size=14),
            align="left"
        )

    # Update layout
    fig.update_layout(
        title=f"{RACE} {YEAR} Qualifications",
        yaxis=dict(categoryorder='total descending', dtick=1),
        legend_title_text='Team Colors'
    )

    return fig


def plot_positions_laps(YEAR, RACE):
    all_laps = pd.read_csv(f"./data_tab_2/{YEAR}/race/{RACE}_all_laps.csv")
    # Plotting
    fig = px.line(all_laps, x='LapNumber', y='Position', color='Driver',
                  line_group='Driver', color_discrete_sequence=all_laps['Color'].unique(),
                  labels={'Position': 'Position', 'LapNumber': 'Lap'},
                  category_orders={"Position": list(range(20, 0, -1))})

    # Customization
    fig.update_layout(yaxis=dict(autorange="reversed"), title=f"{RACE} {YEAR} Course")
    fig.update_traces(mode='lines+markers')
    return fig

def plot_teams_speeds_laps(YEAR, RACE):
    transformed_laps = pd.read_csv(f"./data_tab_2/{YEAR}/race/{RACE}_transformed_laps.csv")
    # Team Order and Color Palette
    team_order = (
        transformed_laps[["Team", "LapTime (s)"]]
        .groupby("Team")
        .median()["LapTime (s)"]
        .sort_values()
        .index
    )
    team_palette = {team: fastf1.plotting.team_color(team) for team in team_order}

    # Plotting
    fig = px.box(transformed_laps, x="Team", y="LapTime (s)", category_orders={"Team": team_order},
                 color="Team", color_discrete_map=team_palette)

    # Customization with More Colors
    # Customize outliers
    fig.update_traces(marker=dict(color='black', size=5), line=dict(color='white'))
    # Customize box and whisker colors
    for team, color in team_palette.items():
        fig.update_traces(selector=dict(name=team), line=dict(color=color))

    # Update layout and titles
    fig.update_layout(title=f"{RACE} {YEAR} Course", xaxis_title=None,
                      yaxis_title="Lap Time (s)")
    return fig