import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import matplotlib.colors as mcolors






from data_processing import get_price_distribution_by_make


def create_correlation_heatmap(data):
    # Erstellen der Figur und Achsen
    fig, ax = plt.subplots(figsize=(8, 6))

    # Einstellen der Transparenz für Figur und Achsen
    fig.patch.set_alpha(0.0)
    ax.set_alpha(0.0)

    # Erstellen der Heatmap
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='YlGnBu', ax=ax)

    # Entfernen der Achsenrahmen
    for edge, spine in ax.spines.items():
        spine.set_visible(False)



def plot_average_price_trend(data):
    jahres_trends = data.groupby('year').agg({'price':'mean'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))

    # Einstellen der Transparenz für Figur und Achsen
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    # Anpassen des Grids und der Linienfarbe, Rahmenfarbe auf Schwarz setzen
    ax.grid(True, color='black')
    for spine in ax.spines.values():
        spine.set_color('black')
    
    sns.lineplot(x='year', y='price', data=jahres_trends, marker='o', ax=ax, color='black')
    ax.set_ylabel('Durchschnittspreis (€)', fontsize=13)
    ax.set_xlabel('Baujahr')

    return fig


def plot_average_mileage_trend(data):
    jahres_trends = data.groupby('year').agg({'mileage':'mean'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    ax.grid(True, color='black')
    for spine in ax.spines.values():
        spine.set_color('black')
    
    sns.lineplot(x='year', y='mileage', data=jahres_trends, color='black', marker='o')
    plt.ylabel('Durchschnittliche Laufleistung (km)')
    plt.xlabel('Baujahr')
    return plt


def plot_average_hp_trend(data):
    jahres_trends = data.groupby('year').agg({'hp':'mean'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    
    ax.grid(True, color='black')
    for spine in ax.spines.values():
        spine.set_color('black')
    
    sns.lineplot(x='year', y='hp', data=jahres_trends, color='black', marker='o')
    plt.ylabel('Durchschnittliche PS')
    plt.xlabel('Baujahr')
    return plt


def plot_price_distribution_by_make(data, top_n=None):
    df = get_price_distribution_by_make(data)
    if top_n:
        df = df.head(top_n)

    fig_height = max(6, len(df) * 0.6)  # Erhöhung des Multiplikators für mehr Abstand zwischen den Balken
    fig, ax = plt.subplots(figsize=(10, fig_height))

    # Farbverlauf erstellen
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["#D2B48C", "#FFBF00"])


    color_range = np.linspace(0.1, 1, len(df))  # Erzeugt einen Bereich von Werten für den Farbverlauf
    colors = cmap(color_range)  # Anwenden des Farbverlaufs  

    # Einstellen der Transparenz für Figur und Achsen
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')

    # Entfernen von Grid, Rahmen und Achsenbeschriftungen
    ax.grid(False)
    ax.xaxis.set_visible(False)  # x-Achse ausblenden
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Erstellen des Balkendiagramms mit Farbverlauf
    sns.barplot(x=df.values, y=df.index, ax=ax, palette=colors)

    # Werte hinter die Balken setzen
    for p in ax.patches:
        ax.text(p.get_width(), p.get_y() + p.get_height() / 2, f'{p.get_width():.2f} €', 
                va='center', ha='left', fontsize=12)

    # Titel
    ax.set_ylabel('Marke')

    plt.tight_layout()
    return fig



def plot_marken_trend_ueber_zeit(data, top_n=20):
    top_marken = data['make'].value_counts().head(top_n).index.tolist()
    trend_data = data[data['make'].isin(top_marken)].groupby(['year', 'make']).size().reset_index(name='count')
    
    fig = px.line(trend_data, x='year', y='count', color='make', 
                  hover_name='make',  # Interaktive Informationen anzeigen
                  labels={'count': 'Anzahl der Verkäufe'})

    # Layout anpassen
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='black'),
        xaxis=dict(showgrid=False, zeroline=False, showline=False, fixedrange=True),  # Weiße Linie und Achsenlinie entfernen
        yaxis=dict(showgrid=False, fixedrange=True),
        showlegend=True  # Legende anzeigen
    )

    # Interaktive Legende aktivieren
    fig.update_traces(mode='lines+markers', hoverinfo='text+name')

    return fig


def plot_top_marken(data, top_n=20):
    marken = data['make'].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=marken.values, y=marken.index, ax=ax)

    ax.set_xlabel('Anzahl der Autos')
    ax.set_ylabel('Marke', fontsize=13)
    ax.xaxis.set_visible(False)
    ax.set_facecolor('none')

    for spine in ax.spines.values():
        spine.set_visible(False)  # Rahmen entfernen

    # Werte direkt auf die Balken setzen
    for p in ax.patches:
        ax.text(p.get_width() - (p.get_width() * 0.05), p.get_y() + p.get_height() / 2, 
                f'{int(p.get_width())}', va='center', ha='right', fontsize=12, color='black')

    fig.patch.set_alpha(0.0)  # Hintergrund der Figur transparent setzen
    plt.tight_layout()
    return fig





