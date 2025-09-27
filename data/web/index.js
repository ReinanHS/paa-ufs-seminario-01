let cfg = {};
let population = [],
  costs = [],
  bestCost = Infinity,
  gen = 0,
  routeColors = [],
  history = [];
let stopAnim = false,
  animationFrameId = null;
let convergenceChart;
const defaultCitiesTemplate = [
  { name: "Aracaju", lat: -10.9095421, lng: -37.0747732 },
  { name: "N. S. Socorro", lat: -10.855, lng: -37.1261 },
  { name: "São Cristóvão", lat: -11.0136465, lng: -37.2071134 },
  { name: "Itabaiana", lat: -10.6858763, lng: -37.4247007 },
  { name: "Lagarto", lat: -10.9145344, lng: -37.6638508 },
  { name: "Estância", lat: -11.2687119, lng: -37.4421355 },
  { name: "Propriá", lat: -10.230052, lng: -36.8394326 },
  { name: "Tobias Barreto", lat: -11.1839, lng: -37.9983 },
  { name: "N. S. Glória", lat: -10.2156554, lng: -37.4212807 },
  { name: "Canindé de S.F.", lat: -9.64194, lng: -37.78778 },
  { name: "Itaporanga", lat: -10.991997, lng: -37.3065 },
  { name: "Boquim", lat: -11.1415, lng: -37.61916 },
];
let cities = [];
let W;
let isDragging = false;
let draggedPointId = null;
let cityColorPalette = [];
let currentPhase = "city-selection";

const SPRITES = {
  FLYING_0: "flying-0",
  FLYING_1: "flying-1",
  SHADOW_0: "shadow-0",
  SHADOW_1: "shadow-1",
  LAYER_HELICOPTER: "planes-symbols",
  LAYER_SHADOW: "planes-shadow",
};
let currentSpriteIndex = 0;
let planeAnimationId = null;

const map = new maplibregl.Map({
  container: "map",
  style: {
    version: 8,
    glyphs: "https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",
    sources: {
      osm: {
        type: "raster",
        tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
        tileSize: 256,
        attribution: "© OpenStreetMap",
      },
    },
    layers: [{ id: "osm", type: "raster", source: "osm" }],
  },
  center: [-37.19, -10.85],
  zoom: 7.2,
});
map.addControl(
  new maplibregl.NavigationControl({ visualizePitch: false }),
  "top-right"
);

function setPhase(phase) {
  currentPhase = phase;

  const isCitySelection = phase === "city-selection";
  const isGaSettings = phase === "ga-settings";
  const isSimulation = phase === "simulation";

  document.getElementById("city-selection-panel").style.display =
    isCitySelection ? "block" : "none";
  document.getElementById("ga-settings").style.display = isGaSettings
    ? "block"
    : "none";
  document.getElementById("simulation-controls").style.display =
    isSimulation ? "block" : "none";

  document.getElementById("right-panel").style.display =
    isCitySelection || isGaSettings || isSimulation ? "flex" : "none";

  document.getElementById("project-info").style.display = isCitySelection
    ? "block"
    : "none";
  document.getElementById("ga-strategy-info").style.display = isGaSettings
    ? "block"
    : "none";
  document.getElementById("simulation-data-view").style.display =
    isSimulation ? "flex" : "none";

  map.getCanvas().style.cursor = isCitySelection ? "pointer" : "";

  if (isCitySelection) {
    map.on("click", onMapClick);
    map.on("mousedown", "editable-cities-points", onMouseDown);

    cancelAnimationFrame(planeAnimationId);
  } else {
    map.off("click", onMapClick);
    map.off("mousedown", "editable-cities-points", onMouseDown);

    map.off("mousemove", onMouseMove);
    map.off("mouseup", onMouseUp);
    isDragging = false;
    draggedPointId = null;

    if (isSimulation) {
      if (!planeAnimationId) {
        animatePlanes(0);
      }
    }
  }

  const downloadButtons = document.querySelector(".download-section");
  if (downloadButtons) {
    const isDownloadEnabled = cities.length >= 3;
    downloadButtons.style.display =
      isDownloadEnabled && isCitySelection ? "block" : "none";
  }
}

