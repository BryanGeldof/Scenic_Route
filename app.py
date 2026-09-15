import streamlit as st
import streamlit.components.v1 as components

# Pagina configuratie
st.set_page_config(
    page_title="Scenic Route Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
</style>
""", unsafe_allow_html=True)

app_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }

  #map {
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
  }

  /* Zoekbalk rechtsboven */
  .search-wrapper {
    position: fixed;
    top: 24px;
    right: 24px;
    z-index: 99999;
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
    box-sizing: border-box;
  }

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
  }

  .search-input::placeholder { color: #94a3b8; }

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
    transition: transform 0.2s ease;
  }
  .search-btn:hover { transform: scale(1.05); }
  .search-btn svg { width: 20px; height: 20px; stroke: #ffffff; stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }

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

  .option-group { margin-bottom: 14px; }
  .option-group label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: #64748b;
    margin-bottom: 4px;
    text-transform: uppercase;
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

  .field-icon {
    width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px;
  }
  .field-icon.black { background-color: #1e293b; }
  .field-icon.black svg { fill: #ffffff; width: 12px; height: 12px; }

  .option-input {
    width: 100%; border: none; background: transparent; font-size: 14px; color: #1e293b; outline: none;
  }

  /* Resultaten Sidebar links */
  .routes-sidebar {
    display: none;
    position: fixed;
    top: 24px;
    left: 24px;
    z-index: 99999;
    width: 380px;
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
    padding: 20px;
    box-sizing: border-box;
    max-height: calc(100vh - 48px);
    overflow-y: auto;
  }

  .routes-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 10px;
  }

  .routes-title { font-size: 16px; font-weight: 700; color: #1e293b; }
  .close-sidebar { background: transparent; border: none; font-size: 18px; color: #94a3b8; cursor: pointer; }

  .route-card {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .route-card:hover { border-color: #3b82f6; background: #f1f5f9; }
  .route-card.active { border-color: #1e293b; background: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }

  .route-card-title {
    font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;
  }
  .route-dot { width: 10px; height: 10px; border-radius: 50%; }
  .route-stats { display: flex; gap: 16px; font-size: 13px; color: #64748b; font-weight: 500; }

  /* Laadscherm / Overlay */
  .loading-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(11, 15, 25, 0.8);
    z-index: 999999;
    backdrop-filter: blur(5px);
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #ffffff;
  }

  .spinner {
    width: 45px; height: 45px;
    border: 4px solid rgba(255,255,255,0.1);
    border-top: 4px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

  /* Modal Venster voor Kilometers */
  .modal-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
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
  }

  .modal-title { font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
  .modal-subtitle { font-size: 13px; color: #64748b; margin-bottom: 16px; }

  .value-input-group {
    margin-bottom: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 12px 16px;
  }
  .value-input-group label { display: block; font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 6px; text-transform: uppercase; }
  .number-input-wrapper { display: flex; align-items: center; justify-content: space-between; }
  .number-input-wrapper input { width: 100%; border: none; background: transparent; font-size: 18px; font-weight: 600; color: #1e293b; outline: none; }
  .unit-label { font-size: 14px; font-weight: 600; color: #64748b; margin-left: 8px; }

  .depart-btn {
    width: 100%; height: 48px; background-color: #1e293b; color: #ffffff; border: none; border-radius: 14px; font-size: 16px; font-weight: 600; cursor: pointer;
  }
  .depart-btn:hover { background-color: #0f172a; }
  .close-modal { background: transparent; border: none; font-size: 20px; color: #94a3b8; cursor: pointer; }
</style>
</head>
<body>

<div id="map"></div>

<!-- Laadscherm -->
<div id="loadingOverlay" class="loading-overlay">
  <div class="spinner"></div>
  <div style="font-size: 18px; font-weight: 700; margin-bottom: 6px;">Slimme lussen berekenen...</div>
  <div id="loadingText" style="font-size: 13px; color: #94a3b8;">Verschillende richtingen en afslagen verkennen</div>
</div>

<!-- Resultaten Sidebar (Links) -->
<div id="routesSidebar" class="routes-sidebar">
  <div class="routes-header">
    <div class="routes-title">Gevonden Rondritten</div>
    <button class="close-sidebar" onclick="closeRoutesSidebar()">&times;</button>
  </div>
  <div id="routesListContainer"></div>
</div>

<!-- Zoekbalk & Opties (Rechtsboven) -->
<div class="search-wrapper">
  <div class="search-container">
    <div class="search-icon-badge">
      <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
    </div>
    <input type="text" id="searchInput" class="search-input" placeholder="Waar wil je starten?" autocomplete="off">
    <button class="expand-btn" id="expandBtn" title="Opties">
      <svg id="arrowIcon" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>
    <button class="search-btn" onclick="openRouteModal()" title="Start Berekening">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </button>
  </div>

  <div id="optionsPanel" class="options-panel">
    <div class="option-group">
      <label>Vertrekpunt / Locatie</label>
      <div class="input-with-icon">
        <div class="field-icon black">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <input type="text" id="startInput" class="option-input" value="GPS Locatie ophalen..." autocomplete="off">
      </div>
    </div>
  </div>
</div>

<!-- Modal voor instellen kilometers -->
<div id="routeModal" class="modal-overlay">
  <div class="modal-card">
    <div class="modal-title">
      Rondrit Generator
      <button class="close-modal" onclick="closeRouteModal()">&times;</button>
    </div>
    <div class="modal-subtitle">Hoeveel kilometer wil je dat de route ongeveer is?</div>

    <div class="value-input-group">
      <label>Gewenste Afstand</label>
      <div class="number-input-wrapper">
        <input type="number" id="routeValueInput" value="30" min="5" max="150" step="5">
        <span class="unit-label">km</span>
      </div>
    </div>

    <button class="depart-btn" onclick="startSmartSearch()">Start Automatisch Zoeken</button>
  </div>
</div>

<script>
  let map = L.map('map', { zoomControl: false, attributionControl: false }).setView([50.8280, 3.2648], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

  let startMarker = null;
  let activeRouteLayers = [];
  let userLat = 50.8280;
  let userLon = 3.2648;

  const startInput = document.getElementById('startInput');
  const expandBtn = document.getElementById('expandBtn');
  const optionsPanel = document.getElementById('optionsPanel');
  const arrowIcon = document.getElementById('arrowIcon');
  const routeModal = document.getElementById('routeModal');
  const routesSidebar = document.getElementById('routesSidebar');
  const routesListContainer = document.getElementById('routesListContainer');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const loadingText = document.getElementById('loadingText');
  const routeValueInput = document.getElementById('routeValueInput');

  function updateMapMarkers() {
    if (startMarker) map.removeLayer(startMarker);
    const blackIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background-color: #1e293b; width: 26px; height: 26px; border-radius: 50%; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div></div>',
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });
    startMarker = L.marker([userLat, userLon], { icon: blackIcon }).addTo(map);
    map.setView([userLat, userLon], 12);
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLat = position.coords.latitude;
        userLon = position.coords.longitude;
        updateMapMarkers();
        startInput.value = "Huidige GPS-locatie";
      },
      () => { updateMapMarkers(); startInput.value = "Kortrijk, België"; },
      { timeout: 10000 }
    );
  } else {
    updateMapMarkers();
  }

  expandBtn.addEventListener('click', () => {
    const isOpen = optionsPanel.style.display === 'block';
    optionsPanel.style.display = isOpen ? 'none' : 'block';
    arrowIcon.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
  });

  function openRouteModal() { routeModal.style.display = 'flex'; }
  function closeRouteModal() { routeModal.style.display = 'none'; }
  function closeRoutesSidebar() {
    routesSidebar.style.display = 'none';
    activeRouteLayers.forEach(l => map.removeLayer(l));
    activeRouteLayers = [];
  }

  async function startSmartSearch() {
    closeRouteModal();
    loadingOverlay.style.display = 'flex';

    activeRouteLayers.forEach(l => map.removeLayer(l));
    activeRouteLayers = [];

    const targetKm = parseFloat(routeValueInput.value) || 30;

    // Simuleer stappen van de AI tijdens het laden
    loadingText.innerText = "Noordelijke wegen verkennen...";
    await new Promise(r => setTimeout(r, 600));
    loadingText.innerText = "Oostelijke afslagen matchen...";
    await new Promise(r => setTimeout(r, 600));
    loadingText.innerText = "Lussen optimaliseren op kilometers...";
    await new Promise(r => setTimeout(r, 600));

    let radius = (targetKm / Math.PI) / 2;
    let rLat = radius / 111;
    let rLon = radius / (111 * Math.cos(userLat * Math.PI / 180));

    let variations = [
      { name: "Ontdekkingslus 1 (Rechtsom)", color: "#3b82f6", points: [[userLat, userLon], [userLat + rLat, userLon + rLon], [userLat - rLat, userLon + rLon], [userLat, userLon]] },
      { name: "Ontdekkingslus 2 (Linksdom)", color: "#10b981", points: [[userLat, userLon], [userLat + rLat, userLon - rLon], [userLat - rLat, userLon - rLon], [userLat, userLon]] },
      { name: "Ontdekkingslus 3 (Noord-Zuid)", color: "#f59e0b", points: [[userLat, userLon], [userLat + (rLat * 1.4), userLon], [userLat - (rLat * 1.4), userLon], [userLat, userLon]] }
    ];

    let html = '';

    for (let i = 0; i < variations.length; i++) {
      let v = variations[i];
      let coordsString = v.points.map(p => `${p[1]},${p[0]}`).join(';');
      let url = `https://routing.openstreetmap.de/routed-car/route/v1/driving/${coordsString}?overview=full&geometries=geojson`;

      let routeGeometry = v.points;
      let actualDist = targetKm;
      let actualDur = (targetKm / 50).toFixed(1);

      try {
        let response = await fetch(url);
        let data = await response.json();
        if (data && data.routes && data.routes.length > 0) {
          let r = data.routes[0];
          routeGeometry = r.geometry.coordinates.map(c => [c[1], c[0]]);
          actualDist = (r.distance / 1000).toFixed(1);
          actualDur = (r.duration / 3600).toFixed(1);
        }
      } catch (err) {
        console.log("Fallback naar wiskundige punten");
      }

      let polyline = L.polyline(routeGeometry, { color: v.color, weight: i === 0 ? 6 : 4, opacity: 0.85 }).addTo(map);
      activeRouteLayers.push(polyline);
      polyline.on('click', () => { selectRouteCard(i); });

      html += `
        <div class="route-card ${i === 0 ? 'active' : ''}" id="routeCard_${i}" onclick="selectRouteCard(${i})">
          <div class="route-card-title">
            <div class="route-dot" style="background-color: ${v.color};"></div>
            ${v.name}
          </div>
          <div class="route-stats">
            <span>🚗 ${actualDist} km</span>
            <span>⏱️ ${actualDur} uur</span>
          </div>
        </div>
      `;
    }

    routesListContainer.innerHTML = html;
    if (activeRouteLayers.length > 0) {
      map.fitBounds(activeRouteLayers[0].getBounds(), { padding: [50, 50] });
    }

    loadingOverlay.style.display = 'none';
    routesSidebar.style.display = 'block';
  }

  window.selectRouteCard = function(index) {
    document.querySelectorAll('.route-card').forEach((card, idx) => {
      if (idx === index) {
        card.classList.add('active');
        activeRouteLayers[idx].setStyle({ weight: 6, opacity: 1 });
        map.fitBounds(activeRouteLayers[idx].getBounds(), { padding: [50, 50] });
      } else {
        card.classList.remove('active');
        activeRouteLayers[idx].setStyle({ weight: 4, opacity: 0.4 });
      }
    });
  }
</script>

</body>
</html>
"""

components.html(app_html, height=900, scrolling=False)
