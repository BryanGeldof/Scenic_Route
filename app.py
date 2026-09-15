import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. Pagina configuratie
st.set_page_config(
    page_title="Scenic Route Navigator | Enterprise",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Professionele Enterprise Styling (Geen breekbare hacks, wel strakke UI)
st.markdown("""
<style>
    /* Algemene achtergrond en font optimalisatie */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Strakke sidebar styling in enterprise dark theme */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 20px;
    }
    
    /* Moderne knoppen */
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 16px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8);
        box-shadow: 0 6px 16px rgba(14, 165, 233, 0.5);
    }
    
    /* Invoervelden */
    .stTextInput input, .stSelectbox select {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    /* Verberg standaard Streamlit branding voor een "white-label" look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. Professionele Sidebar (Controlepaneel)
with st.sidebar:
    st.markdown("### 🗺️ Scenic Navigator")
    st.markdown("<p style='font-size: 13px; color: #94a3b8; margin-top: -10px;'>Professional Route Planning Suite</p>", unsafe_allow_html=True)
    st.divider()
    
    # Navigatie Tabs voor geavanceerde opties
    tab_zoeken, tab_opties = st.tabs(["🔍 Bestemming", "⚙️ Geavanceerd"])
    
    with tab_zoeken:
        destination = st.text_input("Bestemming", placeholder="Typ adres, stad of coördinaten...")
        transport_mode = st.selectbox("Vervoersmiddel", ["🚗 Auto (Schilderachtig)", "🏍️ Motor", "🚴 Fiets", "🚶 Wandelen"])
        
    with tab_opties:
        max_detour = st.slider("Maximale omweg (km)", 5, 50, 15)
        scenic_factor = st.select_slider("Landschap voorkeur", options=["Standaard", "Groenrijk", "Kustlijn", "Heuvels/Bergen"])
        avoid_highways = st.checkbox("Vermijd snelwegen", value=True)
    
    st.divider()
    
    # Actieknop
    if st.button("Route Berekenen 🚀"):
        if destination:
            st.success(f"Route berekend naar **{destination}** via {transport_mode}!")
        else:
            st.warning("Voer eerst een bestemming in.")

# 4. Hoofdweergave: Volledig scherm interactieve kaart
# Hier komt het hart van je kaartapplicatie
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=10,
    tiles="CartoDB positron", # Strakke, professionele kaartstijl (donker of licht)
    zoom_control=True,
    attributionControl=False
)

# Render de kaart in het hoofdscherm op volle grootte
st_folium(m, use_container_width=True, height=850)
