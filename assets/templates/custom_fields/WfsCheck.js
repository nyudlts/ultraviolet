import React, {useEffect, useState} from "react";
import {WfsAttributes} from "./WfsAttributes";

export const WfsCheck = (
  {
    layerName = ""
  }
) => {
  const [attributes, setAttributes] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true)
    setError(null)
    setAttributes(null)

    const formData = new FormData();
    formData.append("url", "https://maps-public.geo.nyu.edu/geoserver/sdr/wfs");
    formData.append("layers", layerName);

    fetch("/geoserver/describe_feature_type", {
      method: "POST", body: formData
    })
      .then(response => response.json())
      .then(data => {
        const sortedAttributes = data.featureTypes[0].properties.sort((a, b) => {
          return a.name.localeCompare(b.name)
        })

        setAttributes(sortedAttributes)
        setLoading(false)
      })
      .catch(error => {
        setError(error)
        setLoading(false)
      });
  }, [layerName]);

  if (loading) {
    return <div className="ui active inverted dimmer">
      <div className="ui text loader">Loading attributes...</div>
    </div>
  }

  if (error) {
    return <div className="ui red message">Error: No WFS layer named <code>{layerName}</code> found!</div>
  }

  return <WfsAttributes attributes={attributes}/>
}
