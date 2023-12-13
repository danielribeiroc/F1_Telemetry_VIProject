import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager
import fastf1 as ff1
import plotly.graph_objects as go
import fastf1.plotting
import matplotlib
from functions_tab1 import build_comparaison_tab, load_f1_data
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
f1_logo_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/2560px-F1.svg.png"
additional_image_path = 'https://www.msengineering.ch/typo3conf/ext/msengineering/Resources/Public/Images/Logo/mse-full.svg'
"----------------------------------------------- Charge DATA - only cloud ---------------------------------------------"

# data = load_f1_data()

"---------------------------------------------------- Dash - html -----------------------------------------------------"

"----------------------- Modal vue --------------------------------"
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("A propos du projet")),
        dbc.ModalBody([
            html.P(
                "Ce projet a été créé en utilisant la librairie FastF1, une ressource dédiée à la fourniture de données et d'analyses pour la Formule 1."),
            html.P([
                "Pour plus d'informations, veuillez consulter la documentation officielle : ",
                html.A("https://docs.fastf1.dev/", href="https://docs.fastf1.dev/", target="_blank")
            ]),
            html.P(
                "Cette démonstration illustre l'interaction avec les graphiques. Un clic sur une légende permet de masquer ou d'afficher la variable correspondante. Un double-clic sur une légende masquera toutes les autres variables, permettant une analyse focalisée sur une variable spécifique.")
        ]),
        html.Div(children=[
            html.Video(
                controls=True,
                id='movie_player',
                src='./assets/f1_telemetry_tuto_720.mp4',
                autoPlay=False,
                style={
                    "width": "100%",
                    "height": "auto",
                    "maxWidth": "100%",
                    "maxHeight": "100%",
                    "padding": "10px",
                    "borderRadius": "15px"
                }
            ),
        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
        ),
    ],
    id="modal",
    is_open=False,
    size="lg"
)
"--------------------------------------------------------------------------"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=f1_logo_path, height="50px"), width=2, align='center'),
        dbc.Col(html.H1("Project VI : F1 - Telemetry", className='mb-2', style={'textAlign': 'center'}), width=7),
        dbc.Col(html.Img(src=additional_image_path, height="75px"), width=2, align='center')
    ], align='center', className='mb-4 mt-4'),
    html.Div([
        dbc.Button("▼", id="toggle-text-button", color="black", className="mb-3"),
        dbc.Collapse(
            html.Div(id="text-content", children=[
                html.P(
                    "Bienvenue sur la page web F1 - Telemetry."),
                html.P(
                    " Cette interface vise à fournir aux spectateurs de F1 des statistiques détaillées sur les courses, les pilotes, ainsi que les écuries. Pour une démonstration sur l'utilisation des graphiques interactifs, veuillez cliquer sur le bouton d'information situé en bas à gauche."),
                html.P(
                    "Trois onglets ont été créés, chacun se concentrant sur des thèmes distincts pour une exploration approfondie des données de la Formule 1."),
                html.P(
                    "N'hésitez pas à explorer ces onglets pour une expérience complète et immersive des statistiques et analyses de la F1.")
            ], style={'font-weight': 'bold'}),
            id='collapse'
        )
    ]),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Comparaison entre pilotes', value='tab-1', children=[
            html.Div([
                html.Br(),
                html.H3('Vue comparaison entre 2 pilotes', style={'margin-top': '10px'}),
                html.P(
                    "Dans cet onglet, les utilisateurs ont la possibilité de comparer les performances de deux pilotes lors d'une course spécifique. En cas d'erreur ou de problème lors du "
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
                dbc.Row([
                    dcc.Loading(
                        id="loading-overlaying",
                        children=[dcc.Graph(id="overlaying")],
                        type="circle",
                    )
                ]),
                dbc.Row([
                    dcc.Loading(
                        id="loading-bar_graph",
                        children=[html.Img(id='bar-graph-matplotlib')],
                        type="circle",
                    )
                ])
            ]),
            html.Div(
                dbc.Button(html.Img(src="https://cdn-icons-png.flaticon.com/512/0/472.png", height="30px"),
                           id="open-modal", n_clicks=0,
                           className="rounded-circle custom-hover-button",
                           style={"background-color": "white", "border-color": "black", "border-style": "solid"}),
                style={"position": "fixed", "bottom": 20, "left": 20, "width": "50px", "height": "50px"}
            ),
            modal,
            dbc.Row(
                dbc.Col(
                    html.Footer(
                        html.P(
                            "Created by Daniel Ribeiro Cabral & Ruben Terceiro - contact: daniel.ribeiroc@master.hes-so.ch"),
                        className="text-center text-muted"
                    ),
                    width=12
                ),
                className='mt-5'  # Adds top margin to the footer row
            )
        ]),
        dcc.Tab(label='Vue globale d\'un week-end de course', value='tab-2', children=[
            html.Div([
                html.H3('Analyse Dynamique et Résultats des Équipes durant les Courses', style={'margin-top': '10px'}),
                html.P(
                    "Cette section analyse les performances en course des pilotes et équipes avec un graphique montrant les écarts de temps et une boîte à moustaches pour les statistiques clés de chaque écurie, comme le temps moyen par tour, offrant ainsi une vue détaillée de la dynamique de course et des stratégies d'équipe.")
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
                dbc.Col([html.Button(id="button_id_2", children="Lancer l'analyse pour la session sélectionnée")]),
                dbc.Col([html.Button(id="cancel_button_id_2", children="Interrompre le processus")])
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
            ]), dbc.Row([
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
                        html.P(
                            "Created by Daniel Ribeiro Cabral & Ruben Terceiro - contact: ruben.terceiro@master.hes-so.ch"),
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
                        html.P(
                            "Created by Daniel Ribeiro Cabral & Ruben Terceiro - contact: daniel.ribeiroc@master.hes-so.ch"),
                        className="text-center text-muted"
                    ),
                    width=12
                ),
                className='mt-5'  # Adds top margin to the footer row
            )
        ]),
    ]),
])

