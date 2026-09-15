import streamlit as st
import folium
from streamlit_folium import st_folium

# Pagina configuratie op full-width
st.set_page_config(
    page_title="Scenic Route Navigator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ultra-premium Waze / Google Maps Glassmorphism Styling
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
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Kaart vult het volledige scherm */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 0;
    }

    /* Ultra-premium zwevend Waze / Google Maps bedieningspaneel */
    .floating-control-panel {
        position: fixed;
        top: 24px;
        left: 24px;
        z-index: 99999;
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 24px;
        border-radius: 24px;
        width: 380px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.05);
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

    /* Strakke inputvelden */
    .stTextInput>div>div>input {
        background-color: rgba(30, 41, 59, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
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
        transition: all 0.3s ease !important;
        margin-top: 10px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%) !important;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.6) !important;
        transform: translateY(-1px);
    }

    .stCheckbox {
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .stCheckbox label {
        color: #cbd5e1 !important;
        font-size: 13px !important;
    }
    
    /* Zorg dat Streamlit elementen netjes binnen het paneel vallen via absolute positioning */
    .element-container {
        position: relative;
        z-index: 100000;
    }
</style>
""", unsafe_allow_html=True)

# 1. Achtergrond Kaart (Gebruik Stamen / OpenStreetMap alternatief dat géén API-key vereist)
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=11,
    tiles="OpenStreetMap", # Altijd gratis en werkt direct zonder watermerken
    zoom_control=False,
    attributionControl=False
)

# Render de kaart fullscreen
st_folium(m, use_container_width=True, height=900)

# 2. Het vaste, zwevende Waze glassmorphism paneel met daarin direct de invoer
st.markdown("""
<div class="floating-control-panel">
    <h2>🗺️ Scenic Navigator</h2>
    <p>Ontdek de mooiste routes met een Waze-look</p>
</div>
""", unsafe_allow_html=True)

# We creëren een kleine tijdelijke container om de widgets visueel in het paneel te plaatsen
# Door de unieke styling vallen ze direct onder de titel in het glazen vlak.
col_dummy, _ = st.columns([1, 3]) # Kleine hack om de breedte te beperken tot het paneel

with st.container():
    # Om te zorgen dat ze exact over het paneel vallen injecteren we ze via een strakke wrapper
    st.markdown('<div style="position: fixed; top: 115px; left: 40px; z-index: 100000; width: 340px;">', unsafe_allow_html=True)
    
    search_query = st.text_input("Waarheen?", placeholder="Typ bestemming of adres...", label_visibility="collapsed")
    is_loop = st.checkbox("🔄 Maak schilderachtige lus vanaf huidige locatie")
    
    if st.button("Start Navigatie"):
        if is_loop:
            st.success("🔄 Lus-modus ingeschakeld!")
        elif search_query:
            st.success(f"🚀 Koers gezet naar: {search_query}")
        else:
            st.warning("⚠️ Voer een bestemming in.")
            
    st.markdown('</div>', unsafe_allow_html=True)
