import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_auth
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}



external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets, dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Open Data Refresh Analytics Dashboard"
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.config.suppress_callback_exceptions = True

data = pd.read_csv("metrics.csv") 
data = data.drop(['threadID'], axis = 1, errors='coerce')
data = data.dropna()
data["Date"] = pd.to_datetime(data.time_started)
data["Agency"] = data["datasetName"].apply(lambda x: x.split('_', 1)[0])