"------------------------------------------------ Dash - functions ----------------------------------------------------"


@app.callback(
    [Output("collapse", "is_open"), Output("toggle-text-button", "children")],
    [Input("toggle-text-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_text(n, is_open):
    if n:
        return not is_open, "▲" if is_open else "▼"
    return is_open, "▼"


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
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('loading-dropdown-12', 'children'),
    Output('dropdown-12', 'options'),
    Output('dropdown-12', 'value'),
    Input('dropdown-11', 'value')
)
def update_dropdown_12(selected_year):
    tab_countries = get_years_selection(selected_year)
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
    output=[Output(component_id='fastests-laps', component_property="figure"),
            Output(component_id='positions-laps', component_property="figure"),
            Output(component_id='teams-speeds', component_property="figure")],
    inputs=[Input("button_id_2", "n_clicks")],
    state=[State("dropdown-21", "value"),
           State("dropdown-22", "value")],
    running=[(Output("button_id_2", "disabled"), True, False),
             (Output("cancel_button_id_2", "disabled"), False, True)
             ],
    cancel=[Input("cancel_button_id_2", "n_clicks")]
)
def plot_data_tab_2(n_clicks, year, race):
    print("PLOT DATA")
    if race == None:
        race = "Bahrain Grand Prix"

    fig_fastest_laps = go.Figure(layout={"title": {"text": f"No data for this stage of {race}"}})
    fig_positions_laps = go.Figure(layout={"title": {"text": f"No data for this stage of {race}"}})
    fig_teams_speeds = go.Figure(layout={"title": {"text": f"No data for this stage of {race}"}})

    try:

        fig_fastest_laps = plot_fastests_laps(year, race)
        fig_positions_laps = plot_positions_laps(year, race)
        fig_teams_speeds = plot_teams_speeds_laps(year, race)
    except Exception as e:
        # Handle the error here
        print(f"Error occurred: {e}")

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
    print("Starting Server !")
    app.run_server(debug=True, port=8082)
    # app.run_server(debug=True, host='0.0.0.0', port=9000)
