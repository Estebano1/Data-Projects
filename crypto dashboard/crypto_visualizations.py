# Importieren von Bibliotheken
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Importieren von Funktionen aus crypto_data.py
from crypto_data import calculate_percent_change, get_fear_greed_index, get_order_book, get_coinmarketcal_events, get_fear_greed_index_history
from crypto_data import download_historical_data, calculate_bollinger_bands, calculate_volatility, get_trending_coins_coingecko


# Alle Visualisierungsfunktionen 


def visualize_candlestick_and_volume_charts(symbol, start_date, end_date, timeframe):
    # Laden der historischen Daten für das ausgewählte Symbol und den Zeitraum
    data = download_historical_data(symbol, start_date, end_date, timeframe)

    # Überprüfen, ob Daten vorhanden sind
    if not data.empty:
        # Berechnung der EMA-Indikatoren, Bollinger Bands und RSI
        data['EMA20'] = data['close'].ewm(span=20, adjust=False).mean()
        data['EMA50'] = data['close'].ewm(span=50, adjust=False).mean()
        data['EMA100'] = data['close'].ewm(span=100, adjust=False).mean()
        data['EMA200'] = data['close'].ewm(span=200, adjust=False).mean()
        data['middle_band'], data['upper_band'], data['lower_band'] = calculate_bollinger_bands(data)

        # Erstellung eines Charts mit zwei Reihen
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.02, 
                            row_heights=[0.7, 0.3])

        # Hauptchart mit Candlesticks, EMA und Bollinger Bands
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['open'],
                                     high=data['high'],
                                     low=data['low'],
                                     close=data['close'],
                                     name='Candlesticks'), row=1, col=1)
        
        # Hinzufügen der EMA-Linien zum Hauptchart
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], mode='lines', name='EMA 20'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], mode='lines', name='EMA 50'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA100'], mode='lines', name='EMA 100'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA200'], mode='lines', name='EMA 200'), row=1, col=1)

        # Bollinger Bands hinzufügen
        fig.add_trace(go.Scatter(x=data.index, y=data['upper_band'], line=dict(width=1), name='Upper Band'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['middle_band'], line=dict(width=1), name='Middle Band'), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['lower_band'], line=dict(width=1), name='Lower Band'), row=1, col=1)

        # Volumen-Balkendiagramm für den Range Slider hinzufügen
        fig.add_trace(go.Bar(x=data.index, y=data['volume'], name='Volume', marker_color='white', opacity=0.6), row=2, col=1)

        # Layout-Einstellungen für den Chart
        fig.update_layout(
            title=f'Price and Volume Chart for {symbol}',
            yaxis_title='Price',
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="silver"  
            ),
            plot_bgcolor='#24104c', 
            paper_bgcolor='#1a0838',  
            xaxis=dict(
                showgrid=True,
                gridcolor='#9d81e6'  
            ),
            yaxis=dict(
                title='Price',
                showgrid=True,
                gridcolor='#9d81e6' 
            ),
            margin=dict(l=40, r=40, t=40, b=40),  # Abstandseinstellungen für den Inhalt
            template='plotly_dark' 
        )
    
        # Y-Achsen-Konfigurationen für den Hauptchart und den Range Slider
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        # Anzeigen des erstellten Charts
        st.plotly_chart(fig)
    else:
        # Fehlermeldung anzeigen, wenn keine Daten verfügbar sind
        st.error("No data available for the selected symbols in the specified timeframe.")





