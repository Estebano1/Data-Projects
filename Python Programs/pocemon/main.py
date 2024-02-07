import streamlit as st
from api import fetch_data, get_all_pokemon

def main():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Comic+Sans+MS&display=swap');
        body {
            background-color: #FFE4B5;
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background-image: url('https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/2880px-International_Pok%C3%A9mon_logo.svg.png');
            background-size: 40%;
            background-position: center top;
            background-repeat: no-repeat;
        }
        p, h1, h2, h3, h4, h5, h6 {
            font-family: 'Comic Sans MS', cursive, sans-serif !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("")    
    st.title("")
    st.title("")
    st.title("")

    pokemon_name = st.text_input('Welches Pokemon möchtest du anschauen?').lower()

    data = fetch_data(pokemon_name)
    
    st.markdown("""
        <style>
        div.stButton > button:first-child {
        background-color: #0099ff;
        color: #ffd700;
        }
        div.stButton > button:hover {
        background-color: #f0f0f0;
        color: #000080;
        }
        </style>""", unsafe_allow_html=True)
    
    if st.button("Übersicht aller Pokemon"):
        all_pokemon = get_all_pokemon()
        if all_pokemon:
            st.header("Liste aller Pokémon:")
            for pokemon in all_pokemon:
                st.write(f"- {pokemon['name'].capitalize()}")
        else:
            st.warning("Fehler beim Abrufen der Pokémon-Liste. Stellen Sie sicher, dass die API verfügbar ist.")
    
    if data is not None:
        if 'sprites' in data and 'front_default' in data['sprites']:
            st.image(data['sprites']['front_default'], caption=pokemon_name.upper(), width=200)
        
        st.header("Informationen")
        if 'name' in data:
            st.write(f"Name: {data['name']}")
        if 'weight' in data:
            st.write(f"Gewicht: {data['weight']} hg")
        if 'height' in data:
            st.write(f"Größe: {data['height']} dm")
        
        st.header("Fähigkeiten")
        if 'abilities' in data:
            for ability in data['abilities']:
                if 'ability' in ability and 'name' in ability['ability']:
                    st.write(ability['ability']['name'])
            
        st.header("Statistiken")
        if 'stats' in data:
            for stat in data['stats']:
                if 'stat' in stat and 'name' in stat['stat'] and 'base_stat' in stat:
                    st.write(f"{stat['stat']['name']}: {stat['base_stat']}")
            
    else:
        st.warning("Fehler beim Abrufen der Daten. Stellen Sie sicher, dass der Pokemon-Name korrekt ist oder die API verfügbar ist.")

if __name__ == "__main__":
    main()
