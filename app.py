import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Scenic Route Navigator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #0b0f19; overflow: hidden; margin: 0; padding: 0; }
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; height: 100vh !important; overflow: hidden !important; }
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
  body, html { margin: 0; padding: 0; width: 100%; height: 100vh; overflow: hidden; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  #map { width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; z-index: 1; }
  .search-wrapper { position: fixed; top: 24px; right: 24px; z-index: 99999; width: 420px; }
  .search-container { display: flex; align-items: center; background: #ffffff; width: 100%; height: 56px; border-radius: 50px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3); padding-left: 18px; box-sizing: border-box; }
  .search-icon-badge { width: 32px; height: 32px; background-color: #1e293b; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px; flex-shrink: 0; }
  .search-icon-badge svg { width: 16px; height: 16px; fill: #ffffff; }
  .search-input { flex: 1; border: none; outline: none; background: transparent; padding-right: 12px; font-size: 16px; color: #1e293b; }
  .expand-btn { background: transparent; border: none; cursor: pointer; padding: 10px; display: flex; align-items: center; justify-content: center; }
  .expand-btn svg { width: 18px; height: 18px; stroke: #64748b; stroke-width: 2.5; fill: none; stroke-linecap: round; stroke-linejoin: round; transition: transform 0.3s ease; }
  .search-btn { width: 52px; height: 52px; background-color: #1e293b; border: none; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; margin-right: 2px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25); }
  .search-btn svg { width: 20px; height: 20px; stroke: #ffffff; stroke-width: 2.2; fill: none; stroke-linecap: round; stroke-linejoin: round; }
  .suggestions-dropdown { display: none; position: absolute; background: #ffffff; border-radius: 16px; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25); overflow-y: auto; z-index: 100000; border: 1px solid rgba(0,0,0,0.06); max-height: 250px; width: 100%; box-sizing: border-box; }
  .suggestion-item { padding: 12px 18px; font-size: 14px; color: #1e293b; cursor: pointer; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .suggestion-item:hover { background-color: #f8fafc; }
  .options-panel { display: none; background: #ffffff; width: 100%; margin-top: 10px; border-radius: 24px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25); padding: 20px; box-sizing: border-box; border: 1px solid rgba(0,0,0,0.06); }
  .option-group { margin-bottom: 14px; }
  .option-group label { display: block; font-size: 12px; font-weight: 600; color: #64748b; margin-bottom: 4px; text-transform: uppercase; }
  .input-with-icon { display: flex; align-items: center; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0 12px; height: 44px; position: relative; }
  .field-icon { width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 10px; flex-shrink: 0; }
  .field-icon.black { background-color: #1e293b; }
  .field-icon.black svg { fill: #ffffff; width: 12px; height: 12px; }
  .field-icon.red { background-color: #ef4444; }
  .field-icon.red svg { fill: #ffffff; width: 12px; height: 12px; }
  .option-input { width: 100%; border: none; background: transparent; font-size: 14px; color: #1e293b; outline: none; }
  .mode-selector { display: flex; background: #f1f5f9; border-radius: 12px; padding: 4px; margin-bottom: 16px; }
  .mode-btn { flex: 1; text-align: center; padding: 8px; font-size: 13px; font-weight: 600; color: #64748b; border-radius: 9px; cursor: pointer; transition: all 0.2s; border: none; background: transparent; }
  .mode-btn.active { background: #ffffff; color: #1e293b; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
  .checkbox-group { display: flex; flex-direction: column; gap: 10px; margin-top: 16px; padding-top: 12px; border-top: 1px solid #f1f5f9; }
  .checkbox-label { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #334155; cursor: pointer; }
  .checkbox-label input { width: 16px; height: 16px; accent-color: #1e293b; cursor: pointer; }
  .routes-sidebar { display: none; position: fixed; top: 24px; left: 24px; z-index: 99999; width: 380px; background: #ffffff; border-radius: 24px; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3); padding: 20px; box-sizing: border-box; max-height: calc(100vh - 48px); overflow-y: auto; }
  .routes-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; }
  .routes-title { font-size: 16px; font-weight: 700; color: #1e293b; }
  .close-sidebar { background: transparent; border: none; font-size: 18px; color: #94a3b8; cursor: pointer; }
  .route-card { background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 16px; padding: 14px; margin-bottom: 12px; cursor: pointer; transition: all 0.2s ease; }
  .route-card:hover { border-color: #3b82f6; background: #f1f5f9; }
  .route-card.active { border-color: #1e293b; background: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
  .route-card-title { font-size: 14px; font-weight: 600; color: #1e293b; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
  .route-dot { width: 10px; height: 10px; border-radius: 50%; }
  .route-stats { display: flex; gap: 16px; font-size: 13px; color: #64748b; font-weight: 500; }
  .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(11, 15, 25, 0.75); z-index: 999999; backdrop-filter: blur(4px); justify-content: center; align-items: center; }
  .modal-card { background: #ffffff; width: 360px; border-radius: 24px; padding: 24px; box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4); box-sizing: border-box; }
  .modal-title { font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
  .modal-subtitle { font-size: 13px; color: #64748b; margin-bottom: 16px; }
  .value-input-group { margin-bottom: 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 12px 16px; }
  .value-input-group label { display: block; font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 6px; text-transform: uppercase; }
  .number-input-wrapper { display: flex; align-items: center; justify-content: space-between; }
  .number-input-wrapper input { width: 100%; border: none; background: transparent; font-size: 18px; font-weight: 600; color: #1e293b; outline: none; }
  .unit-label { font-size: 14px; font-weight: 600; color: #64748b; margin-left: 8px; }
  .depart-btn { width: 100%; height: 48px; background-color: #1e293b; color: #ffffff; border: none; border-radius: 14px; font-size: 16px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); }
  .close-modal { background: transparent; border: none; font-size: 20px; color: #94a3b8; cursor: pointer; }
</style>
</head>
<body>

<div id="map"></div>

<div id="routesSidebar" class="routes-sidebar">
  <div class="routes-header">
    <div class="routes-title" id="sidebarTitle">Ideale Toeren</div>
    <button class="close-sidebar" onclick="closeRoutesSidebar()">&times;</button>
  </div>
  <div id="routesListContainer"></div>
</div>

<div class="search-wrapper">
  <div class="search-container" id="mainSearchContainer" style="position: relative;">
    <div class="search-icon-badge">
      <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
    </div>
    <input type="text" id="searchInput" class="search-input" placeholder="Waar wil je vertrekken?" autocomplete="off">
    <button class="expand-btn" id="expandBtn" title="Opties weergeven">
      <svg id="arrowIcon" viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"></polyline></svg>
    </button>
    <button class="search-btn" onclick="handleSearchClick()">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </button>
  </div>

  <div id="optionsPanel" class="options-panel">
    <div class="mode-selector">
      <button class="mode-btn active" id="modeLoopBtn" onclick="setRouteMode('loop')">Rondrit (Lus)</button>
      <button class="mode-btn" id="modePointBtn" onclick="setRouteMode('point')">Start ➔ Eind</button>
    </div>

    <div class="option-group">
      <label>Vertrekpunt</label>
      <div class="input-with-icon">
        <div class="field-icon black">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <input type="text" id="startInput" class="option-input" placeholder="Startlocatie..." autocomplete="off">
      </div>
    </div>

    <div class="option-group" id="endGroup" style="display: none;">
      <label>Eindbestemming</label>
      <div class="input-with-icon">
        <div class="field-icon red">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <input type="text" id="endInput" class="option-input" placeholder="Waar wil je naartoe?" autocomplete="off">
      </div>
    </div>

    <div class="checkbox-group">
      <label class="checkbox-label">
        <input type="checkbox" id="chkHighways" checked> Autostrades & snelle wegen vermijden (Strikt)
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

<div id="suggestions" class="suggestions-dropdown"></div>

<div id="routeModal" class="modal-overlay">
  <div class="modal-card">
    <div class="modal-title">
      Rondrit Configuratie
      <button class="close-modal" onclick="closeRouteModal()">&times;</button>
    </div>
    <div class="modal-subtitle">Hoe lang moet de lus ongeveer zijn?</div>

    <div class="value-input-group">
      <label>Gewenste afstand</label>
      <div class="number-input-wrapper">
        <input type="number" id="routeValueInput" value="30" min="2" max="300" step="1">
        <span class="unit-label">km</span>
      </div>
    </div>

    <button class="depart-btn" onclick="startNavigation()">Bereken Lus</button>
  </div>
</div>

<script>
  let map = L.map('map', { zoomControl: false, attributionControl: false }).setView([50.8280, 3.2648], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

  let startMarker = null;
  let endMarker = null;
  let activeRouteLayers = [];
  
  let startLat = 50.8280;
  let startLon = 3.2648;
  let endLat = null;
  let endLon = null;

  let currentMode = 'loop';

  const input = document.getElementById('searchInput');
  const startInput = document.getElementById('startInput');
  const endInput = document.getElementById('endInput');
  const endGroup = document.getElementById('endGroup');
  const suggestionsBox = document.getElementById('suggestions');
  const expandBtn = document.getElementById('expandBtn');
  const optionsPanel = document.getElementById('optionsPanel');
  const arrowIcon = document.getElementById('arrowIcon');
  const mainSearchContainer = document.getElementById('mainSearchContainer');
  const routeModal = document.getElementById('routeModal');
  const routesSidebar = document.getElementById('routesSidebar');
  const routesListContainer = document.getElementById('routesListContainer');
  const routeValueInput = document.getElementById('routeValueInput');
  const sidebarTitle = document.getElementById('sidebarTitle');

  let activeField = 'main';
  let timeoutId = null;

  function updateMapMarkers() {
    if (startMarker) map.removeLayer(startMarker);
    if (endMarker) map.removeLayer(endMarker);

    const blackIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background-color: #1e293b; width: 26px; height: 26px; border-radius: 50%; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div></div>',
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });

    const redIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background-color: #ef4444; width: 26px; height: 26px; border-radius: 50%; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div></div>',
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });

    startMarker = L.marker([startLat, startLon], { icon: blackIcon }).addTo(map);
    if (currentMode === 'point' && endLat !== null && endLon !== null) {
      endMarker = L.marker([endLat, endLon], { icon: redIcon }).addTo(map);
      let group = L.featureGroup([startMarker, endMarker]);
      map.fitBounds(group.getBounds(), { padding: [50, 50] });
    } else {
      map.setView([startLat, startLon], 13);
    }
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        startLat = pos.coords.latitude;
        startLon = pos.coords.longitude;
        updateMapMarkers();
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${startLat}&lon=${startLon}&addressdetails=1`, { headers: { 'Accept-Language': 'nl' } })
          .then(res => res.json())
          .then(data => {
            let addr = data.display_name || `${startLat.toFixed(4)}, ${startLon.toFixed(4)}`;
            startInput.value = addr;
            input.value = addr;
          })
          .catch(() => {
            let def = `${startLat.toFixed(4)}, ${startLon.toFixed(4)}`;
            startInput.value = def;
            input.value = def;
          });
      },
      () => { startInput.value = "Lendelede, België"; input.value = "Lendelede, België"; updateMapMarkers(); },
      { timeout: 10000, enableHighAccuracy: true }
    );
  } else { updateMapMarkers(); }

  expandBtn.addEventListener('click', () => {
    const isOpen = optionsPanel.style.display === 'block';
    optionsPanel.style.display = isOpen ? 'none' : 'block';
    arrowIcon.style.transform = isOpen ? 'rotate(0deg)' : 'rotate(180deg)';
  });

  function setRouteMode(mode) {
    currentMode = mode;
    document.getElementById('modeLoopBtn').classList.toggle('active', mode === 'loop');
    document.getElementById('modePointBtn').classList.toggle('active', mode === 'point');
    endGroup.style.display = (mode === 'point') ? 'block' : 'none';
    updateMapMarkers();
  }

  setupAutocomplete(input, 'main');
  setupAutocomplete(startInput, 'start');
  setupAutocomplete(endInput, 'end');

  function setupAutocomplete(field, fieldType) {
    field.addEventListener('input', () => {
      activeField = fieldType;
      const query = field.value.trim();
      if (query.length < 2) { suggestionsBox.style.display = 'none'; return; }

      mainSearchContainer.appendChild(suggestionsBox);
      suggestionsBox.style.top = '62px'; suggestionsBox.style.left = '0px'; suggestionsBox.style.width = '100%';

      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&countrycodes=be`, { headers: { 'Accept-Language': 'nl' } })
          .then(res => res.json())
          .then(data => {
            if (data && data.length > 0) {
              let html = '';
              data.forEach(item => {
                const name = item.display_name.replace(/'/g, "\\'");
                html += `<div class="suggestion-item" onclick="selectSuggestion('${name}', ${item.lat}, ${item.lon}, '${fieldType}')"><span>${item.display_name}</span></div>`;
              });
              suggestionsBox.innerHTML = html;
              suggestionsBox.style.display = 'block';
            } else { suggestionsBox.style.display = 'none'; }
          });
      }, 250);
    });
  }

  window.selectSuggestion = function(val, lat, lon, fieldType) {
    if (fieldType === 'main' || fieldType === 'start') {
      input.value = val;
      startInput.value = val;
      startLat = parseFloat(lat);
      startLon = parseFloat(lon);
    } else if (fieldType === 'end') {
      endInput.value = val;
      endLat = parseFloat(lat);
      endLon = parseFloat(lon);
    }
    updateMapMarkers();
    suggestionsBox.style.display = 'none';
  }

  function handleSearchClick() {
    if (currentMode === 'loop') {
      routeModal.style.display = 'flex';
    } else {
      startNavigation();
    }
  }

  function closeRouteModal() { routeModal.style.display = 'none'; }
  function closeRoutesSidebar() { routesSidebar.style.display = 'none'; clearRoutes(); }
  function clearRoutes() { activeRouteLayers.forEach(l => map.removeLayer(l)); activeRouteLayers = []; }

  // --- VERTROUWDE STABIELE ENGINE (6.28 FACTOR + STRIKTE AUTOSTRADE VERMIJDING) ---
  async function startNavigation() {
    closeRouteModal();
    clearRoutes();

    const avoidHighways = document.getElementById('chkHighways').checked;
    const avoidTolls = document.getElementById('chkTolls').checked;
    const avoidFerries = document.getElementById('chkFerries').checked;

    let serverBase = "https://routing.openstreetmap.de/routed-car/route/v1/driving/";
    let excludes = [];
    if (avoidHighways) {
      excludes.push('motorway');
      excludes.push('trunk');
    }
    if (avoidTolls) excludes.push('toll');
    if (avoidFerries) excludes.push('ferry');

    routesListContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#64748b;">Ideale toeren berekenen...</div>';
    routesSidebar.style.display = 'block';

    let evaluatedRoutes = [];

    if (currentMode === 'loop') {
      sidebarTitle.innerText = "Gegarandeerde Lussen";
      let targetKm = parseFloat(routeValueInput.value);
      
      // De vertrouwde en nauwkeurige straalberekening
      let radius = targetKm / 6.28; 
      let rLat = radius / 111;
      let rLon = radius / (111 * Math.cos(startLat * Math.PI / 180));

      let angles = [0, 1.25, 2.5, 3.76, 5.0];
      let candidateConfigs = [];

      angles.forEach((ang, idx) => {
        let p1Lat = startLat + (rLat * Math.sin(ang));
        let p1Lon = startLon + (rLon * Math.cos(ang));
        let p2Lat = startLat + (rLat * 1.05 * Math.sin(ang + 2.1));
        let p2Lon = startLon + (rLon * 1.05 * Math.cos(ang + 2.1));

        candidateConfigs.push({
          name: `Lus ${idx+1}`,
          waypoints: [
            `${startLon},${startLat}`,
            `${p1Lon},${p1Lat}`,
            `${p2Lon},${p2Lat}`,
            `${startLon},${startLat}`
          ]
        });
      });

      for (let config of candidateConfigs) {
        let url = `${serverBase}${config.waypoints.join(';')}?overview=full&geometries=geojson&continue_straight=true`;
        if (excludes.length > 0) url += `&exclude=${excludes.join(',')}`;

        try {
          let res = await fetch(url);
          let data = await res.json();
          if (data.routes && data.routes.length > 0) {
            let r = data.routes[0];
            let distKm = r.distance / 1000;
            evaluatedRoutes.push({
              name: config.name,
              distance: distKm.toFixed(1),
              duration: (r.duration / 3600).toFixed(1),
              geometry: r.geometry,
              score: Math.abs(distKm - targetKm)
            });
          }
        } catch(e) {}
      }

      if (evaluatedRoutes.length === 0) {
        for (let config of candidateConfigs) {
          let url = `${serverBase}${config.waypoints.join(';')}?overview=full&geometries=geojson`;
          try {
            let res = await fetch(url);
            let data = await res.json();
            if (data.routes && data.routes.length > 0) {
              let r = data.routes[0];
              let distKm = r.distance / 1000;
              evaluatedRoutes.push({
                name: `${config.name} (Flex)`,
                distance: distKm.toFixed(1),
                duration: (r.duration / 3600).toFixed(1),
                geometry: r.geometry,
                score: Math.abs(distKm - targetKm)
              });
            }
          } catch(e) {}
        }
      }

      evaluatedRoutes.sort((a, b) => a.score - b.score);
      renderRouteResults(evaluatedRoutes.slice(0, 3));

    } else {
      sidebarTitle.innerText = "Start ➔ Eindroutes";
      if (endLat === null || endLon === null) {
        routesListContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#ef4444;">Selecteer eerst een geldige eindbestemming.</div>';
        return;
      }

      let waypoints = [`${startLon},${startLat}`, `${endLon},${endLat}`];
      let url = `${serverBase}${waypoints.join(';')}?alternatives=true&overview=full&geometries=geojson&continue_straight=true`;
      if (excludes.length > 0) url += `&exclude=${excludes.join(',')}`;

      try {
        let res = await fetch(url);
        let data = await res.json();
        if (data.routes && data.routes.length > 0) {
          data.routes.forEach((r, idx) => {
            evaluatedRoutes.push({
              name: `Optie ${idx+1}`,
              distance: (r.distance / 1000).toFixed(1),
              duration: (r.duration / 3600).toFixed(1),
              geometry: r.geometry
            });
          });
        }
      } catch(e) {}

      if (evaluatedRoutes.length === 0) {
        let fallbackUrl = `${serverBase}${waypoints.join(';')}?alternatives=true&overview=full&geometries=geojson`;
        try {
          let res = await fetch(fallbackUrl);
          let data = await res.json();
          if (data.routes && data.routes.length > 0) {
            data.routes.forEach((r, idx) => {
              evaluatedRoutes.push({
                name: `Optie ${idx+1} (Flex)`,
                distance: (r.distance / 1000).toFixed(1),
                duration: (r.duration / 3600).toFixed(1),
                geometry: r.geometry
              });
            });
          }
        } catch(e) {}
      }

      renderRouteResults(evaluatedRoutes);
    }
  }

  function renderRouteResults(routes) {
    if (routes.length === 0) {
      routesListContainer.innerHTML = '<div style="text-align:center; padding: 20px; color:#ef4444;">Geen routes gevonden. Pas je opties aan.</div>';
      return;
    }

    let colors = ['#1e293b', '#3b82f6', '#10b981'];
    let html = '';

    routes.forEach((route, index) => {
      let color = colors[index] || '#64748b';
      let coords = route.geometry.coordinates.map(c => [c[1], c[0]]);
      let polyline = L.polyline(coords, { color: color, weight: index === 0 ? 6 : 4, opacity: 0.85 }).addTo(map);
      activeRouteLayers.push(polyline);

      polyline.on('click', () => { selectRouteCard(index); });

      html += `
        <div class="route-card ${index === 0 ? 'active' : ''}" id="routeCard_${index}" onclick="selectRouteCard(${index})">
          <div class="route-card-title">
            <div class="route-dot" style="background-color: ${color};"></div>
            ${route.name}
          </div>
          <div class="route-stats">
            <span>🚗 ${route.distance} km</span>
            <span>⏱️ ${route.duration} uur</span>
          </div>
        </div>
      `;
    });

    routesListContainer.innerHTML = html;
    if (activeRouteLayers.length > 0) {
      map.fitBounds(activeRouteLayers[0].getBounds(), { padding: [50, 50] });
    }
  }

  window.selectRouteCard = function(index) {
    document.querySelectorAll('.route-card').forEach((card, idx) => {
      if (idx === index) {
        card.classList.add('active');
        if (activeRouteLayers[idx]) {
          activeRouteLayers[idx].bringToFront();
          map.fitBounds(activeRouteLayers[idx].getBounds(), { padding: [50, 50] });
        }
      } else {
        card.classList.remove('active');
      }
    });
  };
</script>
</body>
</html>
"""

components.html(app_html, height=800, scrolling=False)