function refreshEditableCities() {
  const cityFeatures = cities.map((c, idx) => ({
    type: "Feature",
    id: idx,
    properties: {
      name: c.name,
      id: idx,
      color: c.color,
    },
    geometry: { type: "Point", coordinates: [c.lng, c.lat] },
  }));
  map
    .getSource("editable-cities")
    .setData({ type: "FeatureCollection", features: cityFeatures });
  document.getElementById("city-count").textContent = cities.length;

  setPhase(currentPhase);
}

function onMapClick(e) {
  if (isDragging || currentPhase !== "city-selection") return;
  const features = map.queryRenderedFeatures(e.point, {
    layers: ["editable-cities-points"],
  });
  if (features.length > 0) {
    cities.splice(features[0].properties.id, 1);
  } else {
    const { lng, lat } = e.lngLat;
    const newColor =
      cityColorPalette[cities.length % cityColorPalette.length];
    cities.push({
      name: `Ponto ${cities.length}`,
      lat,
      lng,
      color: newColor,
    });
  }
  refreshEditableCities();
}

function onMouseDown(e) {
  if (currentPhase !== "city-selection") return;
  const features = map.queryRenderedFeatures(e.point, {
    layers: ["editable-cities-points"],
  });
  if (features.length === 0) return;
  isDragging = true;
  draggedPointId = features[0].properties.id;
  map.getCanvas().style.cursor = "grabbing";
  e.preventDefault();
  map.on("mousemove", onMouseMove);
  map.once("mouseup", onMouseUp);
}

function onMouseMove(e) {
  if (!isDragging || currentPhase !== "city-selection") return;
  const { lng, lat } = e.lngLat;
  cities[draggedPointId].lng = lng;
  cities[draggedPointId].lat = lat;
  refreshEditableCities();
}

function onMouseUp() {
  if (currentPhase !== "city-selection") return;
  isDragging = false;
  draggedPointId = null;
  map.getCanvas().style.cursor = "pointer";
  map.off("mousemove", onMouseMove);
}

