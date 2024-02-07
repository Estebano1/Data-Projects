import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

from data_processing import load_data, get_top_5_selling_brands







def pie_plot(data, top_marken):
    st.markdown("<h3 style='text-align: center;'>Top 5 Meistverkaufte Marken</h3>", unsafe_allow_html=True)
    top_marken_df = data['make'].value_counts().head(5).reset_index()
    top_marken_df.columns = ['Marke', 'Anzahl']
    colors = ['#2a9d8f', '#264653', '#e9c46a', '#f4a261', '#e76f51']
    fig1 = px.pie(top_marken_df, values='Anzahl', names='Marke', color_discrete_sequence=colors)
    fig1.update_traces(textinfo='value+label', marker=dict(line=dict(color='#ffffff', width=2)))
    fig1.update_layout(showlegend=False, plot_bgcolor='rgba(255, 255, 255, 0)', paper_bgcolor='rgba(255, 255, 255, 0)')
    st.plotly_chart(fig1)

def plot_avg_prices_by_brand(data, top_marken):
    st.markdown("<h3 style='text-align: center;'>Durchschnittspreise der Top 5 Marken</h3>", unsafe_allow_html=True)
    top_marken_avgprice = data[data['make'].isin(top_marken)].groupby('make')['price'].mean().sort_values(ascending=False).reset_index()
    colors = ['#2a9d8f', '#e9c46a', '#f4a261', '#e76f51', '#264653']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='price', y='make', data=top_marken_avgprice, ax=ax, palette=colors)

    ax.set_xlabel('Durchschnittspreis (€)')
    ax.set_ylabel('Marke')
    ax.xaxis.set_visible(False)
    ax.set_facecolor('none')

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Schriftgröße der Markennamen auf der Y-Achse erhöhen
    ax.tick_params(axis='y', labelsize=14)

    for index, p in enumerate(ax.patches):
        text_color = 'white' if index == 4 else 'black'
        ax.text(p.get_width(), p.get_y() + p.get_height() / 2, 
                f'{p.get_width():,.2f} €', va='center', ha='right', fontsize=12, color=text_color)

    fig.patch.set_alpha(0.0)
    plt.tight_layout()
    st.pyplot(fig)



def calculate_model_results(data, top_marken):
    df_top5 = data[data['make'].isin(top_marken)]
    X = df_top5[['mileage', 'hp', 'year']]
    y = df_top5['price']
    X = X.dropna()
    y = y[X.index]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'KNN': KNeighborsRegressor(n_neighbors=5)
    }

    results = []
    for model_name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5
        mae = mean_absolute_error(y_test, y_pred)  # Berechnung des MAE
        percent_error_mae = (mae / df_top5['price'].mean()) * 100  # Prozentsatz basierend auf MAE
        percent_error_rmse = (rmse / df_top5['price'].mean()) * 100  # Prozentsatz basierend auf RMSE
        results.append({
            'Modell': model_name, 
            'RMSE': rmse, 
            'MAE': mae,
            'Prozentuale Abweichung vom optimalen MAE': percent_error_mae,
            'Prozentuale Abweichung vom optimalen RMSE': percent_error_rmse
        })

    return results



