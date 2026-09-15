import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import math

# Page Configuration
st.set_page_config(
    page_title="ScenicRoute | De Mooiste Route App",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        background-color: #0d9488;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0f766e;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("🌿 ScenicRoute: De Mooiste Route Generator")
st.markdown("Ontdek geen saaie snelste wegen, maar geniet van de mooiste landschappen, parken en bezienswaardigheden op maat.")

# Sidebar for User Inputs
with st.sidebar:
    st.header("⚙️ Route Instellingen")
    
    # 1. Transport Mode
    transport_mode = st.selectbox(
        "Kies Vervoersmiddel",
        ["Wandelen 🚶", "Fietsen 🚴", "Auto / Motor 🚗"],
        index=1
    )
    
    # 2. Distance or Time limit
    metric_type = st.radio("Doel op basis van:", ["Afstand (km)", "Tijd (minuten)"])
    
    if metric_type == "Afstand (km)":
        target_value = st.slider("Gewenste afstand (km)", min_value=1, max_value=50, value=10)
        estimated_km = target_value
    else:
        target_time = st.slider("Gewenste tijd (minuten)", min_value=15, max_value=240, value=45)
        # Estimation based on transport mode average speeds
        speeds = {"Wandelen 🚶": 4.5, "Fietsen 🚴": 15.0, "Auto / Motor 🚗": 50.0}
        speed = speeds[transport_mode]
        estimated_km = round((target_time / 60) * speed, 1)
        st.info( geschatte afstand bij dit tempo: **{estimated_km} km**)

    # 3. Loop or A-to-B
    route_type = st.radio("Route Type", ["Ronde (Start = Eindpunt)", "Van A naar B (Enkele reis)"])
    is_loop = (route_type == "Ronde (Start = Eindpunt)")

    # 4. Scenic Preference
    scenic_focus = st.multiselect(
        "Voorkeur voor onderweg",
        ["Groen / Natuur 🌳", "Water / Rivieren / Meren 💧", "Rustige wegen / Weinig verkeer 🚲", "Cultuur / Historie 🏰"],
        default=["Groen / Natuur 🌳", "Water / Rivieren / Meren 💧"]
    )

    generate_btn = st.button("🚀 Bereken Mooiste Route", use_container_width=True)

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Interactieve Kaart")
    
    # Default starting point (e.g., Utrecht / Amsterdam or central default)
    # Let's create a dummy interactive map centered around a nice default location (e.g., Utrecht, NL)
    default_lat, default_lon = 52.0907, 5.1214
    
    m = folium.Map(location=[default_lat, default_lon], zoom_start=13, tiles="CartoDB positron")
    
    # If button clicked, generate synthetic scenic route points for demonstration
    if generate_btn:
        st.success(f"Route succesvol gegenereerd! Ongeveer **{estimated_km} km** lang.")
        
        # Generate dummy loop or path coordinates around default location
        points = []
        num_points = 10
        radius = (estimated_km / 2) / 111.0 # rough conversion km to lat degrees
        
        if is_loop:
            for i in range(num_points + 1):
                angle = 2 * math.pi * i / num_points
                # Add slight random wobble for scenic feel
                r_offset = radius * (0.8 + 0.4 * random.random())
                lat = default_lat + r_offset * math.sin(angle)
                lon = default_lon + (r_offset * math.cos(angle)) / math.cos(math.radians(default_lat))
                points.append([lat, lon])
            
            # Add markers
            folium.Marker([default_lat, default_lon], tooltip="Start- & Eindpunt", icon=folium.Icon(color="green", icon="play")).add_to(m)
            folium.PolyLine(points, color="#0d9488", weight=5, opacity=0.8, tooltip="Mooiste Route").add_to(m)
            
            # Add some scenic highlights along the way
            folium.Marker([points[3][0], points[3][1]], tooltip="Mooi uitzichtpunt 🌳", icon=folium.Icon(color="orange", icon="eye")).add_to(m)
            folium.Marker([points[7][0], points[7][1]], tooltip="Rustig natuurpad 💧", icon=folium.Icon(color="blue", icon="tint")).add_to(m)
            
        else:
            # A to B route
            lat_end = default_lat + radius * 1.5
            lon_end = default_lon + radius * 1.0
            points = [
                [default_lat, default_lon],
                [default_lat + radius*0.5, default_lon + radius*0.3],
                [default_lat + radius*1.0, default_lon - radius*0.2],
                [lat_end, lon_end]
            ]
            folium.Marker([default_lat, default_lon], tooltip="Startpunt", icon=folium.Icon(color="green", icon="play")).add_to(m)
            folium.Marker([lat_end, lon_end], tooltip="Eindpunt", icon=folium.Icon(color="red", icon="stop")).add_to(m)
            folium.PolyLine(points, color="#0d9488", weight=5, opacity=0.8, tooltip="Mooiste Route (A-B)").add_to(m)
            
        m.fit_bounds(points)

    st_data = st_folium(m, width="100%", height=500)

with col2:
    st.subheader("📊 Route Statistieken")
    if generate_btn:
        st.markdown(f"""
        <div class="card">
            <p><b>Geschatte Afstand:</b> {estimated_km} km</p>
            <p><b>Type Route:</b> {'Ronde (Lus)' if is_loop / else 'Van A naar B'}</p>
            <p><b>Vervoer:</b> {transport_mode}</p>
            <p><b>Hoogtemeters:</b> ca. +45m / -45m</p>
            <p><b>Geschatte Duur:</b> {round(estimated_km / (15 if 'Fietsen' in transport_mode else (4.5 if 'Wandelen' in transport_mode else 50)) * 60)} minuten</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🌸 Hoogtepunten onderweg")
        st.markdown("- 🌳 **Boswachterij Pad**: 1.2km door schaduwrijk bos")
        st.markdown("- 💧 **Rivieroever**: 2.5km langs rustig water")
        st.markdown("- ☕ **Koffiestop**: Rustige boerderijterras op 60% van de route")
    else:
        st.info("Stel je voorkeuren in via het menu aan de linkerkant en klik op **Bereken Mooiste Route** om te beginnen!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Gemaakt met ❤️ voor wandelaars, fietsers en toeristen. Eenvoudig en gebruiksvriendelijk.</p>", unsafe_allow_html=True)
