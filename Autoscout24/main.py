import streamlit as st
import base64


from data_processing import load_data, get_sales_info, get_unique_brands, get_kraftstoff_preise_laufleistung, get_top_5_selling_brands

from visualization import create_correlation_heatmap, plot_average_price_trend, plot_average_mileage_trend, plot_average_hp_trend
from visualization import plot_price_distribution_by_make, plot_marken_trend_ueber_zeit, plot_top_marken, plot_top_modelle
from visualization import plot_kraftstoff_preise_laufleistung

from machine_learning import pie_plot, plot_avg_prices_by_brand, show_model_results, calculate_model_results, show_model_mae_results, train_and_predict_price 


def get_image_as_base64(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Pfad zum Bild
image_path = "/Users/Estebano/Data Bootcamp/Autoscout/bild.jpg"
image_base64 = get_image_as_base64(image_path)


def main():
    # Bild in Base64 konvertieren
    with open("/Users/Estebano/Data Bootcamp/Autoscout/background.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # Benutzerdefinierte CSS-Stile mit dem Hintergrundbild
    st.markdown(f"""
    <style>
        .reportview-container {{
            background: url("data:image/png;base64,{encoded_string}") no-repeat center center fixed;
            background-size: cover;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Bild in Base64 konvertieren für die Seitenleiste
    with open("/Users/Estebano/Data Bootcamp/Autoscout/sidebar5.jpeg", "rb") as image_file:
        sidebar_bg_encoded = base64.b64encode(image_file.read()).decode()

    # Benutzerdefinierte CSS-Stile für die Seitenleiste
    st.markdown(f"""
    <style>
        .sidebar .sidebar-content {{
            background: url("data:image/png;base64,{sidebar_bg_encoded}") center/cover no-repeat;
            background-size: cover;
        }}
        /* Anpassen der Farbe und Größe der Schrift in der Seitenleiste */
        .sidebar .sidebar-content {{
            color: #00000;
        }}
        /* Weitere Stile können hier hinzugefügt werden */
    </style>
    """, unsafe_allow_html=True)
    
    logo_url = "https://www.autoscout24.de/cms-content-assets/4ydEzuq5aFVUjXdvHLripG-7eb7ed609239464291ac4b2f1dac2927-autoscout24redesign23-1100.png"
    
    # Benutzerdefinierte HTML/CSS für das Logo
    logo_html = f"""
    <div style="position: fixed; top: 0; right: 0; padding: 10px; z-index: 9999;">
        <img src="{logo_url}" alt="AutoScout24" style="height: 60px;">
    </div>
    """

    # Logo mit st.markdown einfügen
    st.markdown(logo_html, unsafe_allow_html=True)
    
    st.sidebar.title("AutoScout24")
    
    
    # Local image path
    local_image_path = "/Users/Estebano/Data Bootcamp/Autoscout/bild.jpeg"
    
    # Display the local image in the Streamlit sidebar
    st.sidebar.image(local_image_path, width=295)
   
    
        

    page = st.sidebar.selectbox("Wählen Sie eine Seite:", ["Startseite", "Überblick", "Analyse", "Machine Learning", "Preisvorhersage"])


    st.sidebar.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    st.sidebar.markdown("### Weitere Informationen")
    st.sidebar.markdown(
        "Besuchen Sie <a href='https://www.autoscout24.de' style='color: #FFFFCC; text-decoration: none;'>AutoScout24</a> für weitere Details zu Fahrzeugen und Angeboten.",
        unsafe_allow_html=True
    )
    

    st.sidebar.markdown("#### *Die App wurde erstellt von*")
    st.sidebar.markdown("*Stephan K.*")



    data = load_data()


    if page == "Startseite":
        st.markdown("""
            <h2 style='text-align: center; color: black;'>Willkommen bei der AutoScout24 Datenanalyse</h2>
            <p>
                In dieser App analysieren wir Daten von verkaufen Autos auf AutoScout24. 
                Entdecken Sie interessante Einblicke in die Verkaufszahlen, Markenverteilungen 
                und vieles mehr. Navigieren Sie durch die verschiedenen Seiten der App, 
                um detaillierte Analysen und Visualisierungen zu entdecken.
            </p>
        """, unsafe_allow_html=True)
        
        
        # Bild von der URL anzeigen mit angepasster Größe
        image_url = "https://play-lh.googleusercontent.com/11ERRMssqX5_4-8Aquo1MsQp7fnlxtE0tmV2Zhdnh2835jvToOrMkZwu2sbts2Rqp1V-"
        st.image(image_url, width=693)  # Breite auf 500 Pixel einstellen



    elif page == "Überblick":
        data = load_data()
        autos_verkauft, zeitraum = get_sales_info(data)
        marken = get_unique_brands(data)
    
        st.markdown("""
        <style>
            .info-box {
                background-color: rgba(255, 255, 255, 0.2); /* Weiß mit leichter Transparenz */
                border-radius: 10px;
                padding: 50px;
                margin: 10px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
                font-family: 'Roboto', sans-serif; /* Moderne Schriftart */
            }
            .info-title {
                font-size: 23px;
                color: #4a4a4a; /* Dunkelgrau für Titel */
                margin-bottom: 15px; /* Etwas mehr Abstand nach unten */
                text-transform: uppercase; /* Text in Großbuchstaben */
                letter-spacing: 1px; /* Buchstabenabstand erhöhen */
            }
            .info-value {
                font-size: 23px; /* Größe der Zahlen erhöhen */
                color: #264653; /* Farbiger Akzent für Werte */
                margin-bottom: 50px; /* Mehr Abstand nach unten */
                font-weight: bold; /* Schrift fett machen */
            }
            .info-footer {
                font-size: 20px;
                color: #264653; /* Dunklerer Farbton für Fußzeile */
                margin-top: 15px; /* Abstand nach oben hinzufügen */
            }
        </style>
        """, unsafe_allow_html=True)
    
        st.markdown(f"""
        <div class='info-box'>
            <div class='info-title'>Anzahl verkaufter Autos</div>
            <div class='info-value'>{autos_verkauft}</div>
            <div class='info-title'>Verkaufszeitraum</div>
            <div class='info-value'>{zeitraum[0]} - {zeitraum[1]}</div>
            <div class='info-title'>erfasste Marken</div>
            <div class='info-footer'><strong>{', '.join(marken)}</strong></div>
        </div>
        """, unsafe_allow_html=True)


    elif page == "Analyse":
        data = load_data()
    
        st.markdown("<h2 style='text-align: center;'>Heatmap der Korrelationsmatrix</h2>", unsafe_allow_html=True)
        fig = create_correlation_heatmap(data)
        st.pyplot(fig)
        st.write("""
        - Kilometerstand und Jahr korrelieren negativ mit -0.68 (neuere Autos haben tendenziell eine geringere Laufleistung).
        - PS & Preis korrelieren positiv mit 0.75 (Autos mit mehr Leistung sind tendenziell teurer).
        - Preis & Jahr korrelieren positiv mit 0.41 (neue Autos sind tendenziell teurer).
        """)

    
        st.markdown("<h2 style='text-align: center;'>Durchschnittspreis der Autos über die Jahre</h2>", unsafe_allow_html=True)
        fig = plot_average_price_trend(data)
        st.pyplot(fig)
        st.write("""
        **Durchschnittspreis-Entwicklung:** Die Preisentwicklung von Autos zeigt einen kontinuierlichen Anstieg im Laufe der Jahre. 
        Dieser Trend kann auf verschiedene Faktoren zurückgeführt werden, wie die Einführung neuerer Modelle mit fortschrittlicheren 
        Technologien oder allgemeine Marktinflation. Dieser Anstieg könnte aber auch darauf hinweisen, dass hochwertige oder luxuriöse 
        Fahrzeugmodelle an Beliebtheit gewonnen haben.
        """)
    
        st.markdown("<h2 style='text-align: center;'>Durchschnittliche Laufleistung der Autos über die Jahre</h2>", unsafe_allow_html=True)
        fig = plot_average_mileage_trend(data)
        st.pyplot(fig)
        st.write("""
        **Veränderungen in der durchschnittlichen Laufleistung:** Der kontinuierliche Rückgang der durchschnittlichen Laufleistung 
        über die Jahre könnte darauf hinweisen, dass Autos früher ausgetauscht werden oder dass neuere Fahrzeuge mit geringerer 
        Laufleistung bevorzugt werden. Dies könnte ebenso auf die gesteigerte Langlebigkeit und Zuverlässigkeit der Fahrzeuge hinweisen.
        """)

        st.markdown("<h2 style='text-align: center;'>Durchschnittliche PS der Autos über die Jahre</h2>", unsafe_allow_html=True)
        fig = plot_average_hp_trend(data)
        st.pyplot(fig)
        st.write("""
        **Durchschnittliche PS der Autos:** Die Daten zeigen einen klaren Anstieg ab dem Jahr 2016. Dies könnte auf ein wachsendes 
        Interesse an leistungsstärkeren Fahrzeugen hinweisen, möglicherweise bedingt durch technologische Innovationen oder 
        Veränderungen in den Präferenzen der Käufer in Richtung leistungsstarker Fahrzeuge.
        """)
    
        st.markdown("<h2 style='text-align: center;'>Top Marken</h2>", unsafe_allow_html=True)
        fig = plot_top_marken(data)
        st.pyplot(fig)
    
        st.markdown("<h2 style='text-align: center;'>Top Modelle</h2>", unsafe_allow_html=True)
        fig = plot_top_modelle(data)
        st.pyplot(fig)
    
        st.markdown("<h2 style='text-align: center;'>Trend der Top Marken über die Jahre</h2>", unsafe_allow_html=True)
        fig = plot_marken_trend_ueber_zeit(data, top_n=10)
        st.plotly_chart(fig)
        st.write("""
        **Trends bei Marken und Modellen:** Volkswagen, Opel, Ford, Skoda und Renault gehören zu den am häufigsten 
        vertretenen Marken. Bei den Modellen dominieren der Golf, Corsa, Fiesta, Astra und Focus. Im Laufe der Zeit
        hat sich die Popularität dieser Top-Marken verändert. Während einige Marken wie Volkswagen und Ford im Jahr 
        2022 einen Rückgang verzeichnen, erleben andere, insbesondere Skoda, aber auch Opel und Renault, einen Aufwärtstrend. 
        Dies könnte auf einen möglichen Trend zu günstigeren Marken hindeuten, möglicherweise als Reaktion auf wirtschaftliche 
        Veränderungen wie die Corona-Pandemie. Volkswagen hält trotz des Rückgangs immer noch den höchsten Durchschnittspreis, 
        dicht gefolgt von Ford und dann Skoda.
        """)
        
        
        st.markdown("<h2 style='text-align: center;'>Einfluss von Kraftstofftypen auf Preise und Laufleistung</h2>", unsafe_allow_html=True)
        kraftstoff_preise, kraftstoff_laufleistung = get_kraftstoff_preise_laufleistung(data, min_eintraege=10)
        fig = plot_kraftstoff_preise_laufleistung(kraftstoff_preise, kraftstoff_laufleistung)
        st.pyplot(fig)
        st.write("""
        **Einfluss von Kraftstofftypen auf Preise und Laufleistung:** Die Analyse des Einflusses von Kraftstofftypen auf Preise 
        und Laufleistung offenbart signifikante Unterschiede. Elektrische Autos sind im Durchschnitt teurer als solche mit Diesel- 
        oder Benzinmotoren, während Fahrzeuge mit Ethanol-Kraftstoff deutlich günstiger sind. Dies spiegelt sich auch in der 
        Laufleistung wider, wobei Diesel-Autos tendenziell die höchste Laufleistung aufweisen. Im Gegensatz dazu zeigen elektrische 
        Fahrzeuge und solche mit alternativen Kraftstoffen wie Wasserstoff eine geringere Laufleistung. Diese Unterschiede sind 
        wichtige Indikatoren für die Gesamtperformance und die Kosten-Nutzen-Bilanz der verschiedenen Kraftstofftypen.
        """)


        st.markdown("<h2 style='text-align: center;'>Durchschnittspreis nach Marke</h2>", unsafe_allow_html=True)
        fig = plot_price_distribution_by_make(data)
        st.pyplot(fig)
    


    elif page == "Machine Learning":
        # Laden Sie die Daten und berechnen Sie die Top-Marken
        data = load_data()
        top_marken_df = get_top_5_selling_brands(data)
        top_marken = top_marken_df.index.tolist()  # Erstellen Sie eine Liste der Top-Marken
    
    
        st.markdown("""
        <h2 style='text-align: center;'>Machine Learning Analyse</h2>
        <p>Im folgenden Abschnitt konzentrieren wir uns auf die Analyse der fünf Top-Marken. Wir werden untersuchen, 
        wie teuer durchschnittlich ein Auto von jedem dieser Hersteller ist und versuchen, mit einem Machine Learning-Modell 
        den Verkaufspreis eines Autos basierend auf ausgewählten Features vorherzusagen. Dabei werden wir verschiedene Modelle 
        und Evaluierungsmethoden betrachten, um die Qualität der Vorhersagen zu beurteilen.</p>
        """, unsafe_allow_html=True)
        
        pie_plot(data, top_marken)


        plot_avg_prices_by_brand(data, top_marken)
        st.markdown("<h3 style='text-align: center;'>Analyse und Vergleich verschiedener Modelle zur Preisvorhersage</h3>", unsafe_allow_html=True)

        # Ergebnisse von den Modellen berechnen
        model_results = calculate_model_results(data, top_marken)
        show_model_results(model_results)
        show_model_mae_results(model_results)
        
     

    elif page == "Preisvorhersage":
        st.title("Preisvorhersage für Autos")
    
        # Eingabefelder mit Slidern
        mileage = st.slider("Laufleistung (in km)", min_value=0, max_value=300000, value=100000, step=1000)
        hp = st.slider("Leistung (in PS)", min_value=0, max_value=500, value=150, step=10)
        year = st.slider("Baujahr", min_value=2011, max_value=2021, value=2015, step=1)
    
        # Vorhersage-Button
        if st.button("Preis vorhersagen"):
            with st.spinner('Berechne Vorhersage...'):
                predicted_price = train_and_predict_price(mileage, hp, year)
    
            # Container für Bild und Text mit Flexbox
            st.markdown(f"""
                <div style='display: flex; align-items: center; justify-content: center;'>
                    <div style='flex: 1; margin-right: 20px;'>
                        <img src='data:image/jpeg;base64,{image_base64}' style='max-width: 100%; height: auto; border-radius: 10px;'>
                    </div>
                    <div style='flex: 1; text-align: center;'>
                        <h3 style='color: black;'>Vorhergesagter Preis:</h3>
                        <h1 style='color: gold;'>{predicted_price:.2f}€</h1>
                    </div>
                </div>
                """, unsafe_allow_html=True)

          
            
            
        

if __name__ == "__main__":
    main()

