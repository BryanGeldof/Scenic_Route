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

# Strakke Waze Glassmorphism Styling
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

    /* Posysionering van de Streamlit container als één strak paneel linksboven */
    .element-container {
        position: fixed !important;
        top: 24px !important;
        left: 24px !important;
        z-index: 99999 !important;
        width: 360px !important;
    }

    /* Het glazen paneel om de widgets heen */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background: rgba(15, 23, 42, 0.88);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 24px;
        border-radius: 24px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
    }

    /* Strakke invoervelden */
    .stTextInput input {
        background-color: rgba(30, 41, 59, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px 14px 10px 36px !important;
        font-size: 14px !important;
    }

    /* Strakke knop in Waze stijl */
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
        margin-top: 8px;
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

# 1. Achtergrond Kaart (OpenStreetMap)
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=11,
    tiles="OpenStreetMap",
    zoom_control=False,
    attributionControl=False
)
st_folium(m, use_container_width=True, height=900)

# 2. Één geïntegreerd paneel met titel, zoekveld, checkbox en knop
with st.container():
    st.markdown("### 🗺️ Scenic Navigator")
    st.markdown("<p style='font-size: 12px; color: #94a3b8; margin-top: -10px; margin-bottom: 12px;'>Plan je route of schilderachtige lus</p>", unsafe_allow_html=True)
    
    search_query = st.text_input("Bestemming", placeholder="🔍 Typ bestemming of adres...", label_visibility="collapsed")
    is_loop = st.checkbox("🔄 Maak schilderachtige lus vanaf locatie")
    
    if st.button("Start Route Berekenen 🚀"):
        if is_loop:
            st.success("🔄 Lus-modus geactiveerd!")
        elif search_query:
            st.success(f"🚀 Route gestart naar: **{search_query}**")
        else:
            st.warning("⚠️ Vul een bestemming in of kies een lus.")
