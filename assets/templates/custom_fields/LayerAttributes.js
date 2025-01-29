import React, {useEffect, useState} from "react";

export const LayerAttributes = (
  {
    layerName = ""
  }
) => {
  let [attributes, setAttributes] = useState([]);

  useEffect(() => {
    if (!layerName) {
      setAttributes([])
      return;
    }

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

      })
      .catch(error => {
        console.error('Error:', error);
        setAttributes([])
      });

  }, [layerName])

  if (attributes.length == 0) {
    return <div className="ui red message">Error: No WFS layer named <code>{layerName}</code> found!</div>
  }

  const attributeRows = attributes.map(attribute => <tr key={attribute.name}>
    <td>{attribute.name}</td>
    <td>{attribute.localType}</td>
  </tr>)

  return <table className="ui unstackable very compact table striped selectable">
    <thead>
    <tr>
      <th>Name</th>
      <th>Type</th>
    </tr>
    </thead>
    <tbody>
    {attributeRows}
    </tbody>
  </table>
}
