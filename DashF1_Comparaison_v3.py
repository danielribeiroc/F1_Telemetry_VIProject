import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager
import fastf1 as ff1
import fastf1.plotting
import matplotlib
from functions_tab1 import build_comparaison_tab
from functions_tab2 import plot_fastests_laps, plot_positions_laps, plot_teams_speeds_laps
from functions_tab3 import plot_standings_by_teams, plot_standings_by_driver
import diskcache

"----------------------------------------------- Cache and variables --------------------------------------------------"
matplotlib.use('agg')
fastf1.Cache.enable_cache("./cache")
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
session = None
tab_test = None
"---------------------------------------------------- Dash - html -----------------------------------------------------"


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)
app.layout = dbc.Container([
    html.H1("Comparaison", className='mb-2', style={'textAlign': 'center'}),
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
            ])
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
        ]),
    ]),
])

"------------------------------------------------ Dash - functions ----------------------------------------------------"
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
    fig_teams_speeds = plot_teams_speeds_laps(race_session, year, race)

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


"---------------------------------------------- Launch Application ----------------------------------------------------"
if __name__ == '__main__':
    app.run_server(debug=True, port=8082)
