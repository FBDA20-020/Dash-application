import dash
import dash_auth
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load web server logs CSV file
def load_logs(filename):
    try:
        df = pd.read_csv('web_server_log.csv')
        return df
    except FileNotFoundError:
        print(f"File {'web_server_log.csv'} not found. Please ensure the file exists and the path is correct.")
        return pd.DataFrame()

# Mock function to map IP to country for demonstration purposes
def get_country_from_ip(ip):
    country_mapping = {
        "228.10.0.1": "USA",
        "155.55.0.24": "Canada",
        "157.20.30.10": "UK",
        "172.16.0.1": "Australia",
        "201.24.35.67": "Brazil",
        "89.23.45.67": "Germany",
        "120.25.45.67": "Japan",
        "203.0.113.0": "India",
        "54.240.196.186": "Netherlands",
        "203.0.113.195": "South Africa",
        # Add more mappings here
    }
    return country_mapping.get(ip, "Unknown")

# Function to map country to continent
def get_continent_from_country(country):
    continent_mapping = {
        "USA": "North America",
        "Canada": "North America",
        "UK": "Europe",
        "Australia": "Oceania",
        "Brazil": "South America",
        "Germany": "Europe",
        "Japan": "Asia",
        "India": "Asia",
        "Netherlands": "Europe",
        "South Africa": "Africa",
        # Add more mappings here
    }
    return continent_mapping.get(country, "Unknown")

# Define username and password
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'password'
}

# Create Dash app
app = dash.Dash(__name__)
server = app.server
# Add basic auth to the app
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# Load web server logs data
logs_df = load_logs('web_server_log.csv')

# Preprocess logs data
def preprocess_logs(logs_df):
    if logs_df.empty:
        return logs_df
    # Convert Timestamp column to datetime format
    logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
    # Extract hour of the day
    logs_df['Hour'] = logs_df['Timestamp'].dt.hour
    # Map IP addresses to countries
    logs_df['Country'] = logs_df['IP'].apply(get_country_from_ip)
    # Map countries to continents
    logs_df['Continent'] = logs_df['Country'].apply(get_continent_from_country)
    # Extract sport from URL
    logs_df['Sport'] = logs_df['URL'].apply(lambda x: x.split('/')[-1].split('.')[0])
    return logs_df

# Preprocess logs data
logs_df = preprocess_logs(logs_df)

# Define app layout
app.layout = html.Div([
    html.H1("Elite Sports Olympic Games Broadcasting Platform Analysis"),

    html.Div([
        html.Label("Select a metric to analyze:"),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Average Viewership for Concurrently Running Sports', 'value': 'avg_viewership'},
                {'label': 'Sporting Events Distribution by Continent', 'value': 'events_distribution'},
                {'label': 'Viewership vs Demographic Variables by Continent', 'value': 'viewership_demographics'},
                {'label': 'Geographic Distribution of Viewership', 'value': 'world_map'},
                {'label': 'Heatmap: Gender vs. Viewership', 'value': 'heatmap_gender_viewership'},
                {'label': 'Viewership Time Distribution by Sporting Events', 'value': 'viewership_time_distribution'},
            ],
            value='avg_viewership'
        ),
    ]),

    dcc.Graph(id='chart')
])

# Callback to update chart based on selected metric
@app.callback(
    Output('chart', 'figure'),
    [Input('metric-dropdown', 'value')]
)
def update_chart(metric):
    if logs_df.empty:
        return go.Figure()

    if metric == 'avg_viewership':
        avg_viewership_per_sport = logs_df.groupby('Sport')['IP'].nunique().reset_index()
        avg_viewership_per_sport.columns = ['Sport', 'Average Viewership']
        fig = px.pie(avg_viewership_per_sport, names='Sport', values='Average Viewership', title='Average Viewership for Concurrently Running Sports')
    elif metric == 'events_distribution':
        sport_distribution_data = calculate_sport_distribution()
        fig = px.bar(sport_distribution_data, x='Sport', y='Count', title='Sporting Events Distribution by Continent')
    elif metric == 'viewership_demographics':
        viewership_demographics = logs_df.groupby(['Country', 'Sport']).size().reset_index(name='Count')
        fig = px.scatter(viewership_demographics, x='Country', y='Sport', size='Count', color='Country', title='Viewership vs Demographic Variables by Continent')
    elif metric == 'world_map':
        viewership_data = logs_df.groupby(['Continent', 'Country', 'Sport'])['IP'].nunique().reset_index()
        fig = px.choropleth(viewership_data,
                            locations='Country',
                            locationmode='country names',
                            color='IP',
                            hover_name='Country',
                            hover_data={'Continent': True, 'Sport': True},
                            title='Geographic Distribution of Viewership by Sporting Event and Continent')
    elif metric == 'heatmap_gender_viewership':
        gender_viewership = logs_df.groupby(['Gender', 'Sport']).size().reset_index(name='Count')
        fig = px.density_heatmap(gender_viewership, x='Gender', y='Sport', z='Count', title='Heatmap: Gender vs. Viewership')
    elif metric == 'viewership_time_distribution':
        time_distribution = logs_df.groupby(['Hour', 'Sport']).size().reset_index(name='Count')
        fig = px.bar(time_distribution, x='Hour', y='Count', color='Sport', title='Viewership Time Distribution by Sporting Events')
    else:
        fig = go.Figure()

    return fig

# Function to calculate sport distribution
def calculate_sport_distribution():
    sport_distribution = logs_df['Sport'].value_counts().reset_index()
    sport_distribution.columns = ['Sport', 'Count']
    return sport_distribution

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


