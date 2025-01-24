import React, {Component, useEffect, useRef} from "react";

import {BooleanCheckbox, Input} from "react-invenio-forms";
import {Grid, GridColumn} from 'semantic-ui-react'
import L from 'leaflet';

import 'leaflet/dist/leaflet.css';

const Map = ({center = [0, 0], zoom = 1}) => {
  const mapRef = useRef(null);

  useEffect(() => {
    const map = L.map(mapRef.current).setView(center, zoom);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{retina}.png', {
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://carto.com/attributions">Carto</a>',
      maxZoom: 18,
      worldCopyJump: true,
      retina: "@2x",
    }).addTo(map);

    return () => map.remove();
  }, [center, zoom]);

  return (
    <div ref={mapRef} id="map" style={{height: '440px', width: '100%'}}/>
  );
};

export class Experiments extends Component {
  render() {
    const {
      fieldPath, // injected by the custom field loader via the `field` config property
      layer,
      has_wms,
      has_wfs,
      bounds,
    } = this.props;

    const fieldPathPrefix = `${fieldPath}`;

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
        <BooleanCheckbox
          fieldPath={`${fieldPathPrefix}.has_wfs`}
          label={has_wfs.label}
          description={has_wfs.description}
        ></BooleanCheckbox>
        <Input
          fieldPath={`${fieldPathPrefix}.bounds`}
          label={bounds.label}
          placeholder={bounds.placeholder}
          description={bounds.description}
        ></Input>
        <Grid>
          <GridColumn>
            <Map></Map>
          </GridColumn>
        </Grid>
      </>
    );
  }
}