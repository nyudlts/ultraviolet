import React, {useEffect, useRef, useState} from "react";

import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const ActualMap = (
  {
    layerName = "",
    boundingBox = ""
  }
) => {
  const mapRef = useRef(null);

  useEffect(() => {
    const map = L.map(mapRef.current).setView([0, 0], 1);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{retina}.png', {
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://carto.com/attributions">Carto</a>',
      maxZoom: 18,
      worldCopyJump: true,
      retina: "@2x",
    }).addTo(map);

    if (layerName != "") {
      const wmsLayer = L.tileLayer.wms("https://maps-public.geo.nyu.edu/geoserver/sdr/wms", {
        layers: layerName,
        format: 'image/png',
        transparent: true,
        opacity: 0.75
      });

      wmsLayer.addTo(map);
      wmsLayer.setOpacity(0.75);
    }

    if (boundingBox != "") {
      const match = boundingBox.match(/ENVELOPE\(([-\d.]+), ([-\d.]+), ([-\d.]+), ([-\d.]+)\)/);

      if (match) {
        let [_, minLon, maxLon, minLat, maxLat] = match;

        map.fitBounds([[minLat, minLon], [maxLat, maxLon]]);
      }
    }

    return () => map.remove();
  }, [layerName])

  return (
    <div ref={mapRef} id="map" style={{height: '440px', width: '100%'}}/>
  );
}

export const Map = (
  {
    layerName = "",
    boundingBox = "",
  }
) => {
  const mapRef = useRef(null);
  const [layerFound, setLayerFound] = useState(false);

  useEffect(() => {
    const formData = new FormData();
    formData.append("url", "https://maps-public.geo.nyu.edu/geoserver/sdr/wfs");
    formData.append("layers", layerName);

    fetch("/geoserver/describe_layer", {
      method: "POST", body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data["exceptions"]) {
          setLayerFound(false)
        } else {
          setLayerFound(true)
        }
      })
      .catch(error => {
        setLayerFound(false)
        console.error('Error:', error);
      });
  }, [layerName]);

  if (layerFound) {
    return <ActualMap layerName={layerName} boundingBox={boundingBox}/>
  } else {
    return <div className="ui red message">Error: No WMS layer named <code>{layerName}</code> found!</div>
  }
};
