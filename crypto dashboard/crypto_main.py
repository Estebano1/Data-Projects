# Importieren von Bibliotheken
import streamlit as st
import pandas as pd

# Importieren von Funktionen aus crypto_data.py
from crypto_data import get_current_price

# Importieren von Funktionen aus crypto_visualizations.py
from crypto_visualizations import visualize_candlestick_and_volume_charts, compare_volumes, visualize_performance_comparison, display_trending_coins, visualize_information_and_explanations
from crypto_visualizations import visualize_volatility_comparison, visualize_fear_greed_index_gauge, visualize_order_book, display_events_page, visualize_fear_greed_index_history

# Importieren von API aus benance.py
from benance import COINMARKETCAL_API

def main():

    st.markdown("## Listen to Some Music While Exploring")
    audio_file = '/Users/Estebano/Downloads/gibran_alcocer_slowed_reverb).mp3'
    
    if st.button('Play Music'):
        st.audio(audio_file, format='audio/mp3')
        
        
        
    # Stildefinitionen für das Dashboard
    st.markdown("""
    <style>
      .reportview-container {
        background: url("https://mir-s3-cdn-cf.behance.net/project_modules/fs/6d29e8132610453.61ace30aea0e2.png");
      }
      .sidebar .sidebar-content {
        background-image: url("https://images.unsplash.com/photo-1607707972895-7f994d8c2f3b?q=80&w=2881&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        color: white;
      }
      .css-1v8ow1e {
        background-color: transparent !important;
      }
      /* Stildefinitionen für Elemente */
      .price-container {
        padding: 10px;
        background-color: #1a0838;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        margin: 10px 0;
        color: white;
        text-align: center;
      }
      h1 {
        font-family: 'Arial', sans-serif;
        font-size: 40px;
        color: #f3e5ab;
        text-shadow: 2px 2px 4px #000000;
        text-align: center; /* Zentrierung der Überschrift */
      }
    </style>
    """, unsafe_allow_html=True)
    
    # Weitere Stildefinitionen für das Dashboard
    st.markdown("""
    <style>
      /* Benutzerdefinierte Schriftarten und Farben */
      .sidebar .sidebar-content {
        font-family: Arial, sans-serif;
        color: #4f4f4f;
      }
      /* Stil für Überschriften in der Seitenleiste */
      .sidebar h1 {
        color: #f3e5ab;
      }
    </style>
    """, unsafe_allow_html=True)

    # Überschrift für das Dashboard
    st.markdown("""
    <style>
    h1 {color: #f3e5ab;}
    </style>
    <h1>Crypto Dashboard 🚀</h1>
    """, unsafe_allow_html=True)
    
    # Stil für Schaltflächen
    st.markdown("""
    <style>
    div.stButton > button:first-child {
    background-color: #24104c;
    color: silver;
    border-radius: 8px; /* Rundere Ecken */
    border: none;
    padding: 10px 20px; /* Leicht größeres Padding */
    font-size: 17px; /* Etwas größere Schrift */
    font-family: Arial, sans-serif; /* Klare Schriftart */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2); /* Schatten hinzufügen */
    transition: background-color 0.3s, box-shadow 0.3s; /* Glatte Übergangsanimation */
    }
    div.stButton > button:first-child:hover {
    background-color: silver;
    color: #24104c;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3); /* Größerer Schatten beim Hover */
    }
    </style>
    """, unsafe_allow_html=True)        
    
    # Seitennavigation
    page = st.sidebar.selectbox("Choose a Page:", ["Dashboard", "Events", "Trending Coins", "Help"])

 
    if page == "Dashboard":
        # Sidebar-Titel und Ansichtsauswahl
        st.sidebar.markdown('# Main Menu 🚀')
        view_mode = st.sidebar.radio("View Mode", ['Single View', 'Comparison View'])
    
        if view_mode == 'Single View':
            # Eingabe von Kryptowährungssymbol, Zeitrahmen und Datumsauswahl
            binance_symbol = st.sidebar.text_input("🔍 Enter Ticker Symbol (e.g., BTCUSDT)", "BTCUSDT", key="single_view_input").upper()
            timeframe = st.sidebar.selectbox("🕒 Select Timeframe", ["4 hours", "1 day", "1 week", "1 month"], index=2)
            start_date = st.sidebar.date_input("📅 Start Date", pd.to_datetime("2023-01-01"))
            end_date = st.sidebar.date_input("📅 End Date", pd.to_datetime("today"))
    
            # Aktueller Preis abrufen und anzeigen
            current_price = get_current_price(binance_symbol)
            st.markdown(f"<div class='price-container' style='color: silber;'>Current Price of {binance_symbol}:  <strong style='color: #FFD700;'> {current_price} $</strong></div>", unsafe_allow_html=True)
    
            # Candlestick- und Volumen-Charts anzeigen
            visualize_candlestick_and_volume_charts(binance_symbol, start_date, end_date, timeframe)
    
            # Flag für die Anzeige des Orderbook Charts
            show_orderbook_chart = True
    
            # Button zum Aktualisieren des Orderbook Charts
            if st.button('Update Chart'):
                show_orderbook_chart = False
                visualize_order_book(binance_symbol, current_price)
    
            # Anzeige des Orderbook Charts, falls das Flag aktiv ist
            if show_orderbook_chart:
                visualize_order_book(binance_symbol, current_price)
    
            # Anzeige des Fear & Greed Index Gauge
            visualize_fear_greed_index_gauge()
    
            # Option zum Anzeigen der historischen Daten des Fear & Greed Index
            if st.button('Show Fear & Greed Index History'):
                visualize_fear_greed_index_history()
    
        elif view_mode == 'Comparison View':
            # Eingabe von Kryptowährungssymbolen für den Vergleich
            selected_symbols_str = st.sidebar.text_input("🔍 Enter Ticker Symbols for Comparison (e.g., BTC, ETH)", key="comparison_view_input")
            selected_symbols = [s.strip().upper() for s in selected_symbols_str.split(',')]
            timeframe = st.sidebar.selectbox("🕒 Select Timeframe", ["4 hours", "1 day", "1 week", "1 month"], index=2)
            start_date = st.sidebar.date_input("📅 Start Date", pd.to_datetime("2023-01-01"))
            end_date = st.sidebar.date_input("📅 End Date", pd.to_datetime("today"))
    
            if len(selected_symbols) > 1:
                # Leistungsvergleich, Volumenvergleich und Volatilitätsvergleich anzeigen
                visualize_performance_comparison(selected_symbols, start_date, end_date, timeframe)
                compare_volumes(selected_symbols, start_date, end_date, timeframe)
                visualize_volatility_comparison(selected_symbols, start_date, end_date, timeframe)
            else:
                st.error("Please enter more than one cryptocurrency for comparison.")

    elif page == "Events":
        # Datum für Veranstaltungen auswählen
        selected_date = st.sidebar.date_input("Select Event Date", pd.to_datetime("today"))
        
        # Funktion aufrufen, um Veranstaltungen anzuzeigen
        display_events_page(COINMARKETCAL_API, selected_date)
    
    elif page == "Trending Coins":
        # Funktion aufrufen, um die Trending Coins anzuzeigen
        display_trending_coins()
    
    elif page == "Help":
        # Funktion aufrufen, um Informationen und Erklärungen anzuzeigen
        visualize_information_and_explanations()
    
    
    
    
if __name__ == '__main__':
        main()
