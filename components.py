from dash import dcc, html

def create_navigation():
    """
    Navigation component: Includes stock input, date range, forecast days input, and action buttons.
    """
    return html.Div(
        [
            html.P("Welcome to the Stock Dash App!", className="start"),

            html.Div([
                dcc.Input(id='stock-code', type='text', placeholder='Enter stock code'),
                html.Button('Submit', id='submit-button')
            ], className="stock-input"),

            html.Div([
                dcc.DatePickerRange(
                    id='date-range',
                    start_date=dt(2020, 1, 1).date(),
                    end_date=dt.now().date(),
                    className='date-input'
                )
            ]),

            html.Div([
                html.Button('Get Stock Price', id='stock-price-button'),
                html.Button('Get Indicators', id='indicators-button'),
                dcc.Input(id='forecast-days', type='number', placeholder='Enter number of days'),
                html.Button('Get Forecast', id='forecast-button')
            ], className="selectors")
        ],
        className="nav"
    )


def create_content():
    """
    Content component: Displays the logo, company name, description, graphs, and forecast information.
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Img(id='logo', className='logo'),
                    html.H1(id='company-name', className='company-name')
                ],
                className="header"
            ),
            html.Div(id="description"),
            html.Div([], id="graphs-content"),
            html.Div([], id="main-content"),
            html.Div([], id="forecast-content")
        ],
        className="content"
    )
