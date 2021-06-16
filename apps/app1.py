import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_auth
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd


from app import app, data




layout = html.Div(
    children=[
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/page-1"), id="page-1-link"),
                dbc.NavItem(dbc.NavLink("Agency", href="/page-2"), id="page-2-link")
                ],
                brand="Open Data Metrics",
                brand_href="/",
                color="#222222",
                dark=True,
                 ),
        html.Div(
            children=[
                html.P(children="NYSITS", className="header-emoji"),
                html.H1(
                    children="Dataset Refresh Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of the Python Refresh Process"
                    " and the number of rows effected in a dataset",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region} for region in data.datasetName
                            ],
                            value="ITS_ACTIVITYLOGDATASET",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="metric", className="menu-title"),
                        dcc.Dropdown(
                            id="metric-filter",
                            options=[
                                {"label": metric, "value": metric} for metric in ['Created','Updated','Deleted']],
                            value="Created",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ]),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="update-chart", config={"displayModeBar": False}
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="speed-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [Output("price-chart", "figure"), Output("update-chart", "figure"), Output("speed-chart", "figure"),],
    [
        Input("region-filter", "value"),
        Input("metric-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),

    ])
def update_charts(region, metric, start_date, end_date):
    mask = (
        (data.datasetName == region)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]
    price_chart_figure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data[metric],
                "type": "lines",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Rows Created",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    UpdatedFigure = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": filtered_data[metric],
                "type": "bar",
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Rows Updated",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    speed = {
        "data": [
            {
                "x": filtered_data["Date"],
                "y": pd.to_datetime(filtered_data["time_finished"], errors='coerce') - pd.to_datetime(filtered_data["time_started"], errors='coerce'),
                "type": "lines",
                "hovertemplate": "%{y}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Time for Update",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    return price_chart_figure, UpdatedFigure, speed