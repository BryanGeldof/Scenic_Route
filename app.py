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

# Styling voor de perfecte pil-vormige zoekbalk rechtsboven
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

    /* Posysionering van het zoekelement rechtsboven */
    .element-container {
        position: fixed !important;
        top: 24px !important;
        right: 24px !important;
        left: auto !important;
        z-index: 99999 !important;
        width: 380px !important;
    }

    /* Pil-vormig inputveld met ruimte aan de rechterkant voor de knop */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 14px 70px 14px 24px !important;
        font-size: 15px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        outline: none !important;
    }

    .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }

    .stTextInput label {
        display: none !important;
    }

    /* Zet de knop exact aan de RECHTERKANT in de pil */
    .stButton {
        position: absolute !important;
        right: 6px !important;
        top: 6px !important;
        z-index: 100000 !important;
    }

    .stButton>button {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 50% !important;
        border: none !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        cursor: pointer !important;
        font-size: 15px !important;
    }

    .stButton>button:hover {
        background-color: #0f172a !important;
        transform: scale(1.05);
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

# 2. Zoekbalk rechtsboven met de knop netjes rechts ingebouwd
with st.container():
    search_query = st.text_input("Zoeken", placeholder="Search...", label_visibility="collapsed")
    
    if st.button("🔍") or search_query:
        if search_query:
            st.toast(f"🚀 Route gestart naar: {search_query}", icon="🗺️")
