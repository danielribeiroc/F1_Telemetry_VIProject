import dash
import fastf1.plotting
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import time

from dash import dcc, html
from dash.dependencies import Input, Output
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

session = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Comparaison", className='mb-2', style={'textAlign': 'center'}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Comparaison entre pilotes', value='tab-1', children=[
            html.Div([
                html.Br(),
                html.H3('Welcome to Tab 2!', style={'margin-top': '10px'}),
                html.Br(),
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
            ])
        ]),
        dcc.Tab(label='Tab 2', value='tab-2', children=[
            html.Div([
                        html.H3('Welcome to Tab 2!',style={'margin-top': '10px'}),
                        html.P('This is a simple welcome message.')
                    ])
        ]),
    ]),
    dbc.Row([
        #html.Button('Submit', id='submit-val', n_clicks=0),
    ]),
    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ], width=12)
    ])
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
    session = ff1.get_event_schedule(selected_year)['Country']
    # session = ff1.get_session(year, wknd, ses)
    # weekend = session.event
    # session.load()
    session = ff1.get_event_schedule(2023)['Country']
    tab_countries = [i for i in session]
    return [dcc.Dropdown(id='dropdown-2', options=tab_countries, className='mb-3')], tab_countries, tab_countries[0]

@app.callback(
    Output('loading-dropdown-3', 'children'),
    Output('dropdown-3', 'options'),
    Output('dropdown-3', 'value'),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value')
)
def update_dropdown_3(selected_year, selected_month):
    global session
    if selected_month is None:
        raise PreventUpdate

    year_schedule = ff1.get_event_schedule(selected_year)['Country']
    indices = [index for index, country in enumerate(year_schedule) if country == selected_month]
    session = ff1.get_session(selected_year, year_schedule[indices[0]], "R")
    session.load(telemetry=False, laps=False, weather=False)
    drivers = [i for i in session.drivers]
    drivers_name = [session.get_driver(i)["Abbreviation"] for i in drivers]
    return [dcc.Dropdown(id='dropdown-3', options=drivers_name, className='mb-3')], drivers_name, drivers_name[0]

@app.callback(
    Output('loading-dropdown-4', 'children'),
    Output('dropdown-4', 'options'),
    Output('dropdown-4', 'value'),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value'),
    Input('dropdown-3', 'value')
)
def update_dropdown_4(selected_year, selected_month, selected_day):
    global session
    if selected_day is None:
        raise PreventUpdate
    session.load(telemetry=False, laps=False, weather=False)
    drivers = [i for i in session.drivers]
    drivers_name = [session.get_driver(i)["Abbreviation"] for i in drivers]
    return [dcc.Dropdown(id='dropdown-4', options=drivers_name, className='mb-3')], drivers_name, drivers_name[1]
@app.callback(
    Output(component_id='bar-graph-matplotlib', component_property="src"),
    Input('dropdown-1', 'value'),
    Input('dropdown-2', 'value'),
    Input('dropdown-3', 'value'),
    Input('dropdown-4', 'value')
)
def plot_data(year, race, driver1, driver2):
    print("PLOT DATA")
    fig_bar_matplotlib = build_comparaison_tab(year, race, driver1, driver2)
    print("FIG BAR - Done")
    return fig_bar_matplotlib

def build_comparaison_tab(year, race, driver1, driver2):
    global session
    year_schedule = ff1.get_event_schedule(year)['Country']
    indices = [index for index, country in enumerate(year_schedule) if country == race]
    _race = year_schedule[indices[0]]
    session = ff1.get_session(year, _race, "R")
    session.load(telemetry=True, laps=True, weather=False)
    lap_driver1 = session.laps.pick_driver(driver1).pick_fastest()
    lap_driver2 = session.laps.pick_driver(driver2).pick_fastest()
    # Calculate lap times for both drivers
    lap = lap_driver1
    lap_time_driver1 = lap_driver1.telemetry['Time'].values
    lap_time_driver2 = lap_driver2.telemetry['Time'].values
    who_fastest = []
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
    fig.suptitle(f'{race} - {year} - {driver1} vs {driver2} - Speed', size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    mask = np.array(who_fastest)  # Repeat each element 10 times for each sector

    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
    norm = plt.Normalize(0, 1)
    # Set the color based on the mask
    lc = LineCollection(segments, cmap=mpl.colors.ListedColormap([fastf1.plotting.driver_color(driver1), fastf1.plotting.driver_color(driver2)]), norm=norm, linewidth=5)
    lc.set_array(mask)

    # Set the values used for colormapping
    lc.set_array(mask)

    # Merge all line segments together
    line = ax.add_collection(lc)

    # Finally, we create a color bar as a legend.
    # Create a color bar as a legend.
    cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
    normlegend = mpl.colors.Normalize(vmin=0, vmax=1)  # Assuming 'who_fastest' contains True and False values
    legend_labels = [f"Driver {driver1} Fastest", f"Driver {driver2} Fastest"]
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=mpl.colors.ListedColormap([fastf1.plotting.driver_color(driver1), fastf1.plotting.driver_color(driver2)]),
                                       orientation="horizontal", ticks=[0, 1])
    legend.set_ticklabels(legend_labels)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

    return fig_bar_matplotlib

if __name__ == '__main__':
    app.run_server(debug=True, port=8082)