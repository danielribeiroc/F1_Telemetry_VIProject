import pandas as pd
from fastf1.ergast import Ergast
import plotly.express as px


def plot_standings_by_driver(SEASON):
    csv_filepath = f"./data_tab_3/f1_standings_{SEASON}.csv"

    try:
        results_df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"CSV file for season {SEASON} not found in './data_tab_3'.")
        return None

    # Data manipulation for plotting (assuming the CSV has the correct format)
    races = results_df['race'].drop_duplicates()
    results_df = results_df.pivot(index='driverCode', columns='round', values='points')

    # Rank the drivers by their total points
    results_df['total_points'] = results_df.sum(axis=1)
    results_df = results_df.sort_values(by='total_points', ascending=False)
    results_df.drop(columns='total_points', inplace=True)

    # Use race name, instead of round no., as column names
    results_df.columns = races
    fig = px.imshow(
        results_df,
        text_auto=True,
        aspect='auto',  # Automatically adjust the aspect ratio
        color_continuous_scale=[[0, 'rgb(198, 219, 239)'],  # Blue scale
                                [0.25, 'rgb(107, 174, 214)'],
                                [0.5, 'rgb(33,  113, 181)'],
                                [0.75, 'rgb(8,   81,  156)'],
                                [1, 'rgb(8,   48,  107)']],
        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}  # Change hover texts
    )
    fig.update_xaxes(title_text='')  # Remove axis titles
    fig.update_yaxes(title_text='')
    fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey',
                     showline=False, tickson='boundaries')  # Show horizontal grid only
    fig.update_xaxes(showgrid=False, showline=False)  # And remove vertical grid
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')  # White background
    fig.update_layout(coloraxis_showscale=False)  # Remove legend
    fig.update_layout(xaxis=dict(side='top'))  # x-axis on top
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
    return fig


def plot_standings_by_teams(Year):
    csv_filepath = f"./data_tab_3/f1_team_standings_{Year}.csv"

    try:
        results = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"CSV file for season {Year} not found in '../data_tab_3'.")
        return None

    races = results['race'].drop_duplicates()
    test = results.groupby(["round", "race", "constructorName"]).sum().reset_index()
    results = test.pivot(index='constructorName', columns='race', values='points')
    results['total_points'] = results.sum(axis=1)
    results = results.sort_values(by='total_points', ascending=False)
    results.drop(columns='total_points', inplace=True)

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