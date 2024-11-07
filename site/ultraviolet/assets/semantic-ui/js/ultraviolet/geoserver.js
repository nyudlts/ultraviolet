import L from "leaflet"
import "leaflet/dist/leaflet.css";

document.addEventListener("DOMContentLoaded", () => {
  const mapElement = document.getElementById("map");
  const baseUrl = mapElement.getAttribute("data-base-url")
  const layerName = mapElement.getAttribute("data-layer-name")
  const bounds = mapElement.getAttribute("data-bounds")

  const map = L.map('map').setView([0, 0], 13);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  const wmsLayer = L.tileLayer.wms(baseUrl, {
    layers: layerName,
    format: 'image/png',
    transparent: true
  });

  wmsLayer.addTo(map);
  wmsLayer.setOpacity(0.75);

  const regex = /ENVELOPE\(([-\d.]+), ([-\d.]+), ([-\d.]+), ([-\d.]+)\)/;
  const match = bounds.match(regex);

  if (match) {
    const minLon = parseFloat(match[1]);
    const maxLon = parseFloat(match[2]);
    const minLat = parseFloat(match[3]);
    const maxLat = parseFloat(match[4]);

    const bounds = [[minLat, minLon], [maxLat, maxLon]];

    map.fitBounds(bounds);
  }
});