def compare_volumes(symbols, start_date, end_date, timeframe):
    # Eine leere Liste, um Volumendaten für verschiedene Symbole zu sammeln
    volume_data = []

    # Schleife über die angegebenen Symbole
    for symbol in symbols:
        # Laden der historischen Daten für den ausgewählten Coin und den Zeitraum
        data = download_historical_data(symbol + "USDT", start_date, end_date, timeframe)
        
        # Überprüfen, ob Daten vorhanden sind und ob die 'volume'-Spalte vorhanden ist
        if not data.empty and 'volume' in data.columns:
            # Falls 'average_price' nicht in den Daten vorhanden ist, selber berechnen
            if 'average_price' not in data.columns:
                data['average_price'] = (data['high'] + data['low']) / 2

            # Berechnung des durchschnittlichen Dollar-Volumens
            dollar_volume = (data['volume'] * data['average_price']).mean()
            
            # Hinzufügen der Volumendaten für den ausgewählten coin 
            volume_data.append({'Currency': symbol, 'Volume': dollar_volume})
        else:
            print(f"No data available for {symbol} in the specified timeframe.")

    # Überprüfen, ob Volumendaten gesammelt wurden
    if volume_data:
        # Erstellen eines Pandas DataFrame aus den gesammelten Volumendaten
        df = pd.DataFrame(volume_data)

        # Umrechnung des Zeitrahmens in lesbaren Text
        timeframe_text = timeframe
        if timeframe == "1w":
            timeframe_text = "Week"
        elif timeframe == "1d":
            timeframe_text = "Day"
        elif timeframe == "4h":
            timeframe_text = "4 Hours"

        # Formatieren des Titels
        title = f"Average Trading Volume per {timeframe_text} from {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')}"
        
        # Erstellen eines Balkendiagramms mit Plotly Express
        fig = px.bar(df, x='Currency', y='Volume', title=title, color_discrete_sequence=['#ec40fc'])

        # Layout-Einstellungen für den Chart
        fig.update_layout(
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="silver"  
            ),
            plot_bgcolor='#24104c', 
            paper_bgcolor='#1a0838',  
            xaxis=dict(
                showgrid=True,
                gridcolor='#9d81e6'  
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#9d81e6' 
            ),
            margin=dict(l=40, r=40, t=40, b=40),  # Abstandseinstellungen für den Inhalt
            template='plotly_dark' 
        )
        
        # Anzeigen des erstellten Balkendiagramms
        st.plotly_chart(fig)
    else:
        # Fehlermeldung anzeigen, wenn keine Daten für die ausgewählten coins vorhanden sind
        st.error("No data available for the selected coins in the specified timeframe.")




def visualize_performance_comparison(selected_symbols, start_date, end_date, timeframe):
    # Erstellen eines Subplots mit einer Zeile und einer Spalte
    fig = make_subplots(rows=1, cols=1)
    
    # Schleife über ausgewählte Symbole
    for symbol in selected_symbols:
        # Laden der historischen Daten für das aktuelle Symbol und den Zeitraum
        data = download_historical_data(symbol + "USDT", start_date, end_date, timeframe)
        
        # Überprüfen, ob Daten vorhanden sind
        if not data.empty:
            # Berechnung der prozentualen Veränderung
            percent_change = calculate_percent_change(data)
            
            # Hinzufügen einer Linie zum Diagramm für den ausgewählten coin
            fig.add_trace(go.Scatter(x=[start_date, end_date], y=[0, percent_change], mode='lines', name=symbol))
    
    # Layout-Einstellungen für den Chart
    fig.update_layout(
        title='Comparison of Cryptocurrency Performance (%)',
        yaxis_title='Percentage Change',
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="silver"  
        ),
        plot_bgcolor='#24104c', 
        paper_bgcolor='#1a0838',  
        xaxis=dict(
            showgrid=True,
            gridcolor='#9d81e6'  
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#9d81e6' 
        ),
        margin=dict(l=40, r=40, t=40, b=40),  # Abstandseinstellungen für den Inhalt
        template='plotly_dark' 
    )
    
    # Anzeigen des erstellten Diagramms
    st.plotly_chart(fig)




