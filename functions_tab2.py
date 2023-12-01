import pandas as pd
from timple.timedelta import strftimedelta
import fastf1.plotting
from fastf1.core import Laps
import plotly.express as px
def plot_fastests_laps(session):
    # Loading the session data
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    session.load()
    # Preparing the data
    drivers = pd.unique(session.laps['Driver'])
    list_fastest_laps = [session.laps.pick_driver(drv).pick_fastest() for drv in drivers]
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
    # Converting LapTimeDelta to a format suitable for plotting
    fastest_laps['LapTimeDeltaSeconds'] = fastest_laps['LapTimeDelta'].dt.total_seconds()

    # Plotting using Plotly Express
    fig = px.bar(fastest_laps, y='Driver', x='LapTimeDeltaSeconds', orientation='h',
                 color='Team', text='LapTimeDeltaSeconds',
                 title=f"{session.event['EventName']} {session.event.year} Qualifying\n"
                       f"Fastest Lap: {strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')} ({pole_lap['Driver']})")

    fig.update_layout(yaxis={'categoryorder': 'total descending'})
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    # Ajout d'une annotation pour le pilote en pole position
    fig.add_annotation(x=1, y=pole_lap['Driver'],
                       text=f"Pole position : {pole_lap['Driver'], pole_lap['Team']}",
                       showarrow=False, font=dict(color='black'))
    return fig
def plot_positions_laps(session):
    session.load(telemetry=False, weather=False)

    # Preparing Data
    all_laps = pd.DataFrame()
    for drv in session.drivers:
        drv_laps = session.laps.pick_driver(drv).copy()
        drv_laps['Color'] = fastf1.plotting.driver_color(drv_laps['Driver'].iloc[0])
        all_laps = pd.concat([all_laps, drv_laps])

    # Plotting
    fig = px.line(all_laps, x='LapNumber', y='Position', color='Driver',
                  line_group='Driver', color_discrete_sequence=all_laps['Color'].unique(),
                  labels={'Position': 'Position', 'LapNumber': 'Lap'},
                  category_orders={"Position": list(range(20, 0, -1))})

    # Customization
    fig.update_layout(yaxis=dict(autorange="reversed"), title="Driver Positions by Lap")
    fig.update_traces(mode='lines+markers')

    return fig
def plot_teams_speeds_laps(session,year,race):
    session.load()
    laps = session.laps.pick_quicklaps()

    # Preparing Data
    transformed_laps = laps.copy()
    transformed_laps.loc[:, "LapTime (s)"] = laps["LapTime"].dt.total_seconds()

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
    fig.update_layout(title=f"Team speed comparaison by lap : {year} {race}", xaxis_title=None,
                      yaxis_title="Lap Time (s)")
    return fig