function buildMatrix() {
  const n = cities.length;
  W = Array.from({ length: n }, () => Array(n).fill(0));
  for (let i = 0; i < n; i++)
    for (let j = 0; j < n; j++) {
      W[i][j] = i === j ? 0 : haversineKm(cities[i], cities[j]);
    }
}
function haversineKm(a, b) {
  const R = 6371;
  const t = (x) => (x * Math.PI) / 180;
  const d = t(b.lat - a.lat);
  const l = t(b.lng - a.lng);
  const s =
    Math.sin(d / 2) ** 2 +
    Math.cos(t(a.lat)) * Math.cos(t(b.lat)) * Math.sin(l / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}

function calculateBearing(start, end) {
  const lat1 = (start.lat * Math.PI) / 180;
  const lat2 = (end.lat * Math.PI) / 180;
  const lon1 = (start.lng * Math.PI) / 180;
  const lon2 = (end.lng * Math.PI) / 180;

  const y = Math.sin(lon2 - lon1) * Math.cos(lat2);
  const x =
    Math.cos(lat1) * Math.sin(lat2) -
    Math.sin(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1);

  let bearingRad = Math.atan2(y, x);
  let bearingDeg = (bearingRad * 180) / Math.PI;

  return (bearingDeg + 360) % 360;
}

function generateHslaColors(count, saturation, lightness, alpha) {
  let colors = [];

  let initialHue = 0;
  const hueStep = 360 / count;

  for (let i = 0; i < count; i++) {
    let hue = (initialHue + i * hueStep) % 360;
    colors.push(`hsla(${hue},${saturation}%,${lightness}%,${alpha})`);
  }
  return colors;
}
function randInt(n) {
  return Math.floor(Math.random() * n);
}
function initPop() {
  const n = cities.length;
  population = [];
  costs = [];
  bestCost = Infinity;
  gen = 0;
  bestRoute = null;
  history = [];
  for (let i = 0; i < cfg.popSize; i++) {
    const r = shuffle([...Array(n).keys()]);
    population.push(r);
    const c = routeCost(r);
    costs.push(c);
    if (c < bestCost) {
      bestCost = c;
      bestRoute = r.slice();
    }
  }
  updateStats();
}
function stepGen() {
  const e = cfg.elitism ? 2 : 0;
  const i = Array.from({ length: population.length }, (_, i) => i).sort(
    (a, b) => costs[a] - costs[b]
  );
  const l = i.slice(0, e).map((i) => population[i].slice());
  const nP = [...l];

  const mutProb = cfg.mutRate / 100;

  while (nP.length < cfg.popSize) {
    const p1 = tournament(population, 5);
    const p2 = tournament(population, 5);
    let [c1, c2] = Math.random() < 0.9 ? ox(p1, p2) : [p1, p2];

    if (Math.random() < mutProb) mutInv(c1);
    if (Math.random() < mutProb) mutInv(c2);

    nP.push(c1);
    if (nP.length < cfg.popSize) nP.push(c2);
  }
  population = nP;
  costs = population.map(routeCost);
  const gBI = costs.indexOf(Math.min(...costs));
  const gB = costs[gBI];
  if (gB < bestCost) {
    bestCost = gB;
    bestRoute = population[gBI].slice();
  }
  gen++;
  const avg = costs.reduce((a, b) => a + b, 0) / costs.length;
  history.push({ gen, best: gB, avg: avg });
  updateStats();
}
function routeCost(r) {
  if (!W || W.length === 0) return Infinity;
  let s = 0;
  for (let k = 0; k < r.length - 1; k++) s += W[r[k]][r[k + 1]];
  return s + W[r[r.length - 1]][r[0]];
}
function tournament(p, k) {
  let bI = -1,
    b = Infinity;
  for (let t = 0; t < k; t++) {
    const i = randInt(p.length);
    const c = costs[i];
    if (c < b) {
      b = c;
      bI = i;
    }
  }
  return p[bI].slice();
}
function ox(p1, p2) {
  const n = p1.length;
  let a = randInt(n),
    b = randInt(n);
  if (a > b) [a, b] = [b, a];
  const m = (A, B) => {
    const c = new Array(n).fill(null);
    c.splice(a, b - a + 1, ...A.slice(a, b + 1));
    const r = B.filter((g) => !c.includes(g));
    let i = 0;
    for (let j = 0; j < n; j++) if (c[j] === null) c[j] = r[i++];
    return c;
  };
  return [m(p1, p2), m(p2, p1)];
}
function mutInv(r) {
  let i = randInt(r.length),
    j = randInt(r.length);
  if (i > j) [i, j] = [j, i];
  r.splice(i, j - i + 1, ...r.slice(i, j + 1).reverse());
}
function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = randInt(i + 1);
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

let lastFrameTime = 0;
const FRAME_RATE = 1000 / 10;

function animatePlanes(timestamp) {
  if (!map.loaded()) {
    planeAnimationId = requestAnimationFrame(animatePlanes);
    return;
  }

  if (timestamp - lastFrameTime > FRAME_RATE) {
    currentSpriteIndex = 1 - currentSpriteIndex;
    lastFrameTime = timestamp;

    const iconName =
      currentSpriteIndex === 0 ? SPRITES.FLYING_0 : SPRITES.FLYING_1;
    const shadowName =
      currentSpriteIndex === 0 ? SPRITES.SHADOW_0 : SPRITES.SHADOW_1;

    if (map.getLayer(SPRITES.LAYER_HELICOPTER)) {
      map.setLayoutProperty(
        SPRITES.LAYER_HELICOPTER,
        "icon-image",
        iconName
      );
    }
    if (map.getLayer(SPRITES.LAYER_SHADOW)) {
      map.setLayoutProperty(
        SPRITES.LAYER_SHADOW,
        "icon-image",
        shadowName
      );
    }
  }

  planeAnimationId = requestAnimationFrame(animatePlanes);
}

const SPRITE_URLS = [
  { id: SPRITES.FLYING_0, url: "./img/flying-0.png" },
  { id: SPRITES.FLYING_1, url: "./img/flying-0.png" },
  { id: SPRITES.SHADOW_0, url: "./img/shadow-0.png" },
  { id: SPRITES.SHADOW_1, url: "./img/shadow-0.png" },
];

function loadMapImages(callback) {
  let loadedCount = 0;
  const total = SPRITE_URLS.length;

  if (total === 0) return callback();

  SPRITE_URLS.forEach(({ id, url }) => {
    map.loadImage(url, (error, image) => {
      if (error) {
        console.error(`Erro ao carregar imagem ${id}:`, error);
      } else {
        map.addImage(id, image, { pixelRatio: 1, sdf: false });
        loadedCount++;
      }

      if (loadedCount === total) {
        callback();
      }
    });
  });
}

function ensureLayers() {
  if (!map.getSource("routes"))
    map.addSource("routes", {
      type: "geojson",
      data: { type: "FeatureCollection", features: [] },
    });
  if (!map.getLayer("routes-lines"))
    map.addLayer({
      id: "routes-lines",
      type: "line",
      source: "routes",
      layout: {},
      paint: {
        "line-width": ["get", "lineWidth"],
        "line-opacity": 0.7,
        "line-color": ["get", "color"],
      },
    });
  if (!map.getSource("planes"))
    map.addSource("planes", {
      type: "geojson",
      data: { type: "FeatureCollection", features: [] },
    });

  if (!map.getLayer(SPRITES.LAYER_SHADOW))
    map.addLayer({
      id: SPRITES.LAYER_SHADOW,
      type: "symbol",
      source: "planes",
      layout: {
        "icon-image": SPRITES.SHADOW_0,
        "icon-size": ["get", "iconSize"],
        "icon-allow-overlap": true,
        "icon-offset": [0, 8],
        "icon-rotate": ["get", "rotation"],
        "icon-rotation-alignment": "map",
      },
    });

  if (!map.getLayer(SPRITES.LAYER_HELICOPTER))
    map.addLayer({
      id: SPRITES.LAYER_HELICOPTER,
      type: "symbol",
      source: "planes",
      layout: {
        "icon-image": SPRITES.FLYING_0,
        "icon-size": ["get", "iconSize"],
        "icon-allow-overlap": true,
        "icon-rotate": ["get", "rotation"],
        "icon-rotation-alignment": "map",
      },
    });
}

function getPopulationToDisplay() {
  const m = document.getElementById("displayMode").value;
  if (m === "all") {
    return population.map((ind, i) => ({
      individual: ind,
      originalIndex: i,
    }));
  }
  const c = parseInt(m, 10);
  const iP = population.map((ind, i) => ({
    individual: ind,
    cost: costs[i],
    originalIndex: i,
  }));
  iP.sort((a, b) => a.cost - b.cost);
  return iP.slice(0, c);
}
function updateDisplay() {
  ensureLayers();
  const p = getPopulationToDisplay();
  drawRoutes(p);
  updateTopIndividualsTable();
}
function drawRoutes(p) {
  const s = p.length === 1;
  const rF = p.map(({ individual: ind, originalIndex: oI }) => {
    const co = ind
      .concat(ind[0])
      .map((i) => [cities[i].lng, cities[i].lat]);
    return {
      type: "Feature",
      properties: {
        color: s ? "#f43f5e" : routeColors[oI],
        lineWidth: s ? 4 : 2,
      },
      geometry: { type: "LineString", coordinates: co },
    };
  });
  map
    .getSource("routes")
    .setData({ type: "FeatureCollection", features: rF });
  const pF = p.map(({ individual: ind }) => {
    const rotation = 0;
    const co = [cities[ind[0]].lng, cities[ind[0]].lat];
    return {
      type: "Feature",
      properties: { iconSize: s ? 0.6 : 0.5, rotation: rotation },
      geometry: { type: "Point", coordinates: co },
    };
  });
  map
    .getSource("planes")
    .setData({ type: "FeatureCollection", features: pF });
}
function animatePopulation(p, d) {
  if (d === 0) return Promise.resolve();
  const s = p.length === 1;
  let aS = p.map(({ individual: ind }) => ({
    route: ind.concat(ind[0]),
    sI: 0,
    prog: 0,
  }));
  const sD = d / cities.length;
  let sT = null;
  return new Promise((res) => {
    function animStep(t) {
      if (stopAnim) {
        res();
        return;
      }
      if (!sT) sT = t;
      const e = t - sT;
      const pF = aS.map((st) => {
        st.prog = e / sD;
        st.sI = Math.floor(st.prog);

        let rotation = 0;
        let currentCoords;
        let currentCity, nextCity;

        if (st.sI >= st.route.length - 1) {
          currentCity = cities[st.route[st.route.length - 1]];
          nextCity = cities[st.route[0]];

          currentCoords = [currentCity.lng, currentCity.lat];

          rotation = calculateBearing(currentCity, nextCity);
        } else {
          currentCity = cities[st.route[st.sI]];
          nextCity = cities[st.route[st.sI + 1]];
          const sP = st.prog - st.sI;

          const lng =
            currentCity.lng + (nextCity.lng - currentCity.lng) * sP;
          const lat =
            currentCity.lat + (nextCity.lat - currentCity.lat) * sP;

          currentCoords = [lng, lat];

          rotation = calculateBearing(currentCity, nextCity);
        }

        return {
          type: "Feature",
          properties: {
            iconSize: s ? 0.6 : 0.5,
            rotation: rotation,
          },
          geometry: { type: "Point", coordinates: currentCoords },
        };
      });
      map
        .getSource("planes")
        .setData({ type: "FeatureCollection", features: pF });
      if (e < d) {
        animationFrameId = requestAnimationFrame(animStep);
      } else {
        res();
      }
    }
    animationFrameId = requestAnimationFrame(animStep);
  });
}
function initConvergenceChart() {
  const c = document.getElementById("convergenceChart").getContext("2d");
  if (convergenceChart) convergenceChart.destroy();
  convergenceChart = new Chart(c, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Melhor Custo (km)",
          data: [],
          borderColor: "#f43f5e",
          tension: 0.1,
          borderWidth: 2,
        },
        {
          label: "Custo Médio (km)",
          data: [],
          borderColor: "#3b82f6",
          tension: 0.1,
          borderWidth: 1.5,
          borderDash: [5, 5],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      color: "#94a3b8",
      scales: {
        x: { ticks: { color: "#94a3b8" } },
        y: { ticks: { color: "#94a3b8" } },
      },
    },
  });
}
function updateConvergenceChart() {
  if (!convergenceChart || history.length === 0) return;
  const l = history[history.length - 1];
  convergenceChart.data.labels.push(l.gen);
  convergenceChart.data.datasets[0].data.push(l.best);
  convergenceChart.data.datasets[1].data.push(l.avg);
  convergenceChart.update();
}
function updateTopIndividualsTable() {
  const t = document.getElementById("top-individuals-table");
  const top10 = getPopulationToDisplay().slice(0, 10);
  let h =
    "<table><tr><th>#</th><th>Custo (km)</th><th>Cromossomo (Rota)</th></tr>";
  top10.forEach(({ individual: ind, cost: c }, i) => {
    const s = ind.join(" → ");
    h += `<tr><td>${i + 1}</td><td>${c.toFixed(
      2
    )}</td><td class="chromosome">${s}</td></tr>`;
  });
  h += "</table>";
  t.innerHTML = h;
}
function createCityLegend() {
  const l = document.getElementById("city-legend");
  let h = "";
  cities.forEach((c, i) => {
    h += `<p><span class="legend-color-dot" style="background-color: ${c.color
      };"></span><b>${i}</b>: ${c.name || `Ponto ${i}`}</p>`;
  });
  l.innerHTML = h;
}
function updateStats() {
  document.getElementById("statGen").textContent = String(gen);
  document.getElementById("statCost").textContent =
    bestCost === Infinity ? "–" : bestCost.toFixed(2);
}

