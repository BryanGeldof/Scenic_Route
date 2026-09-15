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

# Geavanceerde CSS om alle Streamlit marges te verwijderen en de kaart 100vh te maken
st.markdown("""
<style>
    /* Verberg standaard Streamlit elementen en marges */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0b0f19;
        overflow: hidden;
    }
    
    /* Maak de hoofdcontainer volledig scherm */
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
    }
    
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 0;
    }

    /* Zwevend Waze-stijl zoekpaneel linksboven */
    .floating-search-box {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 99999;
        background: rgba(17, 24, 39, 0.90);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px;
        border-radius: 16px;
        width: 360px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .floating-search-box input {
        background-color: #1f2937 !important;
        color: white !important;
        border: 1px solid #374151 !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Achtergrondkaart vult het hele scherm (CartoDB dark_matter voor die strakke navigatie-look)
m = folium.Map(
    location=[51.0543, 3.7174], 
    zoom_start=14,
    tiles="CartoDB dark_matter"
)

# Render de kaart op full screen
st_folium(m, use_container_width=True, height=850)

# Zwevend Waze-menu bovenop de kaart in de linkerbovenhoek
st.markdown("""
<div class="floating-search-box">
    <h3 style="color: white; margin-top: 0; font-size: 18px; font-weight: 700;">🚗 Scenic Navigator</h3>
</div>
""", unsafe_allow_html=True)

# Interactieve elementen via een kleine sidebar of extra overlay overlay-besturing indien gewenst
with st.sidebar:
    st.write("Instellingen & Zoekopdracht")
    search_query = st.text_input("Bestemming", placeholder="Waarheen?")
    is_loop = st.checkbox("🔄 Maak een lus vanaf huidige locatie")
    if st.button("Start Navigatie"):
        st.success("Route berekend!")
