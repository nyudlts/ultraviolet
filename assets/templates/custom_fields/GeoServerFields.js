import React, {useEffect, useState} from "react";

import {BooleanCheckbox, Input} from "react-invenio-forms";
import {Grid, GridColumn, GridRow, Segment} from 'semantic-ui-react'
import {useFormikContext} from 'formik';
import 'leaflet/dist/leaflet.css';

import {WmsCheck} from './WmsCheck'
import {WfsCheck} from "./WfsCheck";

export const GeoServerFields = props => {
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
    let custom_fields = values.custom_fields;

    if (custom_fields && custom_fields.geoserver) {
      let geoServerFields = custom_fields.geoserver;

      geoServerFields.layer ? setLayerName(geoServerFields.layer) : setLayerName("")
      geoServerFields.bounds ? setBoundingBox(geoServerFields.bounds) : setBoundingBox("")

      setHasWms(!!geoServerFields.has_wms)
      setHasWfs(!!geoServerFields.has_wfs)
    }
  }, [values]);

  return (
    <Grid>
      <GridRow>
        <GridColumn>
          <Input
            fieldPath={`${fieldPathPrefix}.layer`}
            label={layer.label}
            placeholder={layer.placeholder}
            description={layer.description}
          ></Input>
          <Input
            fieldPath={`${fieldPathPrefix}.bounds`}
            label={bounds.label}
            placeholder={bounds.placeholder}
            description={bounds.description}
          ></Input>
          <BooleanCheckbox
            fieldPath={`${fieldPathPrefix}.has_wms`}
            label={has_wms.label}
            description={has_wms.description}
          ></BooleanCheckbox>
          {layerName && hasWms && (
            <Segment basic>
              <WmsCheck layerName={layerName} boundingBox={boundingBox}></WmsCheck>
            </Segment>
          )}
          <BooleanCheckbox
            fieldPath={`${fieldPathPrefix}.has_wfs`}
            label={has_wfs.label}
            description={has_wfs.description}
          ></BooleanCheckbox>
          {layerName && hasWfs && (
            <Segment basic>
              <WfsCheck layerName={layerName}/>
            </Segment>
          )}
        </GridColumn>
      </GridRow>
    </Grid>
  );
};
