import dash
import fastf1.plotting
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import time
from dash import dcc, html
from dash.dependencies import Input, Output, State
import fastf1 as ff1
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib as mpl
import dash
import dash_bootstrap_components as dbc
import matplotlib                                # pip install matplotlib
matplotlib.use('agg')
import base64
from io import BytesIO
from dash.long_callback import DiskcacheLongCallbackManager
import dash._callback_context as ctx
## Diskcache
import diskcache
import plotly.graph_objects as go

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
session = None
tab_test = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], long_callback_manager=long_callback_manager)

app.layout = dbc.Container([
    html.H1("Comparaison", className='mb-2', style={'textAlign': 'center'}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Comparaison entre pilotes', value='tab-1', children=[
            html.Div([
                html.Br(),
                html.H3('Vue comparaison entre 2 pilotes', style={'margin-top': '10px'}),
                html.P("Dans cet onglet, les utilisateurs ont la possibilité de comparer les performances de deux pilotes lors d'une course spécifique. n cas d'erreur ou de problème lors du "
                       "chargement des données ou du traitement des informations, un message d'erreur explicite est affiché pour informer l'utilisateur de la situation, garantissant ainsi une expérience utilisateur transparente et informative.", style={'margin-top': '10px'}),
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
                            id='dropdown-1',
                            options=[
                                {'label': str(year), 'value': year} for year in range(1950, 2024)
                            ],
                            value=2023,
                            className='mb-3 mt-10'
                        )
                    ]),
                    dbc.Col([
                        dcc.Loading(
                            id='loading-dropdown-2',
                            type='default',
                            children=[dcc.Dropdown(id='dropdown-2', className='mb-3 mt-10')]
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
        dcc.Tab(label='Tab 2', value='tab-2', children=[
            html.Div([
                        html.H3('Welcome to Tab 2!',style={'margin-top': '10px'}),
                        html.P('This is a simple welcome message.')
                    ])
        ]),
    ]),
])
def time_consuming_function(selected_year, selected_month):
    # Simulate a time-consuming operation
    time.sleep(3)
    return [{'label': f'Day {day}', 'value': day} for day in range(1, 32)]

@app.callback(
    Output('loading-dropdown-2', 'children'),
    Output('dropdown-2', 'options'),
    Output('dropdown-2', 'value'),
    Input('dropdown-1', 'value')
)
def update_dropdown_2(selected_year):
    if selected_year is None:
        raise PreventUpdate
    print("------------------------------------------------------")
    print(selected_year)
    print("------------------------------------------------------")
    session = ff1.get_event_schedule(selected_year)['EventName']
    #session = ff1.get_event_schedule(2023)['Country']
    tab_countries = [i for i in session]
    #[{'label': list[i], 'value': i} for i in range(len(list))]
    return [dcc.Dropdown(id='dropdown-2', options=tab_countries, className='mb-3')], tab_countries, tab_countries[0]

@app.callback(
    Output('loading-dropdown-3', 'children'),
    Output('dropdown-3', 'options'),
    Output('dropdown-3', 'value'),
    Output("alert-no-fade", "is_open"),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value')
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
    if indices==None:
        indices=0

    try:
        session = ff1.get_session(selected_year, year_schedule[indices[0]], "R")
        session.load(telemetry=False, laps=False, weather=False)
        drivers = [i for i in session.drivers]
        drivers_name = [session.get_driver(i)["Abbreviation"] for i in drivers]
        return [dcc.Dropdown(id='dropdown-3', options=drivers_name, className='mb-3')], drivers_name, drivers_name[0], False
    except:
        return [dcc.Dropdown(id='dropdown-3', options=["None"], className='mb-3')], ["None"], ["None"], True


@app.callback(
    Output('loading-dropdown-4', 'children'),
    Output('dropdown-4', 'options'),
    Output('dropdown-4', 'value'),
    Output("alert-no-fade2", "is_open"),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value'),
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
        return [dcc.Dropdown(id='dropdown-4', options=drivers_name, className='mb-3')], drivers_name, drivers_name[1], False
    except:
        return [dcc.Dropdown(id='dropdown-4', options=["None"], className='mb-3')], ["None"], ["None"], False

@app.long_callback(
    output=[Output(component_id='bar-graph-matplotlib', component_property="src"),
            Output(component_id='overlaying', component_property="figure")],
    inputs=[Input("button_id", "n_clicks")],
    state=[State('dropdown-1', 'value'),
           State('dropdown-2', 'value'),
           State('dropdown-3', 'value'),
           State('dropdown-4', 'value')],
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("cancel_button_id", "disabled"), False, True),
    ],
    cancel=[Input("cancel_button_id", "n_clicks")],
)
def plot_data(n_clicks, year, race, driver1, driver2):
    #n_clicks, year, race, driver1, driver2
    print("PLOT DATA")
    fig_bar_matplotlib, overlaying = build_comparaison_tab(year, race, driver1, driver2)
    print("Done")
    return fig_bar_matplotlib, overlaying

def build_comparaison_tab(year, race, driver1, driver2):
    global session
    global tab_test
    print(tab_test)
    try:

        print(f"BEFORE : Values selected : {year} - {race} - {driver1} - {driver2}")

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

        print(f"AFTER : Values selected : {year} - {_1race} - {_driver1} - {_driver2}")
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
        lc = LineCollection(segments, cmap=mpl.colors.ListedColormap([fastf1.plotting.driver_color(_driver1), fastf1.plotting.driver_color(_driver2)]), norm=norm, linewidth=5)
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
        legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=mpl.colors.ListedColormap([fastf1.plotting.driver_color(_driver1), fastf1.plotting.driver_color(_driver2)]),
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
            name='VER',
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
if __name__ == '__main__':
    app.run_server(debug=True, port=8082)