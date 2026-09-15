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

# 2. Zoekbalk met volledige autocomplete voor álle letters en ruime weergave
search_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  .search-wrapper {
    position: fixed;
    top: 24px;
    right: 24px;
    z-index: 99999;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  .search-container {
    display: flex;
    align-items: center;
    background: #ffffff;
    width: 380px;
    height: 56px;
    border-radius: 50px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
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

  /* Ruime suggesties Dropdown met scrollfunctie */
  .suggestions-dropdown {
    display: none;
    position: absolute;
    top: 64px;
    left: 14px;
    width: 310px;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    overflow-y: auto;
    z-index: 100000;
    border: 1px solid rgba(0,0,0,0.06);
    max-height: 260px;
  }

  .suggestion-item {
    padding: 12px 18px;
    font-size: 14px;
    color: #1e293b;
    cursor: pointer;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: background 0.15s ease;
  }

  .suggestion-item:last-child {
    border-bottom: none;
  }

  .suggestion-item:hover {
    background-color: #f8fafc;
  }

  .suggestion-item svg {
    width: 16px;
    height: 16px;
    stroke: #64748b;
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
    flex-shrink: 0;
  }
</style>
</head>
<body>

<div class="search-wrapper">
  <div class="search-container">
    <input type="text" id="searchInput" class="search-input" placeholder="Zoek bestemming..." autocomplete="off">
    <button class="search-btn" onclick="triggerSearch()">
      <svg viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
    </button>
  </div>
  <div id="suggestions" class="suggestions-dropdown"></div>
</div>

<script>
  // Uitgebreide lijst met locaties
  const mockLocations = [
    "Brussel, Centrum",
    "Brussel-Zuid Station",
    "Antwerpen Centraal Station",
    "Antwerpen, Grote Markt",
    "Gent, Korenmarkt",
    "Gent-Sint-Pieters",
    "Brugge, Grote Markt",
    "Leuven, Oude Markt",
    "Leuven Station",
    "Oostende, Zeedijk",
    "Mechelen, Sint-Romboutstoren",
    "Hasselt, Demerstraat",
    "Kortrijk, Broeltorens",
    "Teststraat 1, 1111 Brussel",
    "Waterloo, Leeuw van Waterloo",
    "Blankenberge, Pier",
    "Knokke-Heist, Kustlaan"
  ];

  const input = document.getElementById('searchInput');
  const suggestionsBox = document.getElementById('suggestions');

  // Dynamische filtering voor elke letter die getyped wordt
  input.addEventListener('input', function() {
    const query = input.value.trim().toLowerCase();
    
    if (query.length === 0) {
      suggestionsBox.style.display = 'none';
      return;
    }

    // Filter doorlopend op basis van de ingevoerde tekst
    const filtered = mockLocations.filter(loc => loc.toLowerCase().includes(query));
    
    if (filtered.length > 0) {
      let html = '';
      filtered.forEach(loc => {
        html += `<div class="suggestion-item" onclick="selectSuggestion('${loc}')">
                   <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                   ${loc}
                 </div>`;
      });
      suggestionsBox.innerHTML = html;
      suggestionsBox.style.display = 'block';
    } else {
      suggestionsBox.style.display = 'none';
    }
  });

  // Klik buiten de zoekbalk sluit de suggesties
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.search-wrapper')) {
      suggestionsBox.style.display = 'none';
    }
  });

  // Enter toets indrukken
  input.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      suggestionsBox.style.display = 'none';
      triggerSearch();
    }
  });

  function selectSuggestion(val) {
    input.value = val;
    suggestionsBox.style.display = 'none';
    triggerSearch();
  }

  function triggerSearch() {
    const val = input.value;
    if (val.trim() !== '') {
      console.log("Zoeken naar:", val);
    }
  }
</script>

</body>
</html>
"""

# Belangrijk: height=350 zorgt ervoor dat de dropdown nooit meer wordt afgekapt!
components.html(search_html, height=350, scrolling=False)