def plot_top_modelle(data, top_n=20):
    modelle = data['model'].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=modelle.values, y=modelle.index, ax=ax)

    ax.set_xlabel('Anzahl der Autos')
    ax.set_ylabel('Marke', fontsize=13)
    ax.xaxis.set_visible(False)
    ax.set_facecolor('none')

    for spine in ax.spines.values():
        spine.set_visible(False)  # Rahmen entfernen

    # Werte direkt auf die Balken setzen
    for p in ax.patches:
        ax.text(p.get_width() - (p.get_width() * 0.05), p.get_y() + p.get_height() / 2, 
                f'{int(p.get_width())}', va='center', ha='right', fontsize=12, color='black')

    fig.patch.set_alpha(0.0)  # Hintergrund der Figur transparent setzen
    plt.tight_layout()
    return fig



def plot_kraftstoff_preise_laufleistung(kraftstoff_preise, kraftstoff_laufleistung):
    fig, ax = plt.subplots(1, 2, figsize=(14, 8))

    # Einstellen der Transparenz für Figur und Achsen
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)

    for axe in ax:
        axe.set_facecolor('none')
        axe.grid(False)
        axe.xaxis.set_visible(False)  # x-Achse ausblenden
        axe.tick_params(left=False)  # Y-Achsen-Ticks ausblenden

        # Schriftgröße der Kraftstofftypen auf der Y-Achse erhöhen
        axe.tick_params(axis='y', labelsize=14)  # Hier wird die Schriftgröße angepasst

        # Rahmen entfernen
        for spine in axe.spines.values():
            spine.set_visible(False)

    # Durchschnittspreis nach Kraftstofftyp
    sns.barplot(x='price', y='fuel', data=kraftstoff_preise, ax=ax[0])
    ax[0].set_title('Durchschnittspreis nach Kraftstofftyp', fontsize=19, pad=20)

    # Werte auf die Balken setzen (Preis)
    for p in ax[0].patches:
        ax[0].text(p.get_width() - (0.05 * p.get_width()), p.get_y() + p.get_height() / 2, 
                   f'{p.get_width():.2f} €', va='center', ha='right', fontsize=15)

    # Durchschnittliche Laufleistung nach Kraftstofftyp
    sns.barplot(x='mileage', y='fuel', data=kraftstoff_laufleistung, ax=ax[1])
    ax[1].set_title('Durchschnittliche Laufleistung nach Kraftstofftyp', fontsize=19, pad=20)

    # Werte auf die Balken setzen (Laufleistung)
    for p in ax[1].patches:
        ax[1].text(p.get_width() - (0.05 * p.get_width()), p.get_y() + p.get_height() / 2, 
                   f'{p.get_width():.0f} km', va='center', ha='right', fontsize=15)

    plt.tight_layout()
    return fig

