import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# Pagina configuratie
st.set_page_config(
    page_title="Scenic Route Navigator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. Achtergrond Kaart initialiseren
m = folium.Map(
    location=[50.8503, 4.3517], 
    zoom_start=11,
    tiles="OpenStreetMap",
    zoom_control=False,
    attributionControl=False
)

# Render de kaart op de achtergrond via een container
with st.container():
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
        
        iframe {
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            z-index: 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st_folium(m, use_container_width=True, height=900)

# 2. Pixel-perfecte Waze/Pil zoekbalk exact zoals je voorbeeld rechtsboven ingespoten via HTML/JS
search_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  .search-container {
    position: fixed;
    top: 24px;
    right: 24px;
    z-index: 99999;
    display: flex;
    align-items: center;
    background: #ffffff;
    width: 360px;
    height: 56px;
    border-radius: 50px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  .search-input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    padding-left: 24px;
    padding-right: 16px;
    font-size: 16px;
    color: #1e293b;
    font-weight: 400;
  }

  .search-input::placeholder {
    color: #94a3b8;
    font-weight: 300;
  }

  .search-btn {
    width: 52px;
    height: 52px;
    background-color: #1e293b;
    border: none;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-right: 2px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, background-color 0.2s ease;
  }

  .search-btn:hover {
    background-color: #0f172a;
    transform: scale(1.05);
  }

  .search-btn svg {
    width: 20px;
    height: 20px;
    stroke: #ffffff;
    stroke-width: 2.2;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
  }
</style>
</head>
<body>

<div class="search-container">
  <input type="text" id="searchInput" class="search-input" placeholder="Search..." autocomplete="off">
  <button class="search-btn" onclick="triggerSearch()">
    <svg viewBox="0 0 24 24">
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
  </button>
</div>

<script>
  const input = document.getElementById('searchInput');
  
  input.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      triggerSearch();
    }
  });

  function triggerSearch() {
    const val = input.value;
    if (val.trim() !== '') {
      // Stuur de data terug naar Streamlit via URL parameters of console event
      window.parent.postMessage({type: 'streamlit:setComponentValue', value: val}, '*');
    }
  }
</script>

</body>
</html>
"""

# Render de component pixel-perfect op het scherm
components.html(search_html, height=80, scrolling=False)
