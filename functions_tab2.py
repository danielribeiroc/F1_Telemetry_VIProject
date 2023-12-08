import pandas as pd
from timple.timedelta import strftimedelta
import fastf1.plotting
from fastf1.core import Laps
import plotly.express as px


def plot_fastests_laps(YEAR, RACE):
    session = fastf1.get_session(YEAR, RACE, 'Q')
    # Loading the session data
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    session.load()

    # Preparing the data
    drivers = pd.unique(session.laps['Driver'])
    list_fastest_laps = [session.laps.pick_driver(drv).pick_fastest() for drv in drivers]
    fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
    pole_lap = fastest_laps.pick_fastest()
    fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']
    fastest_laps['LapTimeDeltaSeconds'] = fastest_laps['LapTimeDelta'].dt.total_seconds()

    def get_team_color(team):
        try:
            return fastf1.plotting.team_color(team)
        except:
            return '#000000'

    # Adding team colors directly within the main function
    fastest_laps['Color'] = fastest_laps['Team'].apply(get_team_color)

    # Plotting
    fig = px.bar(fastest_laps, y='Driver', x='LapTimeDeltaSeconds', orientation='h',
                 color='Team',
                 color_discrete_map={team: color for team, color in zip(fastest_laps['Team'], fastest_laps['Color'])},
                 text='LapTimeDeltaSeconds',
                 title=f"{session.event['EventName']} {session.event.year} Qualifying")

    fig.add_annotation(
        text=f"Fastest Lap: {strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')} {pole_lap['Driver'], pole_lap['Team']}",
        xref="paper", yref="paper",
        x=-0.01, y=1.15,
        showarrow=False,
        font=dict(size=14),
        align="left"
    )

    fig.update_layout(yaxis={'categoryorder': 'total descending', 'dtick': 1}, legend_title_text='Team Colors')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    return fig


def plot_positions_laps(YEAR, RACE):
    session = fastf1.get_session(YEAR, RACE, 'R')
    session.load(telemetry=False, weather=False)

    # Preparing Data
    all_laps = pd.DataFrame()
    print(f"Number total of drivers {len(session.drivers)}")
    for drv in session.drivers:
        drv_laps = session.laps.pick_driver(drv).copy()
        print("----------------------------------------------")
        print(drv)
        print(session.get_driver(drv)["Abbreviation"])
        try:
            driver_color = fastf1.plotting.driver_color(session.get_driver(drv)["Abbreviation"])
            if driver_color:
                print(driver_color)
                drv_laps['Color'] = driver_color
            else:
                print("No color assigned for this driver.")
                drv_laps['Color'] = fastf1.plotting.team_color(session)  # Assign a default color
            all_laps = pd.concat([all_laps, drv_laps])
        except Exception as e:
            print(f"Error encountered: {e}")
            # Handle the error or assign a default color
            drv_laps['Color'] = "#ffffff"
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

def plot_teams_speeds_laps(YEAR, RACE):
    session = fastf1.get_session(YEAR, RACE, 'R')
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
    fig.update_layout(title=f"Team speed comparaison by lap : {YEAR} {RACE}", xaxis_title=None,
                      yaxis_title="Lap Time (s)")
    return fig