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

# Ultra-premium Waze / Google Maps stijlen en HTML/JS logica in één strak paneel
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
    
    /* Kaart vult het volledige scherm achter de overlay */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 0;
    }

    /* Het hoofd Waze glassmorphism paneel linksboven (gelijke spacing van 24px) */
    .waze-control-card {
        position: fixed;
        top: 24px;
        left: 24px;
        z-index: 99999;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 24px;
        border-radius: 24px;
        width: 380px; /* Ongeveer 1/3 schermbreedte voor comfortabele navigatie */
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7);
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .waze-control-card h2 {
        font-size: 19px;
        font-weight: 700;
        margin: 0 0 4px 0;
        background: linear-gradient(135deg, #38bdf8 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .waze-control-card p {
        font-size: 12px;
        color: #94a3b8;
        margin: 0 0 16px 0;
    }

    /* Zoekbalk met vergrootglas en autofill dropdown */
    .search-box-wrapper {
        position: relative;
        margin-bottom: 12px;
    }

    .search-input {
        width: 100%;
        background-color: rgba(30, 41, 59, 0.95) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        padding: 12px 14px 12px 40px !important;
        font-size: 14px !important;
        outline: none;
        box-sizing: border-box;
    }

    .search-input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
    }

    .search-icon {
        position: absolute;
        left: 14px;
        top: 14px;
        font-size: 14px;
        pointer-events: none;
        filter: grayscale(1);
    }

    /* Autofill suggestie-lijst */
    .suggestions-list {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        margin-top: 6px;
        max-height: 200px;
        overflow-y: auto;
        z-index: 100000;
        display: none;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }

    .suggestion-item {
        padding: 10px 14px;
        font-size: 13px;
        color: #e2e8f0;
        cursor: pointer;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .suggestion-item:hover {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
    }

    /* Opties en knoppen */
    .options-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;
        font-size: 13px;
        color: #cbd5e1;
        cursor: pointer;
    }

    .nav-button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb);
        color: white;
        border-radius: 14px;
        border: none;
        padding: 12px 20px;
        font-weight: 600;
        font-size: 14px;
        width: 100%;
        cursor: pointer;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
        transition: all 0.3s ease;
    }

    .nav-button:hover {
        background: linear-gradient(135deg, #38bdf8 0%, #1d4ed8);
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.6);
    }
</style>

<!-- Volledig geïntegreerd Waze Paneel met Autofill Logica -->
<div class="waze-control-card">
    <h2>🗺️ Scenic Navigator</h2>
    <p>Ontdek schilderachtige routes met live navigatie</p>
    
    <div class="search-box-wrapper">
        <span class="search-icon">🔍</span>
        <input type="text" id="destinationInput" class="search-input" placeholder="Typ adres of plaats..." autocomplete="off">
        <div id="suggestionsBox" class="suggestions-list"></div>
    </div>

    <label class="options-row">
        <input type="checkbox" id="loopCheckbox" style="accent-color: #0ea5e9; width: 16px; height: 16px;">
        <span>🔄 Maak schilderachtige lus vanaf locatie</span>
    </label>

    <button class="nav-button" onclick="startNavigation()">Start Route Berekenen 🚀</button>
</div>

<script>
    const input = document.getElementById('destinationInput');
    const suggestionsBox = document.getElementById('suggestionsBox');
    let selectedAddress = "";

    // Live OpenStreetMap Nominatim Autofill
    input.addEventListener('input', function() {
        const query = this.value;
        if (query.length < 3) {
            suggestionsBox.style.display = 'none';
            return;
        }

        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = '';
                if (data.length > 0) {
                    suggestionsBox.style.display = 'block';
                    data.forEach(item => {
                        const div = document.createElement('div');
                        div.className = 'suggestion-item';
                        div.innerText = item.display_name;
                        div.onclick = function() {
                            input.value = item.display_name;
                            selectedAddress = item.display_name;
                            suggestionsBox.style.display = 'none';
                        };
                        suggestionsBox.appendChild(div);
                    });
                } else {
                    suggestionsBox.style.display = 'none';
                }
            })
            .catch(err => console.error(err));
    });

    // Verberg suggesties als je ergens anders klikt
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-box-wrapper')) {
            suggestionsBox.style.display = 'none';
        }
    });

    // Direct starten bij enter of knopklik
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            startNavigation();
        }
    });

    function startNavigation() {
        const address = input.value;
        const isLoop = document.getElementById('loopCheckbox').checked;
        
        if (!address && !isLoop) {
            alert('Vul een bestemming in of kies voor een lus.');
            return;
        }
        
        // Stuur actie door naar Streamlit via URL parameters of console melding
        console.log("Navigatie gestart naar: " + address + " | Lus: " + isLoop);
        alert("🚀 Route wordt berekend voor: " + (isLoop ? "Schilderachtige Lus" : address));
    }
</script>
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
