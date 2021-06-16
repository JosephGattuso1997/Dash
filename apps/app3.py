import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash_auth
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
import requests

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
                        html.Div(children="agency", className="menu-title"),
                        dcc.Dropdown(
                            id="agency-filter",
                            options=[{"label": agency, "value": agency} for agency in data.Agency],
                            value="ITS",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                )
            ],
            className="menu",
        ),
        
        html.Div(
            children=[
                html.Div(children=[
                    dt.DataTable(id='table-container', columns=[{'id': c, 'name': c} for c in data.columns.values],style_table={'overflowX': 'scroll'},page_size=25,)
                    ],

                className="card",)
            ],
        className="wrapper",
        
        )

    ]
)

@app.callback(  
    Output("table-container", "data"),
    [
    Input("agency-filter", "value"),
    ],
)
def update_rows(agency):
    dff = data[data.Agency == agency]
    return dff.to_dict('records')