function setControlsState(isPlaying) {
  document.getElementById("btnPlay").disabled = isPlaying;
  document.getElementById("btnStep").disabled = isPlaying;
  document.getElementById("btnPause").disabled = !isPlaying;
}

function generatePointsCsv() {
  const header = "Indice,Nome,Latitude,Longitude";
  const rows = cities.map((city, index) => {
    const name = `"${city.name.replace(/"/g, '""')}"`;
    return `${index},${name},${city.lat.toFixed(8)},${city.lng.toFixed(
      8
    )}`;
  });
  return [header, ...rows].join("\n");
}

function generateDistancesCsv() {
  if (!W || W.length === 0) {
    buildMatrix();
  }

  const n = W.length;

  const header = "Origem/Destino," + [...Array(n).keys()].join(",");

  const rows = W.map((row, rowIndex) => {
    const rowData = row.map((distance) => distance.toFixed(2));
    return `${rowIndex},${rowData.join(",")}`;
  });

  return [header, ...rows].join("\n");
}

function downloadFile(filename, text) {
  const element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:text/csv;charset=utf-8," + encodeURIComponent(text)
  );
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}

document
  .getElementById("btnConfirmCities")
  .addEventListener("click", () => {
    if (cities.length < 3) {
      console.error(
        "Por favor, defina pelo menos 3 cidades para o trajeto."
      );
      return;
    }

    buildMatrix();
    setPhase("ga-settings");
  });

