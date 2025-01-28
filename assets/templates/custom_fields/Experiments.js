import React, {useEffect, useRef, useState} from "react";

import {BooleanCheckbox, Input} from "react-invenio-forms";
import {Grid, GridColumn} from 'semantic-ui-react'
import {useFormikContext} from 'formik';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const Map = ({layerName = "", boundingBox = "", center = [0, 0], zoom = 1}) => {
  const mapRef = useRef(null);

  useEffect(() => {
    const map = L.map(mapRef.current).setView(center, zoom);

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

    const match = boundingBox.match(/ENVELOPE\(([-\d.]+), ([-\d.]+), ([-\d.]+), ([-\d.]+)\)/);

    if (match) {
      let [_, minLon, maxLon, minLat, maxLat] = match;

      const bounds = [[minLat, minLon], [maxLat, maxLon]];

      map.fitBounds(bounds);
    }

    return () => map.remove();
  }, [center, zoom, layerName]);

  return (
    <div ref={mapRef} id="map" style={{height: '440px', width: '100%'}}/>
  );
};

export const Experiments = props => {
  const {
    fieldPath, // injected by the custom field loader via the `field` config property
    layer,
    has_wms,
    has_wfs,
    bounds,
  } = props;

  const [layerName, setLayerName] = useState("")
  const [hasWms, setHasWms] = useState(false)
  const [hasWfs, setHasWfs] = useState(false)
  const [boundingBox, setBoundingBox] = useState("")

  const fieldPathPrefix = `${fieldPath}`;

  const {values} = useFormikContext();

  useEffect(() => {
    console.log("Field value changed:", values);

    if (values.custom_fields && values.custom_fields.experiments) {
      if (values.custom_fields.experiments.layer) {
        setLayerName(values.custom_fields.experiments.layer)
      } else {
        setLayerName("")
      }

      if (values.custom_fields.experiments.has_wms) {
        setHasWms(true)
      } else {
        setHasWms(false)
      }

      if (values.custom_fields.experiments.has_wfs) {
        setHasWfs(true)
      } else {
        setHasWfs(false)
      }

      if (values.custom_fields.experiments.bounds) {
        setBoundingBox(values.custom_fields.experiments.bounds)
      } else {
        setBoundingBox("")
      }
    }
  }, [values]);

  return (
    <>
      <Input
        fieldPath={`${fieldPathPrefix}.layer`}
        label={layer.label}
        placeholder={layer.placeholder}
        description={layer.description}
      ></Input>
      <BooleanCheckbox
        fieldPath={`${fieldPathPrefix}.has_wms`}
        label={has_wms.label}
        description={has_wms.description}
      ></BooleanCheckbox>
      {layerName && hasWms && (
        <Grid>
          <GridColumn>
            <Map layerName={layerName} boundingBox={boundingBox}></Map>
          </GridColumn>
        </Grid>
      )}
      <BooleanCheckbox
        fieldPath={`${fieldPathPrefix}.has_wfs`}
        label={has_wfs.label}
        description={has_wfs.description}
      ></BooleanCheckbox>
      {layerName && hasWfs && (
        <Grid>
          <GridColumn>
            WFS Table Here (eventually)
          </GridColumn>
        </Grid>
      )}
      <Input
        fieldPath={`${fieldPathPrefix}.bounds`}
        label={bounds.label}
        placeholder={bounds.placeholder}
        description={bounds.description}
      ></Input>
    </>
  );
};