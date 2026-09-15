import streamlit as st
import folium
from streamlit_folium import st_folium

# Pagina configuratie op full-width en ingeklapte sidebar
st.set_page_config(
    page_title="Scenic Route Navigator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-premium Waze/Google Maps Glassmorphism Styling
st.markdown("""
<style>
    /* Verberg standaard Streamlit elementen, headers en footers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0b0f19;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    
    /* Zorg dat de hoofdcontainer absoluut geen marges heeft */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Forceer de kaart om het volledige scherm te vullen achter de overlay */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 0;
    }

    /* Ultra-premium zwevend Waze / Google Maps bedieningspaneel linksboven */
    .floating-control-panel {
        position: fixed;
        top: 24px;
        left: 24px;
        z-index: 99999;
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 24px;
        border-radius: 20px;
        width: 380px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.05);
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .floating-control-panel h2 {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 4px;
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .floating-control-panel p {
        font-size: 13px;
        color: #94a3b8;
        margin-bottom: 16px;
    }

    /* Strakke inputvelden in Waze-stijl */
    .stTextInput>div>div>input {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }

    /* Futuristische gradient navigatieknop */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%) !important;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.6) !important;
        transform: translateY(-1px);
    }

    /* Checkbox styling */
    .stCheckbox {
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .stCheckbox label {
        color: #cbd5e1 !important;
        font-size: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. Achtergrond Kaart (Volledig scherm, ultramoderne donkere stijl)
m = folium.Map(
    location=[50.8503, 4.3517],  # Centrum België
    zoom_start=11,
    tiles="CartoDB dark_matter",
    zoom_control=False,  # Verberg standaard controls voor een cleane look
    attributionControl=False
)

# Render de kaart fullscreen via st_folium
st_folium(m, use_container_width=True, height=900)

# 2. Zwevend Glassmorphism Bedieningspaneel (Boven de map in de linkerhoek)
with st.container():
    st.markdown("""
    <div class="floating-control-panel">
        <h2>🗺️ Scenic Navigator</h2>
        <p>Ontdek de mooiste routes met een Waze-look</p>
    </div>
    """, unsafe_allow_html=True)

    # Omdat Streamlit widgets direct in de HTML-stream geplaatst moeten worden, 
    # vangen we ze op binnen een nette wrapper onder het paneel.
    # Hier maken we een nette integratie via een kleine st.sidebar of floating structuur.
