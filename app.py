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

# 1. Achtergrond Kaart initialiseren (gecentreerd op Kortrijk/Wevelgem)
m = folium.Map(
    location=[50.8280, 3.2648], 
    zoom_start=12,
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

# 2. Zoekbalk, uitklapmenu met locatie-iconen én centrale route-popup
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
    width: 410px;
  }

  .search-container {
    display: flex;
    align-items: center;
    background: #ffffff;
    width: 100%;
    height: 56px;
    border-radius: 50px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    padding-left: 18px;
  }

  /* Locatie icoon in hoofdzoekbalk (Wit op donker rondje of passend) */
  .search-icon-badge {
    width: 32px;
    height: 32px;
    background-color: #1e293b;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    flex-shrink: 0;
  }

  .search-icon-badge svg {
    width: 16px;
    height: 16px;
    fill: #ffffff;
  }

  .search-input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    padding-right: 12px;
    font-size: 16px;
    color: #1e293b;
    font-weight: 400;
  }

  .search-input::placeholder {
    color: #94a3b8;
    font-weight: 300;
  }

  /* Uitklapknop (pijltje) */
  .expand-btn {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .expand-btn svg {
    width: 18px;
    height: 18px;
    stroke: #64748b;
    stroke-width: 2.5;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
    transition: transform 0.3s ease;
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

  /* Universele Suggesties Dropdown */
  .suggestions-dropdown {
    display: none;
    position: absolute;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    overflow-y: auto;
    z-index: 100000;
    border: 1px solid rgba(0,0,0,0.06);
    max-height: 250px;
    width: 100%;
    box-sizing: border-box;
  }

  .suggestion-item {
    padding: 12px 18px;
    font-size: 14px;
    color: #1e293b;
    cursor: pointer;
    border-bottom: 1px solid #f1f5f9;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    transition: background 0.15s ease;
    text-align: left;
  }

  .suggestion-item:last-child {
    border-bottom: none;
  }

  .suggestion-item:hover {
    background-color: #f8fafc;
  }

  .suggestion-content {
    display: flex;
    align-items: center;
    gap: 10px;
    overflow: hidden;
  }

  .suggestion-item svg {
    width: 16px;
    height: 16px;
    fill: #64748b;
    flex-shrink: 0;
  }

  .distance-badge {
    font-size: 11px;
    color: #64748b;
    background: #f1f5f9;
    padding: 3px 6px;
    border-radius: 6px;
    flex-shrink: 0;
    font-weight: 500;
  }

  /* Uitklapbaar Opties Venster */
  .options-panel {
    display: none;
    background: #ffffff;
    width: 100%;
    margin-top: 10px;
    border-radius: 24px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
    padding: 20px;
    box-sizing: border-box;
    border: 1px solid rgba(0,0,0,0.06);
  }

  .option-group {
    margin-bottom: 14px;
    position: relative;
  }

  .option-group label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .input-with-icon {
    display: flex;
    align-items: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 0 12px;
    height: 44px;
  }

  .input-with-icon:focus-within {
    border-color: #3b82f6;
    background: #ffffff;
  }

  /* Zwart pijltje voor vertrek / Wit pijltje voor bestemming */
  .field-icon {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
    flex-shrink: 0;
  }

  .field-icon.black {
    background-color: #1e293b;
  }
  .field-icon.black svg {
    fill: #ffffff;
    width: 12px;
    height: 12px;
  }

  .field-icon.white {
    background-color: #e2e8f0;
  }
  .field-icon.white svg {
    fill: #1e293b;
    width: 12px;
    height: 12px;
  }

  .option-input {
    width: 100%;
    border: none;
    background: transparent;
    font-size: 14px;
    color: #1e293b;
    outline: none;
  }

  .checkbox-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid #f1f5f9;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: #334155;
    cursor: pointer;
    font-weight: 400;
  }

  .checkbox-label input {
    width: 16px;
    height: 16px;
    accent-color: #1e293b;
    cursor: pointer;
  }

  /* CENTRALE POPUP (MODAL) */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(11, 15, 25, 0.75);
    z-index: 999999;
    backdrop-filter: blur(4px);
    justify-content: center;
    align-items: center;
  }

  .modal-card {
    background: #ffffff;
    width: 360px;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
    box-sizing: border-box;
    animation: modalPop 0.25s ease-out;
  }

  @keyframes modalPop {
    0% { transform: scale(0.9); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
  }

  .modal-title {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .modal-subtitle {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 16px;
  }

  .preference-container {
    display: flex;
    gap: 12px;
    margin-bottom: 18px;
  }

  .pref-option {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 12px;
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #f8fafc;
  }

  .pref-option input {
    display: none;
  }

  .pref-option span {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
    margin-top: 6px;
  }

  .pref-option svg {
    width: 20px;
    height: 20px;
    stroke: #64748b;
    stroke-width: 2;
    fill: none;
  }

  .pref-option.selected {
    border-color: #1e293b;
    background: #f1f5f9;
  }

  .pref-option.selected svg, .pref-option.selected span {
    color: #1e293b;
    stroke: #1e293b;
  }

  .value-input-group {
    margin-bottom: 20px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 12px 16px;
  }

  .value-input-group label {
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: #64748b;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .number-input-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .number-input-wrapper input {
    width: 100%;
    border: none;
    background: transparent;
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
    outline: none;
  }

  .unit-label {
    font-size: 14px;
    font-weight: 600;
    color: #64748b;
    margin-left: 8px;
  }

  .depart-btn {
    width: 100%;
    height: 48px;
    background-color: #1e293b;
    color: #ffffff;
    border: none;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: background-color 0.2s ease, transform 0.1s ease;
  }

  .depart-btn:hover {
    background-color: #0f172a;
  }

  .depart-btn:active {
    transform: scale(0.98);
  }

  .close-modal {
    background: transparent;
    border: none;
    font-size: 20px;
    color: #94a3b8;
    cursor: pointer;
  }
  .close-modal:hover {
    color: #1e293b;
  }
</style>
</head>
<body>

<div class="search-wrapper">
  <!-- Hoofdzoekbalk container met wit locatie-icoon -->
  <div class="search-container" id="mainSearchContainer" style="position: relative;">
    <div class="search-icon-badge">
      <!-- Wit locatiepijltje -->
      <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
    </div>
    <input type="text" id="searchInput" class="search-input" placeholder="Waar wil je naartoe?" autocomplete="off">
    <button class="expand-btn" id="expandBtn" title="Opties weergeven">
      <svg id="arrowIcon" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>
    <button class="search-btn" onclick="openRouteModal()">
      <svg viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
    </button>
  </div>

  <!-- Uitklapbaar venster -->
  <div id="optionsPanel" class="options-panel">
    <!-- Startpunt met ZWART locatiepijltje -->
    <div class="option-group" id="startGroup">
      <label>Vertrekpunt</label>
      <div class="input-with-icon">
        <div class="field-icon black">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <input type="text" id="startInput" class="option-input" value="Locatie ophalen..." autocomplete="off">
      </div>
    </div>
    
    <!-- Bestemming met WIT locatiepijltje -->
    <div class="option-group" id="destGroup">
      <label>Bestemming</label>
      <div class="input-with-icon">
        <div class="field-icon white">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <input type="text" id="destInput" class="option-input" placeholder="Bestemming..." autocomplete="off">
      </div>
    </div>

    <div class="checkbox-group">
      <label class="checkbox-label">
        <input type="checkbox" id="chkLoop" onchange="toggleLoopMode()"> Maak een lus (rondrit)
      </label>
      <label class="checkbox-label">
        <input type="checkbox" id="chkHighways" checked> Autostrades vermijden
      </label>
      <label class="checkbox-label">
        <input type="checkbox" id="chkTolls"> Payages vermijden
      </label>
      <label class="checkbox-label">
        <input type="checkbox" id="chkFerries"> Veerponten vermijden
      </label>
    </div>
  </div>
</div>

<!-- Universeel suggestievenster -->
<div id="suggestions" class="suggestions-dropdown"></div>

<!-- CENTRALE POPUP (MODAL) VOOR ROUTE START -->
<div id="routeModal" class="modal-overlay">
  <div class="modal-card">
    <div class="modal-title">
      Route optimalisatie
      <button class="close-modal" onclick="closeRouteModal()">&times;</button>
    </div>
    <div class="modal-subtitle" id="modalSubtitle">Hoe wil je dat de route berekend wordt?</div>

    <div class="preference-container">
      <label class="pref-option selected" id="optTime" onclick="setPreference('time')">
        <input type="radio" name="pref" value="time" checked>
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <span>Tijd</span>
      </label>
      
      <label class="pref-option" id="optDistance" onclick="setPreference('distance')">
        <input type="radio" name="pref" value="distance">
        <svg viewBox="0 0 24 24"><path d="M18 6L6 18M6 6l12 12"></path></svg>
        <span>Afstand</span>
      </label>
    </div>

    <!-- Dynamische waarde selector -->
    <div class="value-input-group">
      <label id="valueLabel">Gewenste duur</label>
      <div class="number-input-wrapper">
        <input type="number" id="routeValueInput" value="1.0" min="0.25" max="24" step="0.25">
        <span class="unit-label" id="unitLabel">uur</span>
      </div>
    </div>

    <button class="depart-btn" onclick="startNavigation()">Vertrek</button>
  </div>
</div>

<script>
  const input = document.getElementById('searchInput');
  const destInput = document.getElementById('destInput');
  const startInput = document.getElementById('startInput');
  const suggestionsBox = document.getElementById('suggestions');
  const expandBtn = document.getElementById('expandBtn');
  const optionsPanel = document.getElementById('optionsPanel');
  const arrowIcon = document.getElementById('arrowIcon');
  
  const mainSearchContainer = document.getElementById('mainSearchContainer');
  const startGroup = document.getElementById('startGroup');
  const destGroup = document.getElementById('destGroup');
  const routeModal = document.getElementById('routeModal');
  const modalSubtitle = document.getElementById('modalSubtitle');
  
  const routeValueInput = document.getElementById('routeValueInput');
  const valueLabel = document.getElementById('valueLabel');
  const unitLabel = document.getElementById('unitLabel');
  const chkLoop = document.getElementById('chkLoop');

  let timeoutId = null;
  let userLat = 50.8280;
  let userLon = 3.2648;
  let activeTargetInput = null;
  let currentPreference = 'time';

  // Browser geolocatie ophalen
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLat = position.coords.latitude;
        userLon = position.coords.longitude;
        
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${userLat}&lon=${userLon}&addressdetails=1`, {
          headers: { 'Accept-Language': 'nl' }
        })
        .then(response => response.json())
        .then(data => {
          if (data && data.display_name) {
            startInput.value = data.display_name;
          } else {
            startInput.value = `${userLat.toFixed(4)}, ${userLon.toFixed(4)}`;
          }
        })
        .catch(() => {
          startInput.value = `${userLat.toFixed(4)}, ${userLon.toFixed(4)}`;
        });
      },
      (error) => {
        fallbackIpLocation();
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  } else {
    fallbackIpLocation();
  }

  function fallbackIpLocation() {
    fetch('https://ipwho.is/')
      .then(response => response.json())
      .then(data => {
        if (data && data.success) {
          userLat = data.latitude;
          userLon = data.longitude;
          startInput.value = data.city ? `${data.city} (Huidige locatie)` : "Huidige locatie";
        }
      })
      .catch(() => {
        startInput.value = "Kortrijk, België";
      });
  }

  expandBtn.addEventListener('click', () => {
    const isOpen = optionsPanel.style.display === 'block';
    if (isOpen) {
      optionsPanel.style.display = 'none';
      arrowIcon.style.transform = 'rotate(0deg)';
      suggestionsBox.style.display = 'none';
    } else {
      optionsPanel.style.display = 'block';
      arrowIcon.style.transform = 'rotate(180deg)';
    }
  });

  // Schakelt de weergave van het bestemmingsveld uit als een lus gekozen wordt
  function toggleLoopMode() {
    if (chkLoop.checked) {
      destGroup.style.display = 'none';
      destInput.value = '';
    } else {
      destGroup.style.display = 'block';
    }
  }

  function positionDropdown(targetField) {
    let parentWrapper = null;
    if (targetField === input) {
      parentWrapper = mainSearchContainer;
      suggestionsBox.style.top = '62px';
      suggestionsBox.style.left = '0px';
      suggestionsBox.style.width = '100%';
    } else if (targetField === startInput) {
      parentWrapper = startGroup;
      suggestionsBox.style.top = '64px';
      suggestionsBox.style.left = '0px';
      suggestionsBox.style.width = '100%';
    } else if (targetField === destInput) {
      parentWrapper = destGroup;
      suggestionsBox.style.top = '64px';
      suggestionsBox.style.left = '0px';
      suggestionsBox.style.width = '100%';
    }

    if (parentWrapper && suggestionsBox.parentNode !== parentWrapper) {
      parentWrapper.appendChild(suggestionsBox);
    }
  }

  function handleInputTyping(queryField) {
    const query = queryField.value.trim();
    activeTargetInput = queryField;

    if (queryField === input && !chkLoop.checked) {
      destInput.value = input.value;
    } else if (queryField === destInput) {
      input.value = destInput.value;
    }

    if (query.length < 2) {
      suggestionsBox.style.display = 'none';
      return;
    }

    positionDropdown(queryField);

    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      const viewbox = `${userLon - 0.8},${userLat + 0.8},${userLon + 0.8},${userLat - 0.8}`;
      const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&addressdetails=1&limit=10&countrycodes=be&viewbox=${viewbox}&bounded=0`;
      
      fetch(url, { headers: { 'Accept-Language': 'nl' } })
        .then(response => response.json())
        .then(data => {
          if (data && data.length > 0) {
            data.forEach(item => {
              item.distance = calculateDistance(userLat, userLon, parseFloat(item.lat), parseFloat(item.lon));
            });

            data.sort((a, b) => a.distance - b.distance);

            let html = '';
            data.forEach(item => {
              const name = item.display_name.replace(/'/g, "\\'");
              let distText = item.distance < 1 ? Math.round(item.distance * 1000) + ' m' : item.distance.toFixed(1) + ' km';
              
              // Witte locatiepijltje in de suggestielijst per item
              html += `<div class="suggestion-item" onclick="selectSuggestion('${name}')">
                         <div class="suggestion-content">
                           <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                           <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${item.display_name}</span>
                         </div>
                         <span class="distance-badge">${distText}</span>
                       </div>`;
            });
            suggestionsBox.innerHTML = html;
            suggestionsBox.style.display = 'block';
          } else {
            suggestionsBox.style.display = 'none';
          }
        })
        .catch(err => {
          console.error("Fout bij ophalen suggesties:", err);
        });
    }, 250);
  }

  input.addEventListener('input', () => handleInputTyping(input));
  destInput.addEventListener('input', () => handleInputTyping(destInput));
  startInput.addEventListener('input', () => handleInputTyping(startInput));

  function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
      Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.search-wrapper') && !e.target.closest('#routeModal')) {
      suggestionsBox.style.display = 'none';
    }
  });

  input.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      suggestionsBox.style.display = 'none';
      openRouteModal();
    }
  });

  destInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      suggestionsBox.style.display = 'none';
      openRouteModal();
    }
  });

  startInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      suggestionsBox.style.display = 'none';
      openRouteModal();
    }
  });

  function selectSuggestion(val) {
    if (activeTargetInput) {
      activeTargetInput.value = val;
      if (activeTargetInput === input && !chkLoop.checked) {
        input.value = val;
        destInput.value = val;
      }
    }
    suggestionsBox.style.display = 'none';
  }

  function openRouteModal() {
    const isLoop = chkLoop.checked;
    const dest = destInput.value.trim();
    const mainVal = input.value.trim();

    if (!isLoop && dest === '' && mainVal === '') {
      input.focus();
      return;
    }
    
    if (isLoop) {
      modalSubtitle.innerText = "Hoe lang mag de rondrit duren?";
    } else {
      modalSubtitle.innerText = "Hoe wil je dat de route berekend wordt?";
    }

    suggestionsBox.style.display = 'none';
    routeModal.style.display = 'flex';
  }

  function closeRouteModal() {
    routeModal.style.display = 'none';
  }

  function setPreference(pref) {
    currentPreference = pref;
    document.getElementById('optTime').classList.remove('selected');
    document.getElementById('optDistance').classList.remove('selected');

    if (pref === 'time') {
      document.getElementById('optTime').classList.add('selected');
      valueLabel.innerText = "Gewenste duur";
      unitLabel.innerText = "uur";
      routeValueInput.value = "1.0";
      routeValueInput.step = "0.25";
      routeValueInput.min = "0.25";
    } else {
      document.getElementById('optDistance').classList.add('selected');
      valueLabel.innerText = "Gewenste afstand";
      unitLabel.innerText = "km";
      routeValueInput.value = "50";
      routeValueInput.step = "5";
      routeValueInput.min = "1";
    }
  }

  function startNavigation() {
    const start = startInput.value;
    const dest = destInput.value;
    const isLoop = chkLoop.checked;
    const avoidHighways = document.getElementById('chkHighways').checked;
    const avoidTolls = document.getElementById('chkTolls').checked;
    const avoidFerries = document.getElementById('chkFerries').checked;
    const routeAmount = routeValueInput.value;

    console.log("NAVIGATIE GESTART:", {
      start,
      dest: isLoop ? "(Lus / Rondrit)" : dest,
      optimization: currentPreference,
      amount: routeAmount + " " + unitLabel.innerText,
      isLoop,
      avoidHighways,
      avoidTolls,
      avoidFerries
    });

    closeRouteModal();
  }
</script>

</body>
</html>
"""

# Render de component
components.html(search_html, height=520, scrolling=False)
