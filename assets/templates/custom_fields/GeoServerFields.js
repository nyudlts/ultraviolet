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
    serverUrl
  } = props;

  const [layerName, setLayerName] = useState("")
  const [hasWms, setHasWms] = useState(false)
  const [hasWfs, setHasWfs] = useState(false)
  const [boundingBox, setBoundingBox] = useState("")

  const {values} = useFormikContext();

  // Listen to Formik field changes on custom fields
  // And convert them into local state
  useEffect(() => {
    let customFields = values.custom_fields;

    if (customFields && customFields.geoserver) {
      let geoServerFields = customFields.geoserver;

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
            fieldPath={`${fieldPath}.layer`}
            label={layer.label}
            placeholder={layer.placeholder}
            description={layer.description}
          ></Input>
          <Input
            fieldPath={`${fieldPath}.bounds`}
            label={bounds.label}
            placeholder={bounds.placeholder}
            description={bounds.description}
          ></Input>
          <BooleanCheckbox
            fieldPath={`${fieldPath}.has_wms`}
            label={has_wms.label}
            description={has_wms.description}
            trueLabel="Yes"
            falseLabel="No"
          ></BooleanCheckbox>
          {layerName && hasWms && (
            <Segment basic>
              <WmsCheck layerName={layerName} boundingBox={boundingBox} serverUrl={serverUrl}/>
            </Segment>
          )}
          <BooleanCheckbox
            fieldPath={`${fieldPath}.has_wfs`}
            label={has_wfs.label}
            description={has_wfs.description}
            trueLabel="Yes"
            falseLabel="No"
          ></BooleanCheckbox>
          {layerName && hasWfs && (
            <Segment basic>
              <WfsCheck layerName={layerName} serverUrl={serverUrl}/>
            </Segment>
          )}
        </GridColumn>
      </GridRow>
    </Grid>
  );
};
