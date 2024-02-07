import pandas as pd

def load_data():
    data = pd.read_csv('autoscout24.csv')

    # Entfernen von Zeilen mit Nullwerten
    data = data.dropna()

    return data


def get_sales_info(data):
    autos_verkauft = data.shape[0]
    zeitraum = (data['year'].min(), data['year'].max())
    return autos_verkauft, zeitraum

def get_unique_brands(data):
    marken = data['make'].unique()
    marken.sort()
    return marken


def get_price_distribution_by_make(data):
    return data.groupby('make')['price'].mean().sort_values(ascending=False)



def get_top_marken_modelle(data):
    marken = data['make'].value_counts()
    modelle = data['model'].value_counts()
    top_marken = marken.head(5).index.tolist()
    return marken, modelle, top_marken

def get_marken_trend_ueber_zeit(data, top_marken):
    return data[data['make'].isin(top_marken)].groupby(['year', 'make']).size().unstack().fillna(0)

def get_top_modelle_verkaufszahlen(data, top_modelle):
    data['make_model'] = data['make'] + " " + data['model']
    top_modelle_df = data[data['make_model'].isin(top_modelle)]
    return top_modelle_df['make_model'].value_counts().reset_index(name='Verkaufszahlen').rename(columns={'index': 'Make and Model'})

def get_kraftstoff_preise_laufleistung(data, min_eintraege=10):
    # Zählen der Einträge je Kraftstofftyp
    kraftstoff_eintraege = data['fuel'].value_counts()
    haeufige_kraftstoffe = kraftstoff_eintraege[kraftstoff_eintraege >= min_eintraege].index

    # Filtern des DataFrames, um nur häufige Kraftstofftypen zu berücksichtigen
    gefilterte_data = data[data['fuel'].isin(haeufige_kraftstoffe)]

    kraftstoff_preise = gefilterte_data.groupby('fuel').agg({'price':'mean'}).reset_index()
    kraftstoff_laufleistung = gefilterte_data.groupby('fuel').agg({'mileage':'mean'}).reset_index()
    return kraftstoff_preise, kraftstoff_laufleistung


def get_top_5_selling_brands(data): 
    return data['make'].value_counts().head(5)
