from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
configuration = swagger_client.Configuration()
configuration.access_token = '2cbdd91345bdcc4cc0c25903b0ad8294ef16c268'

# create an instance of the API class
api_instance = swagger_client.AthletesApi(swagger_client.ApiClient(configuration))
id = 157016614 # int | The identifier of the athlete. Must match the authenticated athlete.
page = 56 # int | Page number. (optional)
per_page = 30 # int | Number of items per page. Defaults to 30. (optional) (default to 30)

try:
    # Get Athlete Stats
    api_response = api_instance.get_stats(id, page=page, per_page=per_page)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AthletesApi->get_stats: %s\n" % e)

#f06153bd0a2f46f3cac30f0f5e3f8606190662c3
#157016614

#
import pandas as pd


try:
    pd.concat({k: pd.DataFrame(v).T for k, v in api_response.items()}, axis = 0)
except AttributeError:
    print('Cannot print more')


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

# Sample data from the API response
data = {'all_ride_totals': {'achievement_count': None, 'count': 1, 'distance': 2324.0, 'elapsed_time': 3183, 'elevation_gain': 15.716666221618652, 'moving_time': 1189}, 'all_run_totals': {'achievement_count': None, 'count': 1, 'distance': 2948.300048828125, 'elapsed_time': 7401, 'elevation_gain': 5.007843017578125, 'moving_time': 7353}, 'all_swim_totals': {'achievement_count': None, 'count': 0, 'distance': 0.0, 'elapsed_time': 0, 'elevation_gain': 0.0, 'moving_time': 0}, 'biggest_climb_elevation_gain': 5.299999999999997, 'biggest_ride_distance': 2324.0, 'recent_ride_totals': {'achievement_count': 0, 'count': 1, 'distance': 2324.0, 'elapsed_time': 3183, 'elevation_gain': 15.716666221618652, 'moving_time': 1189}, 'recent_run_totals': {'achievement_count': 0, 'count': 1, 'distance': 2948.300048828125, 'elapsed_time': 7401, 'elevation_gain': 5.007843017578125, 'moving_time': 7353}, 'recent_swim_totals': {'achievement_count': 0, 'count': 0, 'distance': 0.0, 'elapsed_time': 0, 'elevation_gain': 0.0, 'moving_time': 0}, 'ytd_ride_totals': {'achievement_count': None, 'count': 1, 'distance': 2324.0, 'elapsed_time': 3183, 'elevation_gain': 15.716666221618652, 'moving_time': 1189}, 'ytd_run_totals': {'achievement_count': None, 'count': 1, 'distance': 2948.0, 'elapsed_time': 7401, 'elevation_gain': 5.007843017578125, 'moving_time': 7353}, 'ytd_swim_totals': {'achievement_count': None, 'count': 0, 'distance': 0.0, 'elapsed_time': 0, 'elevation_gain': 0.0, 'moving_time': 0}}

# Prepare data for visualization
def prepare_activity_data(api_response):
    activities = ['ride', 'run', 'swim']
    periods = ['recent', 'ytd', 'all']
    
    prepared_data = []
    for period in periods:
        for activity in activities:
            key = f'{period}_{activity}_totals'
            if key in api_response:
                activity_data = data[key]
                prepared_data.append({
                    'Period': period.upper(),
                    'Activity': activity.capitalize(),
                    'Distance': activity_data['distance'],
                    'Count': activity_data['count'],
                    'Elevation Gain': activity_data['elevation_gain'],
                    'Moving Time': activity_data['moving_time']
                })
    
    return pd.DataFrame(prepared_data)

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Strava Activity Dashboard'),
    
    # Dropdown for metric selection
    html.Div([
        html.Label('Select Metric:'),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Distance', 'value': 'Distance'},
                {'label': 'Count', 'value': 'Count'},
                {'label': 'Elevation Gain', 'value': 'Elevation Gain'},
                {'label': 'Moving Time', 'value': 'Moving Time'}
            ],
            value='Distance',
            clearable=False
        )
    ]),
    
    # Bar chart
    dcc.Graph(id='activity-bar-chart'),
    
    # Additional key metrics
    html.Div([
        html.H3('Key Metrics'),
        html.P(f"Biggest Climb Elevation Gain: {data['biggest_climb_elevation_gain']} m"),
        html.P(f"Biggest Ride Distance: {data['biggest_ride_distance']} m")
    ])
])

# Callback to update bar chart
@app.callback(
    Output('activity-bar-chart', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_graph(selected_metric):
    df = prepare_activity_data(data)
    
    fig = px.bar(
        df, 
        x='Activity', 
        y=selected_metric, 
        color='Period',
        barmode='group',
        title=f'{selected_metric} by Activity and Period'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)