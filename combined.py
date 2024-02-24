import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
# from fbprophet import Prophet
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
import requests
from transformers import pipeline
import matplotlib.pyplot as plt
import streamlit as st


# List of Nifty Fifty companies
nifty_fifty_companies = [
    'ADANIPORTS.NS', 'ASIANPAINT.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS',
    'BAJFINANCE.NS', 'BHARTIARTL.NS', 'BPCL.NS', 'CIPLA.NS', 'COALINDIA.NS',
    'DIVISLAB.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS',
    'HDFC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS',
    'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS', 'INFY.NS', 'IOC.NS',
    'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS', 'M&M.NS',
    'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS',
    'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SUNPHARMA.NS',
    'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS',
    'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS'
]

d={'ADANIPORTS.NS': 'Adani Ports',
 'ASIANPAINT.NS': 'Asian Paints',
 'AXISBANK.NS': 'Axis Bank',
 'BAJAJ-AUTO.NS': 'Bajaj Auto',
 'BAJAJFINSV.NS': 'Bajaj Finserv',
 'BAJFINANCE.NS': 'Bajaj Finance',
 'BHARTIARTL.NS': 'Bharti Airtel',
 'BPCL.NS': 'BPCL',
 'CIPLA.NS': 'Cipla',
 'COALINDIA.NS': 'Coal India',
 'DIVISLAB.NS': 'Divis Laboratories',
 'DRREDDY.NS': "Dr. Reddy's",
 'EICHERMOT.NS': 'Eicher Motors',
 'GRASIM.NS': 'Grasim',
 'HCLTECH.NS': 'HCL Tech',
 'HDFC.NS': 'HDFC',
 'HDFCBANK.NS': 'HDFC Bank',
 'HDFCLIFE.NS': 'HDFC Life',
 'HEROMOTOCO.NS': 'Hero MotoCorp',
 'HINDALCO.NS': 'Hindalco',
 'HINDUNILVR.NS': 'Hindustan Unilever',
 'ICICIBANK.NS': 'ICICI Bank',
 'INDUSINDBK.NS': 'IndusInd Bank',
 'INFY.NS': 'Infosys',
 'IOC.NS': 'IOC',
 'ITC.NS': 'ITC',
 'JSWSTEEL.NS': 'JSW Steel',
 'KOTAKBANK.NS': 'Kotak Mahindra Bank',
 'LT.NS': 'Larsen & Toubro',
 'M&M.NS': 'Mahindra & Mahindra',
 'MARUTI.NS': 'Maruti Suzuki',
 'NESTLEIND.NS': 'Nestle India',
 'NTPC.NS': 'NTPC',
 'ONGC.NS': 'ONGC',
 'POWERGRID.NS': 'Power Grid',
 'RELIANCE.NS': 'Reliance Industries',
 'SBILIFE.NS': 'SBI Life',
 'SBIN.NS': 'State Bank of India',
 'SHREECEM.NS': 'Shree Cement',
 'SUNPHARMA.NS': 'Sun Pharma',
 'TATAMOTORS.NS': 'Tata Motors',
 'TATASTEEL.NS': 'Tata Steel',
 'TCS.NS': 'TCS',
 'TECHM.NS': 'Tech Mahindra',
 'TITAN.NS': 'Titan',
 'ULTRACEMCO.NS': 'UltraTech Cement',
 'UPL.NS': 'UPL',
 'WIPRO.NS': 'Wipro'}

# Function to get news for a given company
def get_news(query):
    secret = "1593ff28bfbd4e518d098c0981e6abce"
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': query,
        'pageSize': 100,
        'apiKey': secret
    }
    response = requests.get(url, params=parameters)
    response_json = response.json()['articles']
    title = []
    date = []
    source = []
    for i in response_json:
        title.append(i['title'])
        date.append(i['publishedAt'].split('T')[0])
        source.append(i['source']['name'])
    df = pd.DataFrame()
    df['Title'] = title
    df['Date'] = date
    df['Source'] = source
    df['Topic'] = [query] * len(title)
    return df