document
  .getElementById("btnDownloadDistances")
  .addEventListener("click", () => {
    if (cities.length < 3) {
      console.error(
        "É necessário pelo menos 3 cidades para gerar a Matriz de Distâncias."
      );
      return;
    }
    buildMatrix();
    const csvContent = generateDistancesCsv();
    downloadFile("matriz_distancias.csv", csvContent);
  });

document
  .getElementById("btnDownloadPoints")
  .addEventListener("click", () => {
    if (cities.length < 1) {
      console.error("Não há pontos definidos para download.");
      return;
    }
    const csvContent = generatePointsCsv();
    downloadFile("pontos_caixeiro_viajante.csv", csvContent);
  });

document.getElementById("btnStart").addEventListener("click", () => {
  cfg.popSize =
    parseInt(document.getElementById("popSize").value, 10) || 150;
  cfg.gensPerPlay =
    parseInt(document.getElementById("gensPerPlay").value, 10) || 20;
  cfg.mutRate =
    parseInt(document.getElementById("mutRate").value, 10) || 5;
  cfg.elitism = document.getElementById("chkElitism").checked;

  initPop();
  routeColors = generateHslaColors(cfg.popSize, 100, 60, 0.9);
  initConvergenceChart();
  createCityLegend();
  updateDisplay();
  setControlsState(false);
  setPhase("simulation");
});
document.getElementById("btnPlay").addEventListener("click", async () => {
  const b = cfg.gensPerPlay;
  const t = Number(document.getElementById("simTime").value);
  stopAnim = false;
  setControlsState(true);
  let d = t > 0 ? (t * 1000) / b : 0;
  for (let i = 0; i < b; i++) {
    if (stopAnim) break;
    stepGen();
    const p = getPopulationToDisplay();
    updateDisplay();
    updateConvergenceChart();
    await animatePopulation(p, d);
  }
  updateDisplay();
  setControlsState(false);
});
document.getElementById("btnStep").addEventListener("click", async () => {
  stopAnim = false;
  setControlsState(true);
  stepGen();
  const p = getPopulationToDisplay();
  updateDisplay();
  updateConvergenceChart();
  await animatePopulation(p, 2000);
  setControlsState(false);
});
document.getElementById("btnPause").addEventListener("click", () => {
  stopAnim = true;
  cancelAnimationFrame(animationFrameId);
  setControlsState(false);
});
document.getElementById("btnReset").addEventListener("click", () => {
  stopAnim = true;
  cancelAnimationFrame(planeAnimationId);
  cancelAnimationFrame(animationFrameId);
  const e = { type: "FeatureCollection", features: [] };
  if (map.getSource("routes")) map.getSource("routes").setData(e);
  if (map.getSource("planes")) map.getSource("planes").setData(e);
  if (map.getSource("editable-cities"))
    map.getSource("editable-cities").setData(e);
  cities = defaultCitiesTemplate.map((c, i) => ({
    ...c,
    color: cityColorPalette[i % cityColorPalette.length],
  }));
  W = undefined;
  refreshEditableCities();

  setPhase("city-selection");
});
document
  .getElementById("displayMode")
  .addEventListener("change", updateDisplay);

map.on("load", () => {
  cityColorPalette = generateHslaColors(50, 95, 55, 1);

  map.addSource("editable-cities", {
    type: "geojson",
    data: { type: "FeatureCollection", features: [] },
  });
  map.addLayer({
    id: "editable-cities-points",
    type: "circle",
    source: "editable-cities",
    paint: {
      "circle-radius": 8,
      "circle-color": ["get", "color"],
      "circle-stroke-color": "#ffffff",
      "circle-stroke-width": 2,
    },
  });

  loadMapImages(() => {
    ensureLayers();
    cities = defaultCitiesTemplate.map((c, i) => ({
      ...c,
      color: cityColorPalette[i % cityColorPalette.length],
    }));
    refreshEditableCities();

    setPhase("city-selection");
  });
});