import time
import base64
import numpy as np
import pandas as pd
from io import BytesIO
from timple.timedelta import strftimedelta

import dash
from dash import dcc, html
import dash._callback_context as ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager

import fastf1 as ff1
import fastf1.plotting
from fastf1.core import Laps
from fastf1.ergast import Ergast

import matplotlib  # pip install matplotlib

matplotlib.use('agg')

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

import plotly.express as px
import plotly.graph_objects as go

## Diskcache
import diskcache

fastf1.Cache.enable_cache("./cache")
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
session = None
tab_test = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)

f1_logo_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/2560px-F1.svg.png"
additional_image_path = 'https://www.msengineering.ch/typo3conf/ext/msengineering/Resources/Public/Images/Logo/mse-full.svg'
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=f1_logo_path, height="50px"), width=2, align='center'),
        dbc.Col(html.H1("F1 - Telemetry - Project VI", className='mb-2', style={'textAlign': 'center'}), width=7),
        dbc.Col(html.Img(src=additional_image_path, height="75px"), width=2, align='center')
    ], align='center', className='mb-4 mt-4'),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Comparaison entre pilotes', value='tab-1', children=[
            html.Div([
                html.Br(),
                html.H3('Vue comparaison entre 2 pilotes', style={'margin-top': '10px'}),
                html.P(
                    "Dans cet onglet, les utilisateurs ont la possibilité de comparer les performances de deux pilotes lors d'une course spécifique. n cas d'erreur ou de problème lors du "
                    "chargement des données ou du traitement des informations, un message d'erreur explicite est affiché pour informer l'utilisateur de la situation, garantissant ainsi une expérience utilisateur transparente et informative.",
                    style={'margin-top': '10px'}),
                html.Br(),
                dbc.Alert(
                    "La session n'a pas de données (potentiellement qu'elle ne s'est pas encore déroulé)",
                    id="alert-no-fade",
                    dismissable=True,
                    fade=False,
                    is_open=False,
                    color="danger"
                ),
                dbc.Alert(
                    "Hello! I am an alert that doesn't fade in or out",
                    id="alert-no-fade2",
                    dismissable=True,
                    fade=False,
                    is_open=False,
                    color="danger"
                ),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(
                            id='dropdown-11',
                            options=[
                                {'label': str(year), 'value': year} for year in range(2019, 2024)
                            ],
                            value=2023,
                            className='mb-3 mt-10'
                        )
                    ]),
                    dbc.Col([
                        dcc.Loading(
                            id='loading-dropdown-12',
                            type='default',
                            children=[dcc.Dropdown(id='dropdown-12', className='mb-3 mt-10')]
                        )
                    ])
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Loading(
                            id='loading-dropdown-3',
                            type='default',
                            children=[dcc.Dropdown(id='dropdown-3', className='mb-3')]
                        ),
                    ]),
                    dbc.Col([
                        dcc.Loading(
                            id='loading-dropdown-4',
                            type='default',
                            children=[dcc.Dropdown(id='dropdown-4', className='mb-3')]
                        )
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([html.Button(id="button_id", children="Comparer les 2 pilotes !")]),
                dbc.Col([html.Button(id="cancel_button_id", children="Interrompre le processus")])
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Loading(
                        id="loading-overlaying",
                        children=[dcc.Graph(id="overlaying")],
                        type="circle",
                    )
                ]),
                dbc.Col([
                    dcc.Loading(
                        id="loading-bar_graph",
                        children=[html.Img(id='bar-graph-matplotlib')],
                        type="circle",
                    )
                ])
            ]),
            dbc.Row(
                    dbc.Col(
                        html.Footer(
                            html.P("Created by Daniel Ribeiro Cabral & Ruben Terceiro - contact: daniel.ribeiroc@master.hes-so.ch"),
                            className="text-center text-muted"
                        ),
                        width=12
                    ),
                    className='mt-5'  # Adds top margin to the footer row
                )
        ]),
        dcc.Tab(label='Vue globale d\'un week-end de course', value='tab-2', children=[
            html.Div([
                html.H3('Dynamique des courses et analyse des résultats des équipes', style={'margin-top': '10px'}),
                html.P(
                    'Sous cet onglet nous avons un premier graphique qui permet de voir les différences de temps pour toute la course entre tous les pilotes, l\'évolution du classement durant la course pour chaque pilote et enfin des une booîte à moustache nous indiquant les statistiques pour chaque écurie concernant le temps pour chaque tour')
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        id='dropdown-21',
                        options=[
                            {'label': str(year), 'value': year} for year in range(2019, 2024)
                        ],
                        value=2023,
                        className='mb-3 mt-10'
                    )
                ]),
                dbc.Col([
                    dcc.Loading(
                        id='loading-dropdown-22',
                        type='default',
                        children=[dcc.Dropdown(id='dropdown-22', className='mb-3 mt-10')]
                    )
                ])
            ]),
            dbc.Row([
                html.H3("Différence de vitesse durant la phase de qualification", style={'margin-top': '10px'}),
                dcc.Loading(
                    id="fastestLaps",
                    children=[dcc.Graph(id="fastests-laps")],
                    type="circle",
                )
            ]),
            dbc.Row([
                html.H3("Position des pilotes par tour", style={'margin-top': '10px'}),
                dcc.Loading(
                    id="positionLaps",
                    children=[dcc.Graph(id="positions-laps")],
                    type="circle",
                )
            ]),dbc.Row([
                html.H3("Statistiques du temps réalisé par tour pour chaque équipe", style={'margin-top': '10px'}),
                dcc.Loading(
                    id="teamsSpeeds",
                    children=[dcc.Graph(id="teams-speeds")],
                    type="circle",
                )
            ]),
            dbc.Row([
                html.H3("", style={'margin-bottom': '30px'}),
            ]),
            dbc.Row(
                    dbc.Col(
                        html.Footer(
                            html.P("Created by Daniel Ribeiro Cabral & Ruben Terceiro - contact: ruben.terceiro@master.hes-so.ch"),
                            className="text-center text-muted"
                        ),
                        width=12
                    ),
                    className='mt-5'  # Adds top margin to the footer row
                )
        ]),
        dcc.Tab(label='Classement par course', value='tab-3', children=[
            html.Div([
                html.H2('Classement des Pilotes et des Équipes par Courses', style={'margin-top': '10px'}),
                html.P(
                    "Les graphiques interactifs présentent le nombre de points gagnés par course pour chaque participant, qu'il s'agisse de pilotes ou d'équipes. L'ordre des équipes et des pilotes est déterminé en fonction du nombre total de points accumulés à la fin de la saison ou à l'étape actuelle de la saison en cours.")
            ]),
            dcc.Dropdown(
                id='dropdown_tab_3_year',
                options=[
                    {'label': str(year), 'value': year} for year in range(2019, 2024)
                ],
                value=2022,
                className='mb-3 mt-10'
            ),
            dbc.Row([
                html.H3("Classement des courses par pilote !", style={'margin-top': '10px'}),
                dcc.Loading(
                    id="classementParPilotes",
                    children=[dcc.Graph(id="class-par-pilotes")],
                    type="circle",
                )
            ]),
            dbc.Row([
                html.H3("Classement des courses par équipe !", style={'margin-top': '10px'}),
                dcc.Loading(
                    id="classementParTeams",
                    children=[dcc.Graph(id="class-par-teams")],
                    type="circle",
                )
            ]),

            dbc.Row([
                html.H3("", style={'margin-bottom': '30px'}),
            ]),
            dbc.Row(
                    dbc.Col(
                        html.Footer(
                            html.P("Created by Daniel Ribeiro Cabral & Ruben Terceiro - contact: daniel.ribeiroc@master.hes-so.ch"),
                            className="text-center text-muted"
                        ),
                        width=12
                    ),
                    className='mt-5'  # Adds top margin to the footer row
                )
        ]),
    ]),
])


