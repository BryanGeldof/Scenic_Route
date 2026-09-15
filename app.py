import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Pagina configuratie
st.set_page_config(
    page_title="Scenic Route Navigator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Waze-like Dark Theme Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #1f2937;
        color: white;
        border-radius: 10px;
        border: 1px solid #374151;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8 100%);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# Titel
st.title("🗺️ Scenic Route Navigator")
st.write("Plan je ideale schilderachtige route met een moderne navigatie-look.")

# Sidebar voor invoer
with st.sidebar:
    st.header("Navigatie Opties")
    start_loc = st.text_input("Startlocatie", "Gent")
    end_loc = st.text_input("Bestemming", "Brugge")
    tempo = st.slider("Tempo / Snelheid (km/u)", 10, 120, 50)
    is_loop = st.checkbox("Ronde (Lus terug naar start)", value=False)
    
    calculate_btn = st.button("Bereken Route")

# Logica & Variabelen
estimated_km = round(tempo * 0.8, 1)

# Weergave van info (gecorrigeerde f-string)
st.info(f"Geschatte afstand bij dit tempo: **{estimated_km} km**")

# Layout met kolommen
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Route Kaart")
    # Folium kaart renderen
    m = folium.Map(location=[51.0543, 3.7174], zoom_start=11)
    st_folium(m, width="100%", height=400)

with col2:
    st.subheader("Reisdetails")
    route_type_text = 'Ronde (Lus)' if is_loop else 'Van A naar B'
    st.markdown(f"""
    <div style="background-color: #111827; padding: 20px; border-radius: 16px; border: 1px solid #1f2937;">
        <p><b>Start:</b> {start_loc}</p>
        <p><b>Bestemming:</b> {end_loc}</p>
        <p><b>Type Route:</b> {route_type_text}</p>
        <p><b>Gemiddeld Tempo:</b> {tempo} km/u</p>
    </div>
    """, unsafe_allow_html=True)