def show_model_results(results):
    # Umwandeln der Ergebnisse in ein DataFrame und Berechnung der prozentualen Genauigkeit
    df_results = pd.DataFrame(results)
    df_results['Prozentuale Genauigkeit'] = 100 - df_results['Prozentuale Abweichung vom optimalen RMSE']

    # Ergebnisse extrahieren
    lr_results = next(item for item in results if item["Modell"] == "Linear Regression")
    rf_results = next(item for item in results if item["Modell"] == "Random Forest")
    knn_results = next(item for item in results if item["Modell"] == "KNN")
    

    st.markdown("<h2 style='text-align: center;'>RMSE Abweichung</h2>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(12, 7))  
    sns.barplot(x='Modell', y='RMSE', data=pd.DataFrame(results), ax=ax, palette=['#D9B08C', '#73C6B6', '#F9E79F'])

    # Style-Anpassungen
    ax.set_xlabel('Modell', fontsize=14)
    ax.set_ylabel('RMSE (€)', fontsize=14)
    ax.set_facecolor('none')  # Hintergrund der Achsen transparent setzen
    ax.grid(False)  # Gitternetz ausblenden
    for spine in ax.spines.values():
        spine.set_visible(False)  # Rahmen entfernen
    ax.tick_params(axis='x', labelsize=14)
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width()/2., p.get_height(), 
                f'{p.get_height():,.2f} €', 
                fontsize=14, ha='center', va='bottom')
    fig.patch.set_alpha(0.0)  # Hintergrund der Figur transparent setzen
    plt.tight_layout()
    st.pyplot(fig)


    # Markdown-Text mit eingefügten Werten
    st.markdown(f"""
        <div class='info-box'>
            <h4>Modellergebnisse im Überblick:</h4>
            <ul>
                <li><b>Lineare Regression</b>: RMSE von {lr_results['RMSE']:.2f} €, mit einer prozentualen Abweichung von {lr_results['Prozentuale Abweichung vom optimalen RMSE']:.2f}%. Die lineare Regression zeigt eine mittlere Fehlerquote von etwa einem Drittel des durchschnittlichen Verkaufspreises.</li>
                <li><b>Random Forest</b>: RMSE von {rf_results['RMSE']:.2f} €, mit einer prozentualen Abweichung von {rf_results['Prozentuale Abweichung vom optimalen RMSE']:.2f}%.  Mit einer Fehlerquote von etwa einem Viertel des durchschnittlichen Verkaufspreises erzielt das Random Forest-Modell solide Ergebnisse.</li>
                <li><b>K-Nearest Neighbors (KNN)</b>: RMSE von {knn_results['RMSE']:.2f} €, mit einer prozentualen Abweichung von {knn_results['Prozentuale Abweichung vom optimalen RMSE']:.2f}%. Das KNN-Modell zeigt eine signifikante prozentuale Abweichung.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        
        
def show_model_mae_results(results):
    # Umwandeln der Ergebnisse in ein DataFrame
    df_results = pd.DataFrame(results)

    st.markdown("<h2 style='text-align: center;'>MAE Abweichung</h2>", unsafe_allow_html=True)

    # Balkendiagramm zur Visualisierung der MAE-Werte
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.barplot(x='Modell', y='MAE', data=df_results, ax=ax, palette=['#D9B08C', '#73C6B6', '#F9E79F'])

    # Style-Anpassungen
    ax.set_xlabel('Modell', fontsize=14)
    ax.set_ylabel('MAE (€)', fontsize=14)
    ax.set_facecolor('none')  # Hintergrund der Achsen transparent setzen
    ax.grid(False)  # Gitternetz ausblenden
    for spine in ax.spines.values():
        spine.set_visible(False)  # Rahmen entfernen
    ax.tick_params(axis='x', labelsize=14)
    for p in ax.patches:
        ax.text(p.get_x() + p.get_width()/2., p.get_height(), 
                f'{p.get_height():,.2f} €', 
                fontsize=14, ha='center', va='bottom')
    fig.patch.set_alpha(0.0)  # Hintergrund der Figur transparent setzen
    plt.tight_layout()
    st.pyplot(fig)

    
    
        # Extrahieren der Ergebnisse für jedes Modell
    lr_results = next(item for item in results if item["Modell"] == "Linear Regression")
    rf_results = next(item for item in results if item["Modell"] == "Random Forest")
    knn_results = next(item for item in results if item["Modell"] == "KNN")

    # Markdown-Text für MAE-Ergebnisse
    st.markdown(f"""
        <div class='info-box'>
            <h4>MAE-Ergebnisse im Überblick:</h4>
            <ul>
                <li><b>Lineare Regression</b>: MAE beträgt {lr_results['MAE']:.2f} €, was etwa einem Drittel des durchschnittlichen Verkaufspreises entspricht.</li>
                <li><b>Random Forest</b>: MAE von {rf_results['MAE']:.2f} €. Der Random Forest liefert damit die beste Ergebnisse .</li>
                <li><b>K-Nearest Neighbors (KNN)</b>: MAE von {knn_results['MAE']:.2f} €. Das KNN-Modell zeigt den höchsten MAE und ist damit nicht geeignet.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)





def train_and_predict_price(mileage, hp, year):
    # Daten laden und aufbereiten (ähnlich wie in calculate_model_results)
    data = load_data()  # Stelle sicher, dass diese Funktion deine Daten korrekt lädt
    top_marken = get_top_5_selling_brands(data).index.tolist()
    df_top5 = data[data['make'].isin(top_marken)]

    X = df_top5[['mileage', 'hp', 'year']]
    y = df_top5['price']

    # Trainiere das Modell (Hier könnte man auch das Modell laden, wenn es bereits trainiert wurde)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # Mache eine Vorhersage mit den übergebenen Daten
    predicted_price = rf_model.predict([[mileage, hp, year]])[0]
    return predicted_price