def get_years_selection(selected_year):
    if selected_year is None:
        raise PreventUpdate

    print("------------------------------------------------------")
    print(selected_year)
    print("------------------------------------------------------")
    years_session = ff1.get_event_schedule(selected_year)['EventName']
    # session = ff1.get_event_schedule(2023)['Country']
    tab_countries = [i for i in years_session]
    # [{'label': list[i], 'value': i} for i in range(len(list))]
    return tab_countries


@app.callback(
    Output('loading-dropdown-12', 'children'),
    Output('dropdown-12', 'options'),
    Output('dropdown-12', 'value'),
    Input('dropdown-11', 'value')
)
def update_dropdown_12(selected_year):
    tab_countries = get_years_selection(selected_year)
    # [{'label': list[i], 'value': i} for i in range(len(list))]
    return [dcc.Dropdown(id='dropdown-12', options=tab_countries, className='mb-3')], tab_countries, tab_countries[1]


@app.callback(
    Output('loading-dropdown-22', 'children'),
    Output('dropdown-22', 'options'),
    Output('dropdown-22', 'value'),
    Input('dropdown-21', 'value')
)
def update_dropdown_22(selected_year):
    tab_countries = get_years_selection(selected_year)
    return [dcc.Dropdown(id='dropdown-22', options=tab_countries, className='mb-3')], tab_countries, tab_countries[1]


