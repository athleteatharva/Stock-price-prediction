import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.svm import SVR
import plotly.graph_objs as go

def prediction(stock_code, days):
    # Fetch the stock data
    df = yf.download(stock_code, period="1y")
    df.reset_index(inplace=True)

    # Prepare data for prediction
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = np.arange(len(df))  # Adding a day count
    X = df['Day'].values.reshape(-1, 1)
    y = df['Close'].values

    # Train the SVR model
    model = SVR(kernel='rbf', C=1e3, gamma=0.1)
    model.fit(X, y)

    # Predict future stock prices
    future_days = np.arange(len(df), len(df) + days).reshape(-1, 1)
    predictions = model.predict(future_days)

    # Create forecast DataFrame
    future_dates = pd.date_range(df['Date'].max(), periods=days + 1)[1:]
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted Close': predictions
    })

    # Create plotly graph object
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Actual Close'))
    fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Predicted Close'], mode='lines', name='Predicted Close', line=dict(dash='dot')))

    fig.update_layout(title=f"Stock Price Prediction for {stock_code}", xaxis_title="Date", yaxis_title="Price")
    return fig
