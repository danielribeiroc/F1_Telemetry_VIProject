import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import fastf1 as ff1
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib as mpl
import mpld3
import plotly.graph_objects as go
import dash_ag_grid as dag
import dash
import dash_bootstrap_components as dbc
import matplotlib                                # pip install matplotlib
matplotlib.use('agg')
import base64
from io import BytesIO
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# -----------------------------------------
content = 0
year = 2022
wknd = 1
ses = 'R'
driver1 = 'LEC'
driver2 = 'NOR'
colormap = mpl.cm.plasma

session = ff1.get_session(year, wknd, ses)
weekend = session.event
session.load()
# -----------------------------------------

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
app.layout = dbc.Container([
    html.H1("Interactive Matplotlib with Dash", className='mb-2', style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='category',  # Dropdown component with the ID 'category'
        options=[
            {'label': 'Option 1', 'value': 'option1'},
            {'label': 'Option 2', 'value': 'option2'}
        ],
        value='option1',  # Default selected value
        className='mb-3'
    ),

    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ], width=12)
    ]),
])

# Create interactivity between dropdown component and graph
@app.callback(
    Output(component_id='bar-graph-matplotlib', component_property="src"),
    Input('category', 'value'),
)
def plot_data(selected_yaxis):
    fig_bar_matplotlib = build_comparaison_tab()
    return fig_bar_matplotlib


def build_comparaison_tab():
    # Get telemetry data for both drivers
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
    fig.suptitle(f'{weekend.name} - {year} - {driver1} vs {driver2} - Speed', size=24, y=0.97)

    # Adjust margins and turn of axis
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
    ax.axis('off')

    mask = np.array(who_fastest)  # Repeat each element 10 times for each sector

    # After this, we plot the data itself.
    # Create background track line
    ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
    norm = plt.Normalize(0, 1)
    # Set the color based on the mask
    lc = LineCollection(segments, cmap=mpl.colors.ListedColormap(['red', 'green']), norm=norm, linewidth=5)
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
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=mpl.colors.ListedColormap(['red', 'green']),
                                       orientation="horizontal", ticks=[0, 1])
    legend.set_ticklabels(legend_labels)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

    return fig_bar_matplotlib

if __name__ == "__main__":
    app.run_server(port=8080)