@app.callback(
    Output('loading-dropdown-3', 'children'),
    Output('dropdown-3', 'options'),
    Output('dropdown-3', 'value'),
    Output("alert-no-fade", "is_open"),
    Input('dropdown-11', 'value'),
    Input('dropdown-12', 'value')
)
def update_dropdown_3(selected_year, selected_race):
    global session
    global tab_test
    if selected_race is None:
        raise PreventUpdate

    year_schedule = ff1.get_event_schedule(selected_year)['EventName']
    indices = [index for index, country in enumerate(year_schedule) if country == selected_race]
    print("Print indices :")
    print(indices)
    if indices == None:
        indices = 0

    try:
        session = ff1.get_session(selected_year, year_schedule[indices[0]], "R")
        session.load(telemetry=False, laps=False, weather=False)
        drivers = [i for i in session.drivers]
        drivers_name = [session.get_driver(i)["Abbreviation"] for i in drivers]
        return [dcc.Dropdown(id='dropdown-3', options=drivers_name, className='mb-3')], drivers_name, drivers_name[
            0], False
    except:
        return [dcc.Dropdown(id='dropdown-3', options=["None"], className='mb-3')], ["None"], ["None"], True


@app.callback(
    Output('loading-dropdown-4', 'children'),
    Output('dropdown-4', 'options'),
    Output('dropdown-4', 'value'),
    Output("alert-no-fade2", "is_open"),
    Input('dropdown-11', 'value'),
    Input('dropdown-12', 'value'),
    Input('dropdown-3', 'value')
)
def update_dropdown_4(selected_year, selected_month, selected_day):
    global session
    if selected_day is None:
        raise PreventUpdate
    try:
        session.load(telemetry=False, laps=False, weather=False)
        drivers = [i for i in session.drivers]
        drivers_name = [session.get_driver(i)["Abbreviation"] for i in drivers]
        return [dcc.Dropdown(id='dropdown-4', options=drivers_name, className='mb-3')], drivers_name, drivers_name[
            1], False
    except:
        return [dcc.Dropdown(id='dropdown-4', options=["None"], className='mb-3')], ["None"], ["None"], False


@app.long_callback(
    output=[Output(component_id='bar-graph-matplotlib', component_property="src"),
            Output(component_id='overlaying', component_property="figure")],
    inputs=[Input("button_id", "n_clicks")],
    state=[State('dropdown-11', 'value'),
           State('dropdown-12', 'value'),
           State('dropdown-3', 'value'),
           State('dropdown-4', 'value')],
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
)
def plot_data_tab_1(n_clicks, year, race, driver1, driver2):
    # n_clicks, year, race, driver1, driver2
    print("PLOT DATA")
    fig_bar_matplotlib, overlaying = build_comparaison_tab(year, race, driver1, driver2)
    print("Done")
    return fig_bar_matplotlib, overlaying


@app.callback(
    Output(component_id='fastests-laps', component_property="figure"),
    Output(component_id='positions-laps', component_property="figure"),
    Output(component_id='teams-speeds', component_property="figure"),
    Input("dropdown-21", "value"),
    Input("dropdown-22", "value")
)
def plot_data_tab_2(year, race):
    race_session = fastf1.get_session(year, race, 'R')
    qualif_session = fastf1.get_session(year, race, 'Q')

    print("PLOT DATA")

    fig_fastest_laps = plot_fastests_laps(qualif_session)
    fig_positions_laps = plot_positions_laps(race_session)
    fig_teams_speeds = plot_teams_speeds_laps(race_session)

    print("Done")

    return fig_fastest_laps, fig_positions_laps, fig_teams_speeds


