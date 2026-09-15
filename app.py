import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Pagina configuratie op full-width (wide)
st.set_page_config(
    page_title="Waze Scenic Navigator",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Waze-style Dark Theme & Floating Glassmorphism Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    
    /* Verberg standaard Streamlit branding voor een cleane app-look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Waze-style linker paneel (Zwevend element look) */
    [data-testid="stSidebar"] {
        background-color: rgba(17, 24, 39, 0.92);
        backdrop-filter: blur(12px);
        border-right: 1px solid #1f2937;
        padding-top: 10px;
    }
    
    /* Strakke zoekbalk */
    .stTextInput>div>div>input {
        background-color: #1f2937;
        color: white;
        border-radius: 14px;
        border: 1px solid #374151;
        padding: 12px 16px;
        font-size: 15px;
    }
    
    /* Waze 'Rijden maar' knop (Neon blauw/cyaan gradient) */
    .stButton>button {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 14px 20px;
        font-weight: 700;
        font-size: 16px;
        width: 100%;
        box-shadow: 0 4px 20px rgba(0, 210, 255, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3ae8ff 0%, #2563eb 100%);
        box-shadow: 0 6px 25px rgba(0, 210, 255, 0.6);
        transform: translateY(-2px);
    }
    
    /* Zorg dat de kaart maximaal gebruik maakt van de ruimte */
    iframe {
        border-radius: 16px;
        border: 1px solid #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# Linkerbovenhoek / Sidebar als Waze Navigatie Paneel
with st.sidebar:
    st.markdown("### 🚗 Waze Scenic Navigator")
    st.write("Plan je route of genereer een ontspannende lus.")
    
    # Locatie zoekveld
    search_query = st.text_input("🔍 Waarheen?", placeholder="Typ bestemming of adres...")
    
    # Checkbox voor lus op basis van huidige locatie
    is_loop = st.checkbox("🔄 Maak een schilderachtige lus vanaf huidige locatie", value=False)
    
    # Navigatieknop
    nav_button = st.button("Start Navigatie")
    
    if nav_button:
        if is_loop:
        # Code voor lus genereren
            st.success("🔄 Lus-modus geactiveerd vanaf je huidige locatie!")
        elif search_query:
            st.success(f"🚀 Koers gezet naar: **{search_query}**")
        else:
            st.warning("⚠️ Voer een bestemming in of selecteer de lus-optie.")

# Hoofdscherm: Volledige kaart in Waze Dark Mode stijl
# We gebruiken CartoDB dark_matter voor die echte hippe navigatie-uitstraling
m = folium.Map(
    location=[51.0543, 3.7174], 
    zoom_start=13,
    tiles="CartoDB dark_matter"
)

# Render de kaart over vrijwel het hele scherm
st_folium(m, use_container_width=True, height=780)
