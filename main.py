import streamlit as st
from modules.data_loader import load_data, preprocess_data, commodity_columns
from modules.agent_simulation import run_simulation, MarketAgent
from modules.visualization import plot_price_data, plot_currency_data, plot_stock_data
import pandas as pd
import os

# Page setup
# Set the page configuration
st.set_page_config(
    page_title="Global Financial App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go To", ["Home", "Commodity Markets", "Stocks","Financial Markets", "Currency Markets","Market Simulation"])

# Load and preprocess commodity data
price_data = load_data('data\\wb.csv')
price_data = preprocess_data(price_data)

# Load stock index data
index_files = [f for f in os.listdir('data\\index') if f.endswith('.csv')]
index_data = {}
for file in index_files:
    index_name = file.split('.')[0]
    data = load_data(f'data\\index\\{file}')
    index_data[index_name] = preprocess_data(data)

# Load stock ticker data
stock_files = [f for f in os.listdir('data\\stocks') if f.endswith('.csv')]
stock_data = {}
for file in stock_files:
    stock_name = file.split('.')[0]
    data = load_data(f'data\\stocks\\{file}')
    stock_data[stock_name] = preprocess_data(data)

# Load and preprocess data
def load_currency_data(currency_folder='data\\currency'):
    currency_files = os.listdir(currency_folder)
    currency_data = {}
    for file in currency_files:
        if file.endswith('.csv'):
            pair_name = file.split('_1mo.csv')[0].replace('_', '/')
            currency_data[pair_name] = pd.read_csv(os.path.join(currency_folder, file))
    return currency_data