@app.callback(
    [Output(component_id='class-par-pilotes', component_property="figure"),
     Output(component_id='class-par-teams', component_property="figure")],
    [Input("dropdown_tab_3_year", "value")]
)
def plot_data_tab_3(year):
    print("PLOT DATA")
    fig = plot_standings_by_driver(year)
    fig_by_team = plot_standings_by_teams(year)
    print("Charging done")
    return fig, fig_by_team

"--------------------------------------------- Code for plots of tab 1 ------------------------------------------------------------"


def build_comparaison_tab(year, race, driver1, driver2):
    global session
    global tab_test
    print(tab_test)
    try:

        if race == None:
            _1race = "Bahrain Grand Prix"
        else:
            _1race = race
        if driver1 == None:
            _driver1 = "VER"
        else:
            _driver1 = driver1
        if driver2 == None:
            _driver2 = "PER"
        else:
            _driver2 = driver2

        year_schedule = ff1.get_event_schedule(year)['EventName']
        indices = [index for index, country in enumerate(year_schedule) if country == _1race]
        _race = year_schedule[indices[0]]
        session = ff1.get_session(year, _1race, "R")
        session.load(telemetry=True, laps=True, weather=False)
        lap_driver1 = session.laps.pick_driver(_driver1).pick_fastest()
        lap_driver2 = session.laps.pick_driver(_driver2).pick_fastest()
        # Calculate lap times for both drivers
        lap = lap_driver1
        lap_time_driver1 = lap_driver1.telemetry['Time'].values
        lap_time_driver2 = lap_driver2.telemetry['Time'].values
        who_fastest = []

        if len(lap_time_driver1) < len(lap_time_driver2):
            # Make lap_time_driver1 the same length as lap_time_driver2
            lap_time_driver2 = lap_time_driver2[:len(lap_time_driver1)]
        elif len(lap_time_driver2) < len(lap_time_driver1):
            # Make lap_time_driver2 the same length as lap_time_driver1
            lap_time_driver1 = lap_time_driver1[:len(lap_time_driver2)]
        else:
            # Both arrays are already of the same length, no modification needed
            pass

        print(f"Length of the driver {driver1} : {len(lap_time_driver1)}")
        print(f"Length of the driver {driver2} : {len(lap_time_driver2)}")
        # Jump 10 laps at a time and compare lap times
        for i in range(0, len(lap_time_driver1) - 10, 10):
            lap_time_1_chunk = lap_time_driver1[i + 10] - lap_time_driver1[i]
            lap_time_2_chunk = lap_time_driver2[i + 10] - lap_time_driver2[i]

            if lap_time_1_chunk < lap_time_2_chunk:
                for j in range(10):
                    who_fastest.append(True)
            else:
                for j in range(10):
                    who_fastest.append(False)

        # Check if there are any remaining laps that are not a multiple of 10
        remaining_laps = len(lap_time_driver1) % 10
        if remaining_laps > 0:
            # Compare the remaining laps individually
            for i in range(len(lap_time_driver1) - remaining_laps, len(lap_time_driver1)):
                if lap_time_driver1[i] < lap_time_driver2[i]:
                    who_fastest.append(True)
                else:
                    who_fastest.append(False)

        # Get telemetry data
        x = lap.telemetry['X']  # values for x-axis
        y = lap.telemetry['Y']  # values for y-axis

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        # We create a plot with title and adjust some setting to make it look good.
        fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
        fig.suptitle(f'{_1race} - {year} - {_driver1} vs {_driver2} - Speed', size=24, y=0.97)

        # Adjust margins and turn of axis
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        ax.axis('off')

        mask = np.array(who_fastest)  # Repeat each element 10 times for each sector

        # After this, we plot the data itself.
        # Create background track line
        ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
        norm = plt.Normalize(0, 1)
        # Set the color based on the mask
        lc = LineCollection(segments, cmap=mpl.colors.ListedColormap(
            [fastf1.plotting.driver_color(_driver1), fastf1.plotting.driver_color(_driver2)]), norm=norm, linewidth=5)
        lc.set_array(mask)

        # Set the values used for colormapping
        lc.set_array(mask)

        # Merge all line segments together
        line = ax.add_collection(lc)

        # Finally, we create a color bar as a legend.
        # Create a color bar as a legend.
        cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
        normlegend = mpl.colors.Normalize(vmin=0, vmax=1)  # Assuming 'who_fastest' contains True and False values
        legend_labels = [f"Driver {_driver1} Fastest", f"Driver {_driver2} Fastest"]
        legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=mpl.colors.ListedColormap(
            [fastf1.plotting.driver_color(_driver1), fastf1.plotting.driver_color(_driver2)]),
                                           orientation="horizontal", ticks=[0, 1])
        legend.set_ticklabels(legend_labels)
        # Save it to a temporary buffer.
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
        fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'
        fig_over = overlayingSpeed(session, _driver1, _driver2)
        return fig_bar_matplotlib, fig_over

    except Exception as e:
        # Handle the error here
        print(f"Error occurred: {e}")
        # Create an image with the error message
        buf = BytesIO()
        fig = plt.figure()
        plt.text(0.5, 0.5, f"Error: {e}", ha='center', va='center', fontsize=10)
        plt.axis('off')  # Turn off axis for the error message
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
        fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

        return fig_bar_matplotlib, None