def candlestick(ticker):
    df = yf.download(ticker, start="2018-01-01", period="max", interval="1d")
    df = df.reset_index()
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])

    fig.update_layout(title=f'Candlestick Chart for {ticker}',
                      xaxis_title='Date',
                      yaxis_title='Price')

    return fig

def get_info(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        market_cap = stock.info["marketCap"]
        pe_ratio = stock.info["forwardPE"]
        current_price = stock.info["currentPrice"]
        book_value = stock.info["bookValue"]
        dividend_yield = stock.info["dividendYield"]
        de_ratio = stock.info["debtToEquity"]
        return market_cap,pe_ratio,current_price,de_ratio,book_value,dividend_yield
    except:
        market_cap = " "
        pe_ratio = " "
        current_price = " "
        book_value = " "
        dividend_yield = " "
        de_ratio = " "
        return market_cap,pe_ratio,current_price,de_ratio,book_value,dividend_yield




def get_plot_fbprophet(ticker):
    df = yf.download(ticker, start="2018-01-01", period='max', interval='1d')
    df = df.reset_index()
    df = df[['Date','Close']]
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])
    
    model = Prophet(daily_seasonality=True)
    model.fit(df)
    
    future = model.make_future_dataframe(periods=365, freq='D')
    forecast = model.predict(future)
    
    # Plotting forecast and components
    fig = model.plot(forecast)
    st.pyplot(fig)

    fig_components = model.plot_components(forecast)
    st.pyplot(fig_components)


