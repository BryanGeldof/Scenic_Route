import streamlit as st
import folium
from streamlit_folium import st_folium

# Pagina configuratie
st.set_page_config(
    page_title="Scenic Route Navigator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Strakke Styling: Rechthoekig zoekveld met afgeronde hoeken en wit vergrootglas-icoon
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0b0f19;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Achtergrondkaart vult het volledige scherm */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 0;
    }

    /* Posysionering rechtsboven */
    .element-container {
        position: fixed !important;
        top: 24px !important;
        right: 24px !important;
        left: auto !important;
        z-index: 99999 !important;
        width: 380px !important;
    }

    /* Rechthoekig zoekveld met mooi afgeronde hoeken (geen ovaal/pil) */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        padding: 12px 55px 12px 16px !important;
        font-size: 15px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
        outline: none !important;
    }

    .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }

    .stTextInput label {
        display: none !important;
    }

    /* De knop met een strak wit vergrootglas (cirkel + handvat) erin verwerkt */
    .stButton {
        position: absolute !important;
        right: 6px !important;
        top: 6px !important;
        z-index: 100000 !important;
    }

    .stButton>button {
        background-color: #1e293b !important;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        color: transparent !important;
        border-radius: 8px !important;
        border: none !important;
        width: 38px !important;
        height: 38px !important;
        padding: 0 !important;
        cursor: pointer !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        transition: background-color 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. Achtergrond Kaart
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=11,
    tiles="OpenStreetMap",
    zoom_control=False,
    attributionControl=False
)
st_folium(m, use_container_width=True, height=900)

# 2. Zoekbalk rechtsboven met het witte vergrootglas
with st.container():
    search_query = st.text_input("Zoeken", placeholder="Search...", label_visibility="collapsed")
    
    if st.button("Zoek") or search_query:
        if search_query:
            st.toast(f"🚀 Route gestart naar: {search_query}", icon="🗺️")
