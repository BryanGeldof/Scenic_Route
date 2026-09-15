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

# CSS om het volledige kader/achtergrondvlak volledig onzichtbaar te maken
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

    /* Posysionering linksboven */
    .element-container {
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 99999 !important;
        width: 340px !important;
    }

    /* WIS HET KADER: Maak de achtergrondcontainer volledig transparant en randloos */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background: transparent !important;
        backdrop-filter: none !important;
        -webkit-backdrop-filter: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* Strakke invoervelden */
    .stTextInput input {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 12px !important;
        padding: 10px 14px 10px 36px !important;
        font-size: 14px !important;
    }

    /* Strakke knop */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4) !important;
        cursor: pointer;
        margin-top: 4px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8) !important;
    }

    .stCheckbox label {
        color: #ffffff !important;
        font-size: 13px !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }
</style>
""", unsafe_allow_html=True)

# 1. Achtergrond Kaart (OpenStreetMap)
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=11,
    tiles="OpenStreetMap",
    zoom_control=False,
    attributionControl=False
)
st_folium(m, use_container_width=True, height=900)

# 2. Invoer elementen zonder enig achtergrondkader
with st.container():
    st.markdown("<h3 style='color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8); margin-bottom: 0px;'>🗺️ Scenic Navigator</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 12px; color: #cbd5e1; text-shadow: 0 1px 3px rgba(0,0,0,0.8); margin-top: 2px; margin-bottom: 8px;'>Plan je route of schilderachtige lus</p>", unsafe_allow_html=True)
    
    search_query = st.text_input("Bestemming", placeholder="🔍 Typ bestemming of adres...", label_visibility="collapsed")
    is_loop = st.checkbox("🔄 Maak schilderachtige lus vanaf locatie")
    
    if st.button("Start Route Berekenen 🚀"):
        if is_loop:
            st.success("🔄 Lus-modus geactiveerd!")
        elif search_query:
            st.success(f"🚀 Route gestart naar: **{search_query}**")
        else:
            st.warning("⚠️ Vul een bestemming in of kies een lus.")
