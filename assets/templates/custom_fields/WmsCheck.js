import React, {useEffect, useState} from "react";

import {Map} from "./Map.js"

export const WmsCheck = (
  {
    layerName = "",
    boundingBox = "",
  }
) => {
  const [layerFound, setLayerFound] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true)
    setError(null)
    setLayerFound(false)

    const formData = new FormData();
    formData.append("url", "https://maps-public.geo.nyu.edu/geoserver/sdr/wfs");
    formData.append("layers", layerName);

    fetch("/geoserver/describe_layer", {
      method: "POST", body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data["exceptions"]) {
          setError("Layer not found")
          setLoading(false)
        } else {
          setLayerFound(true)
          setLoading(false)
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setLayerFound(true)
        setLoading(false)
      });
  }, [layerName]);

  if (loading) {
    return <div className="ui active inverted dimmer">
      <div className="ui text loader">Loading map...</div>
    </div>
  }

  if (error) {
    return <div className="ui red message">Error: No WMS layer named <code>{layerName}</code> found!</div>
  }

  return <Map layerName={layerName} boundingBox={boundingBox}/>
};
