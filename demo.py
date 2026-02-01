import dash
from dash import dcc, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from datetime import datetime as dt
import yfinance as yf
import pandas as pd
import plotly.express as px

# Import components and prediction function
from components import create_navigation, create_content
from model import prediction

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=['assets/styles.css'])
server = app.server

# Set the layout
app.layout = html.Div(className='container', children=[
    create_navigation(),  # Navigation Component
    create_content()  # Content Component
])

# Callbacks for stock info and details
@app.callback(
    [
        Output("description", "children"),
        Output("logo", "src"),
        Output("company-name", "children"),
        Output("stock-price-button", "n_clicks"),
        Output("indicators-button", "n_clicks"),
        Output("forecast-button", "n_clicks")
    ],
    [Input("submit-button", "n_clicks")],
    [State("stock-code", "value")]
)
def update_data(n_clicks, stock_code):
    if n_clicks is None or stock_code is None:
        raise PreventUpdate
    else:
        ticker = yf.Ticker(stock_code)
        info = ticker.info

        if 'logo_url' not in info:
            return None, None, None, None, None, None
        else:
            return info['longBusinessSummary'], info['logo_url'], info['longName'], None, None, None


# Callback for displaying stock price graphs
@app.callback(
    [Output("graphs-content", "children")],
    [
        Input("stock-price-button", "n_clicks"),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ],
    [State("stock-code", "value")]
)
def stock_price(n_clicks, start_date, end_date, stock_code):
    if n_clicks is None or stock_code is None:
        raise PreventUpdate

    df = yf.download(stock_code, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    fig = px.line(df, x="Date", y=["Close", "Open"], title="Stock Price: Closing and Opening Prices vs Date")
    return [dcc.Graph(figure=fig)]


# Callback for displaying stock indicators
@app.callback(
    [Output("main-content", "children")],
    [
        Input("indicators-button", "n_clicks"),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ],
    [State("stock-code", "value")]
)
def indicators(n_clicks, start_date, end_date, stock_code):
    if n_clicks is None or stock_code is None:
        raise PreventUpdate

    df = yf.download(stock_code, start=start_date, end=end_date)
    df.reset_index(inplace=True)

    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.line(df, x="Date", y="EWA_20", title="Exponential Moving Average (20-day) vs Date")
    return [dcc.Graph(figure=fig)]


# Callback for stock forecast
@app.callback(
    [Output("forecast-content", "children")],
    [Input("forecast-button", "n_clicks")],
    [State("forecast-days", "value"),
     State("stock-code", "value")]
)
def forecast(n_clicks, days, stock_code):
    if n_clicks is None or days is None or stock_code is None:
        raise PreventUpdate

    fig = prediction(stock_code, int(days))
    return [dcc.Graph(figure=fig)]


if __name__ == '__main__':
    app.run_server(debug=True)
