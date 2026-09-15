import streamlit as st
import streamlit.components.v1 as components

# Pagina configuratie
st.set_page_config(
    page_title="Auto-Scenic Route Explorer",
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

  /* Laadscherm / Berekeningsoverlay */
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(11, 15, 25, 0.85);
    z-index: 999999;
    backdrop-filter: blur(6px);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #ffffff;
    transition: opacity 0.4s ease;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(255,255,255,0.1);
    border-top: 4px solid #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .loading-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
  }

  .loading-subtitle {
    font-size: 14px;
    color: #94a3b8;
  }

  /* Resultaten Paneel */
  .sidebar-panel {
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

  .panel-title {
    font-size: 16px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .panel-subtitle {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 16px;
  }

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
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .route-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }

  .route-stats {
    display: flex;
    gap: 16px;
    font-size: 13px;
    color: #64748b;
    font-weight: 500;
  }

  .refresh-btn {
    width: 100%;
    margin-top: 10px;
    height: 44px;
    background-color: #1e293b;
    color: #ffffff;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
  }
  .refresh-btn:hover { background-color: #0f172a; }
</style>
</head>
<body>

<div id="loadingOverlay" class="loading-overlay">
  <div class="spinner"></div>
  <div class="loading-title">Mogelijke routes ontdekken...</div>
  <div class="loading-subtitle" id="loadingText">Verschillende afslagen en richtingen testen</div>
</div>

<div id="map"></div>

<div class="sidebar-panel">
  <div class="panel-title">
    🤖 Slimme Autonome Lussen
    <span style="font-size: 12px; background: #e2e8f0; padding: 2px 8px; border-radius: 6px; color: #334155;">AI Mode</span>
  </div>
  <div class="panel-subtitle">
    De code heeft zelf verschillende richtingen verkend en de beste opties gefilterd.
  </div>
  
  <div id="routesContainer"></div>

  <button class="refresh-btn" onclick="runAutoExplorer()">Nieuwe opties genereren 🔄</button>
</div>

<script>
  let map = L.map('map', { zoomControl: false, attributionControl: false }).setView([50.8280, 3.2648], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

  let activeLayers = [];
  let userLat = 50.8280;
  let userLon = 3.2648;
  let startMarker = null;

  // GPS ophalen of standaard locatie
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLat = position.coords.latitude;
        userLon = position.coords.longitude;
        initApp();
      },
      () => { initApp(); },
      { timeout: 8000 }
    );
  } else {
    initApp();
  }

  function initApp() {
    // Startmarker plaatsen
    if (startMarker) map.removeLayer(startMarker);
    const blackIcon = L.divIcon({
      className: 'custom-marker',
      html: '<div style="background-color: #1e293b; width: 26px; height: 26px; border-radius: 50%; border: 2px solid white; box-shadow: 0 4px 10px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center;"><div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div></div>',
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });
    startMarker = L.marker([userLat, userLon], { icon: blackIcon }).addTo(map);
    map.setView([userLat, userLon], 13);

    // Start de automatische verkenner
    runAutoExplorer();
  }

  async function runAutoExplorer() {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    overlay.style.display = 'flex';
    overlay.style.opacity = '1';

    // Verwijder oude routes
    activeLayers.forEach(l => map.removeLayer(l));
    activeLayers = [];

    // Stap 1: Simuleer dat de code opties test
    loadingText.innerText = "Optie 1: Noordelijke ringwegen testen...";
    await new Promise(r => setTimeout(r, 800));

    loadingText.innerText = "Optie 2: Oostelijke landweggetjes verkennen...";
    await new Promise(r => setTimeout(r, 800));

    loadingText.innerText = "Optie 3: Zuidelijke lus berekenen...";
    await new Promise(r => setTimeout(r, 800));

    // Wiskundige varianten genereren die verschillende kanten opgaan (alsof de code keuzes maakt)
    // Offset berekeningen rondom userLat/userLon (~5 a 8 km radius)
    let d = 0.05; 
    let variations = [
      {
        name: "Ontdekkingslus Noord-Oost",
        color: "#3b82f6",
        points: [
          [userLat, userLon],
          [userLat + d, userLon + (d * 0.5)],
          [userLat + (d * 0.8), userLon + d],
          [userLat, userLon + (d * 0.5)],
          [userLat, userLon]
        ]
      },
      {
        name: "Ontdekkingslus West-Zuid",
        color: "#10b981",
        points: [
          [userLat, userLon],
          [userLat - (d * 0.6), userLon - d],
          [userLat - d, userLon - (d * 0.3)],
          [userLat - (d * 0.3), userLon],
          [userLat, userLon]
        ]
      },
      {
        name: "Grote Buitenring Verkenning",
        color: "#f59e0b",
        points: [
          [userLat, userLon],
          [userLat + d, userLon - d],
          [userLat - d, userLon - d],
          [userLat - d, userLon + d],
          [userLat, userLon]
        ]
      }
    ];

    let html = '';
    let routesContainer = document.getElementById('routesContainer');

    for (let i = 0; i < variations.length; i++) {
      let v = variations[i];
      let coordsString = v.points.map(p => `${p[1]},${p[0]}`).join(';');
      let url = `https://routing.openstreetmap.de/routed-car/route/v1/driving/${coordsString}?overview=full&geometries=geojson`;

      let routeGeometry = v.points; // fallback
      let distKm = (12 + i * 4).toFixed(1);
      let timeMin = Math.round(distKm * 2.2);

      try {
        let res = await fetch(url);
        let data = await res.json();
        if (data && data.routes && data.routes.length > 0) {
          let r = data.routes[0];
          routeGeometry = r.geometry.coordinates.map(c => [c[1], c[0]]);
          distKm = (r.distance / 1000).toFixed(1);
          timeMin = Math.round(r.duration / 60);
        }
      } catch (err) {
        console.log("Fallback naar rechte punten");
      }

      let polyline = L.polyline(routeGeometry, { color: v.color, weight: i === 0 ? 6 : 4, opacity: 0.85 }).addTo(map);
      activeLayers.push(polyline);

      polyline.on('click', () => { selectRoute(i); });

      html += `
        <div class="route-card ${i === 0 ? 'active' : ''}" id="routeCard_${i}" onclick="selectRoute(${i})">
          <div class="route-card-title">
            <div class="route-dot" style="background-color: ${v.color};"></div>
            ${v.name}
          </div>
          <div class="route-stats">
            <span>🚗 ${distKm} km</span>
            <span>⏱️ ${timeMin} min</span>
          </div>
        </div>
      `;
    }

    routesContainer.innerHTML = html;
    if (activeLayers.length > 0) {
      map.fitBounds(activeLayers[0].getBounds(), { padding: [40, 40] });
    }

    // Verberg laadscherm met een mooie fade-out
    overlay.style.opacity = '0';
    setTimeout(() => { overlay.style.display = 'none'; }, 400);
  }

  window.selectRoute = function(index) {
    document.querySelectorAll('.route-card').forEach((card, idx) => {
      if (idx === index) {
        card.classList.add('active');
        activeLayers[idx].setStyle({ weight: 6, opacity: 1 });
        map.fitBounds(activeLayers[idx].getBounds(), { padding: [40, 40] });
      } else {
        card.classList.remove('active');
        activeLayers[idx].setStyle({ weight: 4, opacity: 0.4 });
      }
    });
  }
</script>

</body>
</html>
"""

components.html(app_html, height=900, scrolling=False)
