from datetime import datetime
import base64
import numpy as np
from io import BytesIO
import fastf1 as ff1
import fastf1.plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import plotly.graph_objects as go

session = None
tab_test = None
data_loaded = False

def load_f1_data(start_year=2019): # this step will take a certain time to end and will only be executed one time in the cloud
    global data_loaded

    # Check if data is already loaded
    if data_loaded:
        return
    current_year = datetime.now().year
    all_sessions = []
    for year in range(start_year, current_year + 1):
        for gp in ff1.get_event_schedule(year).itertuples():

            print(f"Loading data for {year} {gp.EventName} Qualification")
            qualifying = ff1.get_session(year, gp.EventName, 'Q').load()
            all_sessions.append(qualifying)

            print(f"Loading data for {year} {gp.EventName} Race")
            race = ff1.get_session(year, gp.EventName, 'R').load()
            all_sessions.append(race)
    data_loaded = True

    return all_sessions



# --------------------------------------------------------------------------------------------------------------------------------


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