# Home page
if page == "Home":
    st.title('Global Financial Market App')
    st.markdown("""
    <style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        color: #4CAF50;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #6A1B9A;
    }
    .feature {
        font-size: 20px;
        margin: 10px 0;
        color: #2E7D32;
    }
    .nav-link {
        font-size: 18px;
        margin: 5px 0;
        color: #00796B;
        text-decoration: none;
    }
    .nav-link:hover {
        color: #004D40;
    }
    .footer {
        font-size: 14px;
        margin: 20px 0;
        color: #757575;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="main-header">Stocks - Currencies - Indexes</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your comprehensive tool for financial market analysis and insights</div>', unsafe_allow_html=True)

    # Features section
    st.markdown('<div class="sub-header">Key Features:</div>', unsafe_allow_html=True)
    features = [
        "Real-time market data visualization",
        "Historical stock and commodity price analysis",
        "Economic indicators and forecasting",
        "Portfolio simulation and backtesting",
        "Sentiment analysis and market events tracking"
    ]
    for feature in features:
        st.markdown(f'<div class="feature">• {feature}</div>', unsafe_allow_html=True)

    # Navigation section
    st.markdown('<div class="sub-header">Explore the App:</div>', unsafe_allow_html=True)
    nav_links = [
        {"title": "Financial Markets", "url": "#"},
        {"title": "Portfolio Simulation", "url": "#"},
        {"title": "Economic Indicators", "url": "#"},
        {"title": "Market Sentiment", "url": "#"},
        {"title": "Contact", "url": ""}
    ]
    for link in nav_links:
        st.markdown(f'<a class="nav-link" href="{link["url"]}">{link["title"]}</a>', unsafe_allow_html=True)
    st.image("data\\finance.png", use_column_width=False)
    # Footer section
    st.markdown('<div class="footer">© 2024 Global Financial App. Created by Kampamba Shula. All rights reserved.</div>', unsafe_allow_html=True)

# Commodity Markets page
elif page == "Commodity Markets":
    st.header("Commodity Markets")
    st.subheader("Commodities Price Data")
    asset = st.selectbox("Select Commodity", commodity_columns)
    time_range = st.selectbox("Select Time Range", ["6 Months", "1 Year", "5 Years", "10 Years"])

    # Calculate date range
    end_date = price_data['Date'].max()
    if time_range == "6 Months":
        start_date = end_date - pd.DateOffset(months=6)
    elif time_range == "1 Year":
        start_date = end_date - pd.DateOffset(years=1)
    elif time_range == "5 Years":
        start_date = end_date - pd.DateOffset(years=5)
    elif time_range == "10 Years":
        start_date = end_date - pd.DateOffset(years=10)

    filtered_data = price_data[(price_data['Date'] >= start_date) & (price_data['Date'] <= end_date)]
    filtered_data = filtered_data[['Date', asset]]

    plot_price_data(filtered_data, asset)

# Financial Markets page
elif page == "Financial Markets":
    st.header("Financial Markets")
    st.subheader("Stock Index Data")
    index = st.selectbox("Select Stock Index", list(index_data.keys()))
    column = st.selectbox("Select Column", ["Open", "Close", "High", "Low", "Volume"])
    time_range = st.selectbox("Select Time Range", ["6 Months", "1 Year", "5 Years", "10 Years","20 Years"])

    # Calculate date range
    index_df = index_data[index]
    end_date = index_df['Date'].max()
    if time_range == "6 Months":
        start_date = end_date - pd.DateOffset(months=6)
    elif time_range == "1 Year":
        start_date = end_date - pd.DateOffset(years=1)
    elif time_range == "5 Years":
        start_date = end_date - pd.DateOffset(years=5)
    elif time_range == "10 Years":
        start_date = end_date - pd.DateOffset(years=10)
    elif time_range == "20 Years":
        start_date = end_date - pd.DateOffset(years=20)

    filtered_data = index_df[(index_df['Date'] >= start_date) & (index_df['Date'] <= end_date)]
    filtered_data = filtered_data[['Date', column]]

    plot_stock_data(filtered_data, column, index)

# Market Simulation page
elif page == "Market Simulation":
    st.title('Market Simulation')

    berkshire_hathaway = MarketAgent('Berkshire Hathaway', 'long')
    AAPL = st.number_input(label="AAPL",min_value=0.05, max_value=0.3)
    BAC = st.number_input(label="BAC",min_value=0.05, max_value=0.3)
    AXP = st.number_input(label="AXP",min_value=0.05, max_value=0.3)
    KO = st.number_input(label="KO",min_value=0.05, max_value=0.3)
    CVX = st.number_input(label="CVX",min_value=0.05, max_value=0.3)
    OXY = st.number_input(label="OXY",min_value=0.05, max_value=0.3)
    KHC = st.number_input(label="KHC",min_value=0.05, max_value=0.3)
    MCO = st.number_input(label="MCO",min_value=0.05, max_value=0.3)
    DVA = st.number_input(label="DVA",min_value=0.05, max_value=0.3)
    HPQ = st.number_input(label="HPQ",min_value=0.05, max_value=0.3)
    

    berkshire_hathaway.add_stock('AAPL', AAPL)
    berkshire_hathaway.add_stock('BAC', BAC)
    berkshire_hathaway.add_stock('AXP', AXP)
    berkshire_hathaway.add_stock('KO', KO)
    berkshire_hathaway.add_stock('CVX', CVX)
    berkshire_hathaway.add_stock('OXY', OXY)
    berkshire_hathaway.add_stock('KHC', KHC)
    berkshire_hathaway.add_stock('MCO', MCO)
    berkshire_hathaway.add_stock('DVA', DVA)
    berkshire_hathaway.add_stock('HPQ', HPQ)

    start_date = st.date_input("Start Date", value=pd.to_datetime("2017-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2022-01-01"))

    if st.button("Run Simulation"):
        portfolio_return = berkshire_hathaway.simulate(start_date, end_date)
        st.line_chart(portfolio_return)

elif page == "Currency Markets":
    st.header("Currency Markets")
    currency_data = load_currency_data()

    st.subheader("Currency Exchange Rates")
    currency_pair = st.selectbox("Select Currency Pair", list(currency_data.keys()))
    time_range = st.selectbox("Select Time Range", ["6 Months", "1 Year", "5 Years", "10 Years"])

    data = currency_data[currency_pair]
    data['Date'] = pd.to_datetime(data['Date'])
    end_date = data['Date'].max()

    if time_range == "6 Months":
        start_date = end_date - pd.DateOffset(months=6)
    elif time_range == "1 Year":
        start_date = end_date - pd.DateOffset(years=1)
    elif time_range == "5 Years":
        start_date = end_date - pd.DateOffset(years=5)
    elif time_range == "10 Years":
        start_date = end_date - pd.DateOffset(years=10)

    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    plot_currency_data(filtered_data, currency_pair)

elif page == "Stocks":
    st.header("Stocks")
    st.subheader("Stock Ticker Data")
    index = st.selectbox("Select Stock Index", list(stock_data.keys()))
    column = st.selectbox("Select Column", ["Open", "Close", "High", "Low", "Volume"])
    time_range = st.selectbox("Select Time Range", ["6 Months", "1 Year", "5 Years", "10 Years","20 Years"])

    # Calculate date range
    stock_df = stock_data[index]
    end_date = stock_df['Date'].max()
    if time_range == "6 Months":
        start_date = end_date - pd.DateOffset(months=6)
    elif time_range == "1 Year":
        start_date = end_date - pd.DateOffset(years=1)
    elif time_range == "5 Years":
        start_date = end_date - pd.DateOffset(years=5)
    elif time_range == "10 Years":
        start_date = end_date - pd.DateOffset(years=10)
    elif time_range == "20 Years":
        start_date = end_date - pd.DateOffset(years=20)

    filtered_data = stock_df[(stock_df['Date'] >= start_date) & (stock_df['Date'] <= end_date)]
    filtered_data = filtered_data[['Date', column]]

    plot_stock_data(filtered_data, column, index)
    