def get_plot_lstm(ticker):
    # Downloading stock data
    dataset = yf.download(ticker, start="2018-01-01", period="max", interval="1d")
    
    # Splitting dataset into training and testing sets
    dataset_training = dataset.iloc[:int(len(dataset)*0.75), ]
    dataset_testing = dataset.iloc[int(len(dataset)*0.75):, ]
    
    # Preprocessing data
    training_set = dataset_training.iloc[:, 3:4].values
    scaler = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = scaler.fit_transform(training_set)
    
    # Creating input sequences for LSTM
    x_train, y_train = [], []
    for i in range(60, len(dataset_training)):
        x_train.append(training_set_scaled[i-60:i, 0])
        y_train.append(training_set_scaled[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    
    # Building LSTM model
    regressor = Sequential([
        LSTM(60, return_sequences=True, input_shape=(x_train.shape[1], 1)),
        Dropout(0.3),
        LSTM(60, return_sequences=True),
        Dropout(0.3),
        LSTM(60, return_sequences=True),
        Dropout(0.3),
        LSTM(60, return_sequences=True),
        Dropout(0.3),
        LSTM(60, return_sequences=False),
        Dropout(0.3),
        Dense(1)
    ])
    regressor.compile(optimizer='adam', loss='mean_squared_error')
    regressor.fit(x_train, y_train, epochs=1, batch_size=64)
    
    # Making predictions on test set
    dataset_total = pd.concat((dataset_training['Open'], dataset_testing['Open']), axis=0)
    inputs = dataset_total[len(dataset_total) - len(dataset_testing) - 60:].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)
    x_test = []
    for i in range(60, len(inputs)):
        x_test.append(inputs[i-60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predicted_stock_price = regressor.predict(x_test)
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
    
    # Forecasting for the next 30 days
    x_forecast = x_test[-1, :]
    forecasted_prices = []
    for _ in range(30):
        forecast = regressor.predict(np.array([x_forecast]))
        forecasted_prices.append(forecast[0, 0])
        x_forecast = np.concatenate((x_forecast[1:], np.array([[forecast[0, 0]]])))
    
    forecasted_prices = scaler.inverse_transform(np.array(forecasted_prices).reshape(-1, 1))
    forecast_dates = pd.date_range(start=dataset.index[-1], periods=31)[1:]
    
    # Visualizing results
    dataset_testing['Predicted'] = predicted_stock_price
    final_visualization = pd.concat([dataset['Open'], dataset_testing[['Open', 'Predicted']], pd.Series(index=forecast_dates, data=forecasted_prices.flatten())], axis=1)
    final_visualization.columns = ['Training Data', 'Testing Data', 'Predicted', 'Forecasted']
    
    # Plotting
    st.subheader("Stock Price Prediction")
    st.line_chart(final_visualization)

def compare(companies, column):
    plt.figure(figsize=(10, 6))

    for i in companies:
        dataset = yf.download(i, start="2018-01-01", period="max", interval="1d")
        plt.plot(dataset.index, dataset[column], label=i.split('.')[0])

    plt.legend()
    plt.grid()
    plt.title(f'Comparison for {column} prices')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    # Show the figure
    # st.plotly_chart(fig)

def multivariate_lstm(ticker_symbol):
    import numpy as np
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM
    from tensorflow.keras.layers import Dense, Dropout
    import pandas as pd
    from matplotlib import pyplot as plt
    from sklearn.preprocessing import StandardScaler
    import seaborn as sns
    import yfinance as yf
    import ta


    # ticker_symbol = "ASIANPAINT.NS"
    ticker = yf.Ticker(ticker_symbol)

    # Get historical price data
    historical_data = ticker.history(period="max")
    rsi = ta.momentum.RSIIndicator(close=historical_data['Close'], window=14)
    historical_data['RSI'] = rsi.rsi()

    #On Balance Volume
    obv = [0]
    # Iterate through historical data starting from the second day
    for i in range(1, len(historical_data)):
        today_close = historical_data['Close'][i]
        yesterday_close = historical_data['Close'][i - 1]
        volume = historical_data['Volume'][i]
        if today_close > yesterday_close:
            obv.append(obv[-1] + volume)
        elif today_close < yesterday_close:
            obv.append(obv[-1] - volume)
        else:
            obv.append(obv[-1])

    # Add OBV values to the DataFrame
    historical_data['OBV'] = obv
    # Print the historical data with OBV values
    df = historical_data[['Open','High','Low','Close','Volume','OBV','RSI']]
    df.reset_index(inplace=True)
    train_dates = pd.to_datetime(df['Date'])
    cols = list(df)[1:8]

    #New dataframe with only training data - 5 columns
    df_for_training = df[cols].astype(float)
    df_for_training = df_for_training[15:]

    scaler = StandardScaler()
    scaler = scaler.fit(df_for_training)
    df_for_training_scaled = scaler.transform(df_for_training)

    trainX = []
    trainY = []
    n_future = 1
    n_past = 60 
    for i in range(n_past, len(df_for_training_scaled) - n_future +1):
        trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])
        trainY.append(df_for_training_scaled[i + n_future - 1:i + n_future, 3])

    trainX, trainY = np.array(trainX), np.array(trainY)

    model = Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
    model.add(LSTM(32, activation='relu', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(trainY.shape[1]))

    model.compile(optimizer='adam', loss='mse')
    # model.summary()

    history = model.fit(trainX, trainY, epochs=5, batch_size=25, validation_split=0.1, verbose=1)

    n_past = 61
    n_days_for_prediction=90  #let us predict past 15 days

    predict_period_dates = pd.date_range(list(train_dates)[-n_past], periods=n_days_for_prediction).tolist()

    #Make prediction
    prediction = model.predict(trainX[-n_days_for_prediction:]) #shape = (n, 1) where n is the n_days_for_prediction
    prediction_copies = np.repeat(prediction, df_for_training.shape[1], axis=-1)
    predicted = scaler.inverse_transform(prediction_copies)[:,0]
    
    #sns.lineplot(x=range(1,len(df)+1), y=df['Close'], label='Original')
    # sns.lineplot(x=range(len(df)+1,len(df)+len(predicted)+1),y=predicted, label='Forecast')
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=range(1, len(df) + 1), y=df['Close'], label='Original')
    sns.lineplot(x=range(len(df) + 1, len(df) + len(predicted) + 1), y=predicted, label='Forecast')
    plt.xlabel('Day')
    plt.ylabel('Stock Price')
    plt.title('Stock Price Forecast')
    st.pyplot()



# Streamlit App
def dashboard():
    st.title("RISE.ai Web Portal")

    # Sidebar for selecting a company
    selected_company = st.sidebar.selectbox("Select Company:", nifty_fifty_companies)

    # Get Info Button
    get_info_button = st.sidebar.button("Get Info")

    # Sidebar for selecting companies and column for comparison
    selected_companies = st.sidebar.multiselect("Select Companies for comparison:", nifty_fifty_companies, default=["TCS.NS"])
    selected_column = st.sidebar.selectbox("Select Column for Comparison:", ["Open", "High", "Low", "Close", "Adj Close", "Volume"])
    compare_button = st.sidebar.button("Compare")


    if get_info_button:
        # Display sentiment analysis, news, candlestick chart, Facebook Prophet forecast, and LSTM stock price prediction at once
        st.subheader(f"Info for {d[selected_company]}")
        market_cap, pe_ratio, current_price, de_ratio, book_value, dividend_yield = get_info(selected_company)
        # Display information in three boxes in one row
        info_columns = st.columns(3)
        with info_columns[0]:
            st.info("Market Cap:")
            st.write(f"{market_cap}")

        with info_columns[1]:
            st.info("P/E Ratio:")
            st.write(f"{pe_ratio}")

        with info_columns[2]:
            st.info("Current Price:")
            st.write(f"{current_price}")

        with info_columns[0]:
            st.info("Debt to Equity ratio:")
            st.write(f"{de_ratio}")

        with info_columns[1]:
            st.info("Book Value:")
            st.write(f"{book_value}")

        with info_columns[2]:
            st.info("Dividend Yield:")
            st.write(f"{dividend_yield}")

        # Sentiment Analysis and News
        st.subheader(f"Sentiment Analysis and News for {d[selected_company]}")
        # Your existing code for sentiment analysis and news
        if selected_company:
            news_df = get_news(d[selected_company])
            label = []
            score = []
            # Initialize sentiment analysis pipeline
            sentiment_analysis = pipeline("sentiment-analysis")
            for i in range(len(news_df)):
                try:
                    label.append(sentiment_analysis(news_df['Title'].iloc[i])[0]['label'])
                    score.append(sentiment_analysis(news_df['Title'].iloc[i])[0]['score'])
                except:
                    label.append('NA')
                    score.append('NA')
            news_df['Label'] = label
            news_df['Score'] = score

            # Display the DataFrame
            col1, col2 = st.columns(2)
            col1.dataframe(news_df)

            # Plot pie chart in the second column
            with col2:
                plt.figure(figsize=(5, 5))
                plt.pie(news_df['Label'].value_counts().values, labels=news_df['Label'].value_counts().index,
                        autopct='%1.1f%%')
                plt.title("Distribution of News Titles with Labels in Percentage")
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot()

        # Candlestick Chart
        st.subheader(f"Candlestick Chart for {d[selected_company]}")
        fig_candlestick = candlestick(selected_company)
        st.plotly_chart(fig_candlestick, use_container_width=True)  # Adjusted to use container width

        # Facebook Prophet Forecast
        # st.subheader(f"Facebook Prophet Forecast for {d[selected_company]}")
        # get_plot_fbprophet(selected_company)

        # LSTM Stock Price Prediction
        st.subheader(f"Univariate LSTM Stock Price Prediction for {d[selected_company]}")
        get_plot_lstm(selected_company)

        st.subheader(f"Multivariate LSTM Stock Price Prediction for {d[selected_company]}")
        multivariate_lstm(selected_company)


    if compare_button:
        st.subheader(f"Comparison for {selected_column} prices")
        compare(selected_companies, selected_column)
    

    
    

if __name__ == "__main__":
    dashboard()