def visualize_volatility_comparison(selected_symbols, start_date, end_date, timeframe):
    # Eine leere Liste zum Speichern der Volatilitätsdaten
    volatilities = []

    # Schleife über ausgewählte Coins
    for symbol in selected_symbols:
        # Laden der historischen Daten für den ausgewählten Coin und den Zeitraum
        data = download_historical_data(symbol + "USDT", start_date, end_date, timeframe)
        
        # Überprüfen, ob Daten vorhanden sind
        if not data.empty:
            # Berechnung der Volatilität
            volatility = calculate_volatility(data)
            
            # Hinzufügen der Volatilität zur Liste
            volatilities.append({'Currency': symbol, 'Volatility': volatility})

    # Überprüfen, ob Volatilitätsdaten vorhanden sind
    if volatilities:
        # Erstellen eines DataFrame aus den Volatilitätsdaten
        df = pd.DataFrame(volatilities)

        # Erstellen des Titels für das Diagramm
        title = f"Average Volatility per {timeframe} from {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')}"
        
        # Erstellen eines Balkendiagramms mit Plotly Express
        fig = px.bar(df, x='Currency', y='Volatility', title=title, color_discrete_sequence=['#ec40fc'])

        # Layout-Einstellungen für den Chart
        fig.update_layout(
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="silver"  
            ),
            plot_bgcolor='#24104c', 
            paper_bgcolor='#1a0838',  
            xaxis=dict(
                showgrid=True,
                gridcolor='#9d81e6'  
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#9d81e6' 
            ),
            margin=dict(l=40, r=40, t=40, b=40),  # Abstandseinstellungen für den Inhalt
            template='plotly_dark' 
        )

        # Anzeigen des erstellten Diagramms
        st.plotly_chart(fig)
    else:
        st.error("No data available for the selected symbols in the specified timeframe.")



def visualize_fear_greed_index_gauge():
    # Abrufen des Fear & Greed Index-Datensatzes
    df = get_fear_greed_index()
    
    # Extrahieren des neuesten Indexwerts
    latest_index = df.iloc[-1]['value']
    
    # Konvertieren des neuesten Indexwerts in eine Zahl, falls er ein String ist
    latest_index_num = float(latest_index) if isinstance(latest_index, str) else latest_index

    # Erstellen eines Plotly-Figur-Objekts für das Gauge-Diagramm
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=latest_index_num,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Today's Fear & Greed Index"},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#24104c"},
            'bar': {'color': "#24104c"},
            'steps': [
                {'range': [0, 25], 'color': 'green'},
                {'range': [25, 50], 'color': 'lightgreen'},
                {'range': [50, 75], 'color': 'orange'},
                {'range': [75, 100], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': "#24104c", 'width': 4},
                'thickness': 0.75,
                'value': latest_index_num
            }
        }
    ))

    # Hinzufügen von Anmerkungen zum Gauge-Diagramm
    fig.add_annotation(x=-0.1, y=0.03, text="STRONG BUY", showarrow=False, font=dict(size=22, color="silver"))
    fig.add_annotation(x=1.11, y=0.03, text="STRONG SELL", showarrow=False, font=dict(size=22, color="silver"))
    fig.add_annotation(x=0.1, y=0.9, text="BUY", showarrow=False, font=dict(size=22, color="silver"))
    fig.add_annotation(x=0.92, y=0.9, text="SELL", showarrow=False, font=dict(size=22, color="silver"))

    # Anpassen des Layouts des Gauge-Diagramms
    fig.update_layout(paper_bgcolor="#1a0838", font={'color': "silver", 'family': "Arial, sans-serif"})

    # Anzeigen des erstellten Diagramms
    st.plotly_chart(fig)





def visualize_fear_greed_index_history():
    # Abrufen des Fear & Greed Index-Historiendatensatzes
    df = get_fear_greed_index_history()
    
    # Erstellen eines Plotly-Figur-Objekts für die Indexverlaufsdarstellung
    fig = go.Figure(data=[
        go.Scatter(x=df['timestamp'], y=df['value'], mode='lines+markers', name='Fear & Greed Index')
    ])
    
    # Anpassen des Layouts der Indexverlaufsdarstellung
    fig.update_layout(
        title="Fear & Greed Index Over Time",
        yaxis_title="Index Value",
        font=dict(
            family="Arial, sans-serif",
            size=12,
            color="silver"
        ),
        plot_bgcolor='#24104c',
        paper_bgcolor='#1a0838',
        xaxis=dict(
            showgrid=True,
            gridcolor='#9d81e6'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#9d81e6'
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        template='plotly_dark'
    )

    # Anzeigen des erstellten Diagramms
    st.plotly_chart(fig)


    

def visualize_order_book(symbol, current_price):
    # Abrufen des Orderbuchs für den ausgewählten Coin
    order_book = get_order_book(symbol)

    if order_book:
        # Erstellen von DataFrames für Gebote und Angebote
        bids = pd.DataFrame(order_book['bids'], columns=['Price', 'Quantity'], dtype=float)
        asks = pd.DataFrame(order_book['asks'], columns=['Price', 'Quantity'], dtype=float)

        # Sortieren der Gebote absteigend und der Angebote aufsteigend nach Preis
        bids = bids.sort_values(by='Price', ascending=False)
        asks = asks.sort_values(by='Price', ascending=True)

        # Berechnen der kumulativen Mengen für Gebote und Angebote
        bids['Cumulative Quantity'] = bids['Quantity'].cumsum()
        asks['Cumulative Quantity'] = asks['Quantity'].cumsum()

        # Erstellen des Liniendiagramms für das Orderbuch
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=bids['Price'], y=bids['Cumulative Quantity'], mode='lines', name='Buy order', fill='tozeroy', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=asks['Price'], y=asks['Cumulative Quantity'], mode='lines', name='Sell order', fill='tozeroy', line=dict(color='red')))

        # Layout-Anpassungen für das Diagramm
        fig.update_layout(
            title=f'Orderbook of {symbol}',
            xaxis_title='Price',
            yaxis_title='Units',
            font=dict(
                family="Arial, sans-serif",
                size=12,
                color="silver"  
            ),
            plot_bgcolor='#24104c', 
            paper_bgcolor='#1a0838',
            margin=dict(l=40, r=40, t=40, b=40),
            template='plotly_dark'
        )

        # Anzeigen des erstellten Diagramms
        st.plotly_chart(fig)
    else:
        st.error("No order book data available.")

        
        
