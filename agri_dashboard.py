import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load dataset
df = pd.read_excel("crop_factor.xlsx")  # Change filename if needed

# Convert 'Year' column to datetime format and set it as index
df['Year'] = pd.to_datetime(df['Year'], format='%Y')
df.set_index('Year', inplace=True)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Agricultural Production Dashboard", style={'textAlign': 'center', 'color': '#4CAF50'}),

    # Dropdown to select year
    html.Label("Select Year:", style={'fontSize': '18px', 'margin': '10px'}),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in df.index.year.unique()],
        value=df.index.year.max(),  # Default to latest year
        clearable=False,
        style={'width': '50%', 'margin': 'auto'}
    ),

    # Top Panel showing last year's production, rainfall, and avg temperature
    html.Div([
        html.Div([
            html.H3("Last Year Data", style={'color': '#333'}),
            html.H4(id='last-year-data', style={'fontSize': '22px', 'color': '#555'}),
        ], style={'padding': '20px', 'backgroundColor': '#f4f4f4', 'borderRadius': '10px', 'textAlign': 'center'})
    ], style={'width': '40%', 'margin': 'auto', 'marginTop': '20px'}),

    # Graphs Layout
    html.Div([
        dcc.Graph(id='production-graph'),
        dcc.Graph(id='yield-graph'),
        dcc.Graph(id='rainfall-graph'),
        dcc.Graph(id='temp-graph'),
        dcc.Graph(id='area-harvested-graph'),
        dcc.Graph(id='avg-min-temp-graph'),
        dcc.Graph(id='avg-max-temp-graph')
    ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'padding': '20px'})
])

# Callback function to update graphs
@app.callback(
    [Output('production-graph', 'figure'),
     Output('yield-graph', 'figure'),
     Output('rainfall-graph', 'figure'),
     Output('temp-graph', 'figure'),
     Output('area-harvested-graph', 'figure'),
     Output('avg-min-temp-graph', 'figure'),
     Output('avg-max-temp-graph', 'figure'),
     Output('last-year-data', 'children')],
    [Input('year-dropdown', 'value')]
)
def update_graphs(selected_year):
    filtered_data = df[df.index.year <= selected_year]

    # Production Graph
    production_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Production'], mode='lines+markers', marker=dict(color='blue'))])
    production_fig.update_layout(title="Production vs Year", xaxis_title="Year", yaxis_title="Production (Million Tons)", template="plotly_white")

    # Yield Graph
    yield_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Yield'], mode='lines+markers', marker=dict(color='green'))])
    yield_fig.update_layout(title="Yield vs Year", xaxis_title="Year", yaxis_title="Yield (Tons per Hectare)", template="plotly_white")

    # Rainfall Graph
    rainfall_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Rainfall'], mode='lines+markers', marker=dict(color='orange'))])
    rainfall_fig.update_layout(title="Rainfall vs Year", xaxis_title="Year", yaxis_title="Rainfall (mm)", template="plotly_white")

    # Average Temperature Graph
    temp_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Avg Temp'], mode='lines+markers', marker=dict(color='red'))])
    temp_fig.update_layout(title="Average Temperature vs Year", xaxis_title="Year", yaxis_title="Avg Temp (°C)", template="plotly_white")

    # Area Harvested Graph
    area_harvested_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Area Harvested'], mode='lines+markers', marker=dict(color='purple'))])
    area_harvested_fig.update_layout(title="Area Harvested vs Year", xaxis_title="Year", yaxis_title="Area (Hectares)", template="plotly_white")

    # Avg Min Temp Graph
    avg_min_temp_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Avg Min Temp'], mode='lines+markers', marker=dict(color='cyan'))])
    avg_min_temp_fig.update_layout(title="Avg Min Temp vs Year", xaxis_title="Year", yaxis_title="Avg Min Temp (°C)", template="plotly_white")

    # Avg Max Temp Graph
    avg_max_temp_fig = go.Figure(data=[go.Scatter(x=filtered_data.index, y=filtered_data['Avg Max Temp'], mode='lines+markers', marker=dict(color='magenta'))])
    avg_max_temp_fig.update_layout(title="Avg Max Temp vs Year", xaxis_title="Year", yaxis_title="Avg Max Temp (°C)", template="plotly_white")

    # Display last year's production, rainfall, and avg temp
    last_year = df[df.index.year == selected_year].iloc[-1]
    last_year_data = f"Production: {last_year['Production']} | Rainfall: {last_year['Rainfall']} | Avg Temp: {last_year['Avg Temp']}"

    return production_fig, yield_fig, rainfall_fig, temp_fig, area_harvested_fig, avg_min_temp_fig, avg_max_temp_fig, last_year_data

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
