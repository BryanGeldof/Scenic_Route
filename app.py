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

# Ultra-premium Waze Glassmorphism Styling
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

    /* Zwevend Waze Paneel linksboven (1/3 breedte, exact 24px marges) */
    .waze-glass-panel {
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
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .waze-glass-panel h2 {
        font-size: 19px;
        font-weight: 700;
        margin: 0 0 4px 0;
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .waze-glass-panel p {
        font-size: 12px;
        color: #94a3b8;
        margin: 0 0 16px 0;
    }

    /* Streamlit widgets mooi integreren in het glazen paneel via vaste positionering */
    .element-container {
        position: fixed !important;
        top: 130px !important;
        left: 48px !important;
        z-index: 100000 !important;
        width: 332px !important;
    }

    /* Strakke invoervelden met vergrootglas */
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        padding: 12px 14px 12px 38px !important;
        font-size: 14px !important;
    }

    /* Strakke knop in Waze stijl */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        width: 100% !important;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4) !important;
        cursor: pointer;
        margin-top: 10px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8) !important;
        transform: translateY(-1px);
    }

    .stCheckbox label {
        color: #cbd5e1 !important;
        font-size: 13px !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. Achtergrond Kaart (OpenStreetMap, geen API-key nodig)
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=11,
    tiles="OpenStreetMap",
    zoom_control=False,
    attributionControl=False
)
st_folium(m, use_container_width=True, height=900)

# 2. Het visuele glazen achtergrondpaneel linksboven
st.markdown("""
<div class="waze-glass-panel">
    <h2>🗺️ Scenic Navigator</h2>
    <p>Plan je route of schilderachtige lus</p>
</div>
""", unsafe_allow_html=True)

# 3. De echte interactieve Streamlit elementen erbovenop gepositioneerd
with st.container():
    search_query = st.text_input("Bestemming", placeholder="🔍 Typ bestemming of adres...", label_visibility="collapsed")
    is_loop = st.checkbox("🔄 Maak schilderachtige lus vanaf locatie")
    
    if st.button("Start Route Berekenen 🚀"):
        if is_loop:
            st.success("🔄 Lus-modus geactiveerd!")
        elif search_query:
            st.success(f"🚀 Route gestart naar: **{search_query}**")
        else:
            st.warning("⚠️ Vul een bestemming in of kies een lus.")
