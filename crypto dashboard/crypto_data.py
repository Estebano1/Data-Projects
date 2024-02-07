# Importieren von Bibliotheken
import pandas as pd  
import requests 
from binance.exceptions import BinanceAPIException
from binance.client import Client

# Importieren von API Keys aus benance.py
from benance import BINANCE_API_KEY, BINANCE_API_SECRET, COINMARKETCAL_API

# Binance API und Secret Keys 
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# CoinMarketCal API-Schlüssel
COINMARKETCAL_API_KEY = COINMARKETCAL_API

def format_price(value):
    if value < 0.01:
        # Für sehr kleine Werte unter einem Cent wird der ganze Preis angezeigt
        # Konvertieren in einen String um alle Nullen zu behalten
        return "{:.10f}".format(value).rstrip('0').rstrip('.')
    else:
        # Für größere Werte dann mit zwei Dezimalstellen
        return "{:.2f}".format(value)

    
def get_current_price(symbol):
    try:
        # Preis von der Binance-API abzurufen
        ticker = client.get_symbol_ticker(symbol=symbol)
        
        # Den Preis aus der API-Antwort extrahieren und in eine Gleitkommazahl konvertieren
        price = float(ticker['price'])
        
        # Die zuvor definierte Funktion format_price aufrufen, um den Preis zu formatieren
        return format_price(price)
    except BinanceAPIException as e:
        # Wenn ein Fehler bei der API-Anfrage auftritt, wird eine Fehlermeldung ausgegeben, und None wird zurückgegeben
        print(f"An error occurred: {e}")
        return None




def download_historical_data(symbol, start_date, end_date, timeframe):
    try:
        # Datum in Millisekunden konvertieren
        start_str = str(int(pd.to_datetime(start_date).timestamp() * 1000))
        end_str = str(int(pd.to_datetime(end_date).timestamp() * 1000))
        
        # Timeframe in das Binance-Format umwandeln
        timeframe_dict = {
            "4 hours": Client.KLINE_INTERVAL_4HOUR,
            "1 day": Client.KLINE_INTERVAL_1DAY,
            "1 week": Client.KLINE_INTERVAL_1WEEK,
            "1 month": Client.KLINE_INTERVAL_1MONTH
        }

        # API-Aufruf, um historische Daten zu erhalten
        klines = client.get_historical_klines(symbol, timeframe_dict[timeframe], start_str, end_str)

        # Daten in ein DataFrame umwandeln
        data = pd.DataFrame(klines, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])

        # Zeitstempel und Preise von Strings in numerische Werte konvertieren
        data['open_time'] = pd.to_datetime(data['open_time'], unit='ms')
        data['close_time'] = pd.to_datetime(data['close_time'], unit='ms')
        data['open'] = data['open'].astype(float)
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        data['close'] = data['close'].astype(float)
        data['volume'] = data['volume'].astype(float)

        data['average_price'] = (data['high'] + data['low']) / 2
        return data

    except BinanceAPIException as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # Gibt einen leeren DataFrame zurück



def calculate_bollinger_bands(data, window=20, num_of_std=2):
    # Berechnet die Bollinger Bands
    
    rolling_mean = data['close'].rolling(window=window).mean()
    rolling_std = data['close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_of_std)
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return rolling_mean, upper_band, lower_band




def calculate_percent_change(data):
    # Berechnet die prozentuale Veränderung
    start_price = data['close'].iloc[0]
    end_price = data['close'].iloc[-1]
    return (end_price - start_price) / start_price * 100






def calculate_volatility(data):    
    # Berechnen der täglichen Renditen
    daily_returns = data['close'].pct_change()
    # Berechnen der Volatilität als Standardabweichung der täglichen Renditen
    volatility = daily_returns.std()
    return volatility




def get_fear_greed_index():
    url = "https://api.alternative.me/fng/?limit=1"
    
    # API-Antwort abrufen und in JSON-Format umwandeln.
    response = requests.get(url)
    data = response.json()['data']
    
    # Daten in ein Pandas DataFrame konvertieren und Timestamp formatieren.
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    return df



def get_fear_greed_index_history(limit=30):
    url = f"https://api.alternative.me/fng/?limit={limit}"
    
    # API-Antwort abrufen und in JSON-Format umwandeln.
    response = requests.get(url)
    data = response.json()['data']
    
    # Daten in ein Pandas DataFrame konvertieren und Timestamp formatieren.
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Wert in numerischen Datentyp (float) konvertieren.
    df['value'] = pd.to_numeric(df['value'])
    return df



def get_order_book(symbol, limit=5000):
    try:
        # Binance-API-Aufruf, um das Orderbuch abzurufen
        order_book = client.get_order_book(symbol=symbol, limit=limit)
        return order_book
    except Exception as e:
        print(f"An error occurred while retrieving the order book data: {e}")
        return None

    
def get_coinmarketcal_events(api_key, start_date, end_date, categories=''):
    # Die URL für die API-Anfrage
    url = "https://developers.coinmarketcal.com/v1/events"
    
    # Die Header für die Anfrage festlegen, einschließlich des API-Schlüssels
    headers = {
        'x-api-key': api_key,
        'Accept-Encoding': 'deflate, gzip',
        'Accept': 'application/json'
    }
    
    # Die Parameter für die Datumsbereichs festlegen
    params = {
        'dateRangeStart': start_date.strftime('%Y-%m-%d'),
        'dateRangeEnd': end_date.strftime('%Y-%m-%d')
    }
    
    # Eine GET-Anfrage an die API senden
    response = requests.get(url, headers=headers, params=params)
    
    # Debug-Log nach Erhalt der Antwort
    print(f"Response from API: {response.text}")

    # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
    if response.status_code == 200:
        # Die JSON-Daten aus der Antwort extrahieren und zurückgeben
        return response.json()['body']
    else:
        print(f"Fehler beim Abrufen von Ereignissen: {response.status_code}")
        return []





def get_trending_coins_coingecko(limit=15):
    # Die URL für die API-Anfrage
    url = "https://api.coingecko.com/api/v3/search/trending"
    
    try:
        # Anfrage an die API senden
        response = requests.get(url)
        
        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            data = response.json()
            coins = data.get('coins', [])
            
            # Coins auswählen
            trending_coins = [{'name': coin['item']['name'], 'symbol': coin['item']['symbol']} for coin in coins[:limit]]
            
            return trending_coins
        else:
            print("API-Anfrage fehlgeschlagen mit Statuscode:", response.status_code)
            return []
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", str(e))
        return []