def display_events_page(api_key, selected_date):
    # Anwenden von CSS für den Titel
    st.markdown(
    """
    <style>
    .custom-title {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    # Anzeigen des Titels mit dem ausgewählten Datum
    st.markdown(f'<h1 class="custom-title">Upcoming Cryptocurrency Events for {selected_date.strftime("%d-%m-%Y")}</h1>', unsafe_allow_html=True)

    # Events für das gewählte Datum abrufen
    events = get_coinmarketcal_events(api_key, selected_date, selected_date)

    # Anzeigen der Events
    for event in events:
        # Formatieren und Anzeigen jedes Events
        st.markdown(
            f"""
            <div style="background-color: rgba(211, 211, 211, 0.3);padding:10px;border-radius:10px; max-width: 75;">
                <h3 style="color: #f3e5ab;">{event['title']['en']}</h3>
                <p><strong>Date:</strong> {pd.to_datetime(event['date_event']).strftime('%d-%m-%Y')}</p>
                {f"<p><strong>Coin(s):</strong> {', '.join([coin['fullname'] for coin in event['coins']])}</p>" if 'coins' in event else ''}
                <p><a href="{event['source']}" target="_blank" style="color: darkblue;">More Info</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")  # Trennlinie nach jedem Event



def display_trending_coins():
    # Anwenden von CSS für den Titel
    st.markdown(
    """
    <style>
    .custom-title {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    
    #  Überschrift CSS
    st.markdown('<h1 class="custom-title">Trending Coins on Coingecko</h1>', unsafe_allow_html=True)

    # Aufrufen der Trending Coins 
    trending_coins = get_trending_coins_coingecko()

    if trending_coins:
        for coin in trending_coins:
            # Formatieren und Anzeigen der Trending Coins
            st.markdown(
                f"""
                <div style="background-color: rgba(211, 211, 211, 0.2); padding: 5px; border-radius: 25px; margin: 5px auto; display: flex; align-items: center; max-width: 45%;">
                    <h4 style="color: black; margin: 0; flex-grow: 1;">{coin['name']}</h4>
                    <p style="margin: 0 5px 0 0; font-weight: bold; color: gold;">Symbol: {coin['symbol']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No trending coins found.")

        
        
        
def visualize_information_and_explanations():
    # Anwenden von CSS für den Titel
    st.markdown(
        """
        <style>
        h2 {color: silver;}
        </style>
        <h2 class="custom-title">Dashboard Information and Explanations</h2>
        """, unsafe_allow_html=True,
    )

    # Inhalt der Hilfeseite
    st.markdown("""        
        **Candlestick and Volume Charts Display:**

        - This section provides detailed candlestick and volume charts for a selected cryptocurrency.
        - You can choose a cryptocurrency symbol, start date, end date, and timeframe to view historical price data.
        - The charts display candlestick patterns that represent the open, close, high, and low prices for each period.
        - Additionally, you'll see volume bars indicating trading activity.
        - This visualization is useful for technical analysis and understanding price movements over time.
          
        *Moving Average (20/50/100/200):*
        
        Moving Averages are commonly used technical indicators in financial analysis. They represent the average closing price of a security over a specified period of time. The numbers in parentheses (20/50/100/200) refer to the specific timeframes commonly used:
        
        - 20-day moving average: It calculates the average closing price over the last 20 days.
        - 50-day moving average: It calculates the average closing price over the last 50 days.
        - 100-day moving average: It calculates the average closing price over the last 100 days.
        - 200-day moving average: It calculates the average closing price over the last 200 days.
        - Moving averages are used to identify trends, smooth out price data, and provide insights into potential support and resistance levels.
        
        *Bollinger Bands (Upper, Middle, Lower Band):*
        
        Bollinger Bands are a volatility indicator that consists of three lines:
        
        - Upper Band: It is typically set two standard deviations above the middle band. It represents the upper volatility boundary.
        - Middle Band: This is a simple moving average, usually calculated over a 20-day period. It serves as the centerline of the Bollinger Bands.
        - Lower Band: It is set two standard deviations below the middle band and represents the lower volatility boundary.
        - Bollinger Bands are used to assess price volatility and identify potential overbought or oversold conditions. 
        - When the price approaches the upper or lower bands, it may indicate a potential reversal or continuation of a trend.
        
        *Volume:*
        
        - Volume in financial markets refers to the total number of shares or contracts traded during a specific time period (usually a day). 
        - It is a crucial indicator as it provides insights into the level of interest or activity in a particular security or market.
        - High volume typically accompanies significant price movements and reflects strong market participation. 
        - Low volume may suggest a lack of interest or uncertainty. 
        - Traders and analysts often use volume in conjunction with price analysis to make informed decisions about buying or selling assets.

        **Volume Comparison:**
        
        - This chart allows you to compare the average trading volume of multiple cryptocurrencies over a specific timeframe.
        - You can select a list of cryptocurrencies, a start date, an end date, and a timeframe.
        - It will display a bar chart comparing the average trading volume for each selected cryptocurrency.


        **Performance Comparison:**
            
        - This chart allows you to compare the performance of different cryptocurrencies over a specific timeframe.
        - You can select a list of cryptocurrencies, a start date, an end date, and a timeframe.
        - It will display a line chart showing the percentage change in price for each selected cryptocurrency.
        
        
        **Volatility Comparison:**

        - This chart allows you to compare the volatility of different cryptocurrencies over a specific timeframe.
        - You can select a list of cryptocurrencies, a start date, an end date, and a timeframe.
        - It will display a bar chart showing the average volatility for each selected cryptocurrency.


        **Fear & Greed Index Display:**

        - This section displays the current Fear & Greed Index for the cryptocurrency market.
        - The Fear & Greed Index measures the sentiment in the market, indicating whether it's driven by fear or greed.
        - The index ranges from 0 to 100, with lower values indicating fear and higher values indicating greed.
        - You'll see a gauge chart indicating the current sentiment, and it will fall into categories like "Buy," "Sell," "Strong Buy," or "Strong Sell" based on the index value.


        **Historical Data of Fear & Greed Index:**

        - This section provides a historical view of the Fear & Greed Index over time.
        - You'll see a line chart displaying how the sentiment has changed over a specified period.
        
        
        **Order Book Display:**

        - This section allows you to view the order book for a specific cryptocurrency.
        - You can select a cryptocurrency symbol, and it will display the buy and sell orders in the order book.
        - The order book provides insights into the current demand (buy orders) and supply (sell orders) for the selected cryptocurrency.
        
        
        **Cryptocurrency Events Display:**
        
        - This section provides information about upcoming cryptocurrency events.
        - You can explore events for a specific date.
        - It lists events such as coin launches, conferences, and other important announcements related to cryptocurrencies.
        
    
        **Trending Coins Display:**
        
        - In this section, you can discover the trending coins in the cryptocurrency market.
        - It displays a list of coins that are currently gaining popularity.
        - Trending coins can be an indicator of market interest and potential opportunities.
        
        
        
        
        """)
        

