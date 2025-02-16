import streamlit as st
import os
import google.generativeai as genai
import requests
import yfinance as yf

# Configure API Key for Gemini
genai.configure(api_key="AIzaSyAxTa2S6ixZ-Dgn9hLidZJbCTm2yYzLNoY")
model = genai.GenerativeModel('gemini-pro')

# Function to get AI-based financial insights
def get_financial_advice(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to fetch live stock prices
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_info = stock.history(period="1mo")
    return stock_info

# Streamlit UI
st.set_page_config(page_title="💰 AI Financial Analyst", layout="wide")
st.header("💹 AI Financial Analyst Chatbot")

# User Input
stock_symbol = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA, MSFT)")
investment_goal = st.selectbox("Select Investment Type", ["Short-term", "Long-term", "Dividend"])

# Fetch Stock Data
if st.button("Analyze Stock"):
    if stock_symbol:
        try:
            # Fetch Stock Data
            stock_data = get_stock_data(stock_symbol.upper())

            if not stock_data.empty:
                st.subheader(f"📈 Stock Price Trends for {stock_symbol.upper()}")
                st.line_chart(stock_data['Close'])  # Plot closing prices

                # Generate AI financial insights
                prompt = f"Analyze the financial health of {stock_symbol.upper()} for a {investment_goal} investment. Consider earnings, revenue, P/E ratio, and market trends."
                advice = get_financial_advice(prompt)

                st.subheader("💡 AI-Powered Investment Advice")
                st.write(advice)
            else:
                st.error("No stock data found. Please check the symbol and try again.")
        except Exception as e:
            st.error(f"Error fetching stock data: {str(e)}")
    else:
        st.error("Please enter a valid stock ticker symbol.")

# Market Trend Prediction
st.subheader("📊 AI Market Trend Predictions")
market_prompt = "Provide an overview of the current stock market trends and investment opportunities."
market_trends = get_financial_advice(market_prompt)
st.write(market_trends)