def overlayingSpeed(SESSION_FASTF1, DRIVER1, DRIVER2):
    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    rbr_color = fastf1.plotting.driver_color(DRIVER1)
    mer_color = fastf1.plotting.driver_color(DRIVER2)
    session = SESSION_FASTF1
    ver_lap = session.laps.pick_driver(DRIVER1).pick_fastest()
    ham_lap = session.laps.pick_driver(DRIVER2).pick_fastest()
    ver_tel = ver_lap.get_car_data().add_distance()
    ham_tel = ham_lap.get_car_data().add_distance()

    ver_tel_data = {
        'Distance': ver_tel['Distance'],
        'Speed': ver_tel['Speed']
    }

    ham_tel_data = {
        'Distance': ham_tel['Distance'],
        'Speed': ham_tel['Speed']
    }

    ver_trace = go.Scatter(
        x=ver_tel_data['Distance'],
        y=ver_tel_data['Speed'],
        mode='lines',
        name=DRIVER1,
        line=dict(color=rbr_color)
    )

    ham_trace = go.Scatter(
        x=ham_tel_data['Distance'],
        y=ham_tel_data['Speed'],
        mode='lines',
        name=DRIVER2,
        line=dict(color=mer_color)
    )

    layout = go.Layout(
        title=f"Fastest Lap in Race - Overlaying \n {session.event['EventName']} {session.event.year}",
        xaxis=dict(title='Distance in m'),
        yaxis=dict(title='Speed in km/h'),
        legend=dict(x=0, y=1)
    )

    # Create figure and add traces
    fig = go.Figure(data=[ver_trace, ham_trace], layout=layout)
    return fig


"--------------------------------------------- Code for plots of tab 2 ------------------------------------------------------------"

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
def plot_teams_speeds_laps(session):
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
    fig.update_layout(title="Team speed comparaison by lap : 2023 British Grand Prix", xaxis_title=None,
                      yaxis_title="Lap Time (s)")
    return fig


"--------------------------------------------- Code for plots of tab 3 ------------------------------------------------------------"


