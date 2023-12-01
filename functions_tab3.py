import pandas as pd
from fastf1.ergast import Ergast
import plotly.express as px

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