import React, {useEffect, useRef, useState} from "react";

import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export const WmsMap = (
  {
    layerName = "",
    boundingBox = "",
    serverUrl = ""
  }
) => {
  const mapRef = useRef(null);
  const [envelope, setEnvelope] = useState("");

  useEffect(() => {
    const map = L.map(mapRef.current, {zoomSnap: 0.25}).setView([0, 0], 1);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{retina}.png', {
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://carto.com/attributions">Carto</a>',
      maxZoom: 18,
      worldCopyJump: true,
      retina: "@2x",
    }).addTo(map);

    if (layerName !== "") {
      const wmsLayer = L.tileLayer.wms(`${serverUrl}/wms`, {
        layers: layerName,
        format: 'image/png',
        transparent: true,
        opacity: 0.75
      });

      wmsLayer.addTo(map);
      wmsLayer.setOpacity(0.75);
    }

    if (boundingBox !== "") {
      const match = boundingBox.match(/ENVELOPE\(([-\d.]+), ([-\d.]+), ([-\d.]+), ([-\d.]+)\)/);

      if (match) {
        let [_, minLon, maxLon, minLat, maxLat] = match;

        map.fitBounds([[minLat, minLon], [maxLat, maxLon]]);
      }
    }

    map.on('moveend', () => {
      const bounds = map.getBounds();
      setEnvelope(`ENVELOPE(${bounds.getWest()}, ${bounds.getEast()}, ${bounds.getNorth()}, ${bounds.getSouth()})`);
    });

    return () => map.remove();
  }, [layerName, boundingBox])

  return (
    <>
      <div ref={mapRef} id="map" style={{height: '440px', width: '100%'}}/>
      <p>Shift-click &amp; drag to draw a bounding box to zoom to. Scroll wheel can be used for a finer zoom control.</p>
      <p><input type="text" value={envelope}/></p>
    </>
  );
}