def plot_standings_by_driver(SEASON):
    ergast = Ergast()
    races = ergast.get_race_schedule(SEASON)  # Races in year 2022
    results = []
    for rnd, race in races['raceName'].items():
        print(f"Drivers : Race : {race}")
        # Get results. Note that we use the round no. + 1, because the round no.
        # starts from one (1) instead of zero (0)
        temp = ergast.get_race_results(season=SEASON, round=rnd + 1)
        if len(temp.content) < 1:
            break
        else:
            temp = temp.content[0]

        # If there is a sprint, get the results as well
        sprint = ergast.get_sprint_results(season=SEASON, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
            # Add sprint points and race points to get the total
            temp['points'] = temp['points_x'] + temp['points_y']
            temp.drop(columns=['points_x', 'points_y'], inplace=True)

        # Add round no. and grand prix name
        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        temp = temp[['round', 'race', 'driverCode', 'points']]  # Keep useful cols.
        results.append(temp)

    # Append all races into a single dataframe
    results = pd.concat(results)
    races = results['race'].drop_duplicates()
    results = results.pivot(index='driverCode', columns='round', values='points')
    # Rank the drivers by their total points
    results['total_points'] = results.sum(axis=1)
    results = results.sort_values(by='total_points', ascending=False)
    results.drop(columns='total_points', inplace=True)

    # Use race name, instead of round no., as column names
    results.columns = races
    fig = px.imshow(
        results,
        text_auto=True,
        aspect='auto',  # Automatically adjust the aspect ratio
        color_continuous_scale=[[0, 'rgb(198, 219, 239)'],  # Blue scale
                                [0.25, 'rgb(107, 174, 214)'],
                                [0.5, 'rgb(33,  113, 181)'],
                                [0.75, 'rgb(8,   81,  156)'],
                                [1, 'rgb(8,   48,  107)']],
        labels={'x': 'Race',
                'y': 'Driver',
                'color': 'Points'}  # Change hover texts
    )
    fig.update_xaxes(title_text='')  # Remove axis titles
    fig.update_yaxes(title_text='')
    fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                     showline=False,
                     tickson='boundaries')  # Show horizontal grid only
    fig.update_xaxes(showgrid=False, showline=False)  # And remove vertical grid
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')  # White background
    fig.update_layout(coloraxis_showscale=False)  # Remove legend
    fig.update_layout(xaxis=dict(side='top'))  # x-axis on top
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
    return fig


def plot_standings_by_teams(Year):
    ergast = Ergast()
    races = ergast.get_race_schedule(Year)  # Races in year 2022
    results = []
    for rnd, race in races['raceName'].items():
        print("Teams : Race name ", race)
        # Get results. Note that we use the round no. + 1, because the round no.
        # starts from one (1) instead of zero (0)
        temp = ergast.get_race_results(season=Year, round=rnd + 1)
        if len(temp.content) < 1:
            break
        else:
            temp = temp.content[0]

        # If there is a sprint, get the results as well
        sprint = ergast.get_sprint_results(season=Year, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            temp = pd.merge(temp, sprint.content[0], on='constructorName', how='left')
            # Add sprint points and race points to get the total
            temp['points'] = temp['points_x'] + temp['points_y']
            temp.drop(columns=['points_x', 'points_y'], inplace=True)

        # Add round no. and grand prix name
        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        temp = temp[['round', 'race', 'constructorName', 'points']]  # Keep useful cols.
        results.append(temp)
    results = pd.concat(results)
    races = results['race'].drop_duplicates()
    test = results.groupby(["round", "race", "constructorName"]).sum().reset_index()
    results = test.pivot(index='constructorName', columns='race', values='points')
    results['total_points'] = results.sum(axis=1)
    results = results.sort_values(by='total_points', ascending=False)
    results.drop(columns='total_points', inplace=True)

    # Use race name, instead of round no., as column names
    results.columns = races
    # Assuming 'results' is your data, replace it with your actual dat
    fig = px.imshow(
        results,
        text_auto=True,
        aspect='auto',  # Automatically adjust the aspect ratio
        color_continuous_scale=[[0, 'rgb(198, 219, 239)'],  # Blue scale
                                [0.25, 'rgb(107, 174, 214)'],
                                [0.5, 'rgb(33,  113, 181)'],
                                [0.75, 'rgb(8,   81,  156)'],
                                [1, 'rgb(8,   48,  107)']],
        labels={'x': 'Race',
                'y': 'Driver',
                'color': 'Points'}  # Change hover texts
    )
    fig.update_xaxes(title_text='')  # Remove axis titles
    fig.update_yaxes(title_text='')
    fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                     showline=False,
                     tickson='boundaries')  # Show horizontal grid only
    fig.update_xaxes(showgrid=False, showline=False)  # And remove vertical grid
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')  # White background
    fig.update_layout(coloraxis_showscale=False)  # Remove legend
    fig.update_layout(xaxis=dict(side='top'))  # x-axis on top
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8082)
