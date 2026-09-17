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
    wms_layer,
    wfs_layer,
    bounds,
    publicServerUrl,
    restrictedServerUrl
  } = props;

  const [wmsLayerName, setWmsLayerName] = useState("")
  const [wfsLayerName, setWfsLayerName] = useState("")
  const [boundingBox, setBoundingBox] = useState("")

  const [serverUrl, setServerUrl] = useState("")
  const [fieldHint, setFieldHint] = useState("")

  const {values} = useFormikContext();

  // Listen to Formik field changes on custom fields
  // And convert them into local state
  useEffect(() => {
    let customFields = values.custom_fields;
    
    if (values.access.files === "public" && values.access.record === "public") {
      setServerUrl(publicServerUrl)
    } else {
      setServerUrl(restrictedServerUrl)
    }

    if (customFields && customFields.geoserver) {
      let geoServerFields = customFields.geoserver;

      geoServerFields.wms_layer ? setWmsLayerName(geoServerFields.wms_layer) : setWmsLayerName("")
      geoServerFields.wfs_layer ? setWfsLayerName(geoServerFields.wfs_layer) : setWfsLayerName("")
      geoServerFields.bounds ? setBoundingBox(geoServerFields.bounds) : setBoundingBox("")

    }
  }, [values]);

  useEffect(() => {
    if (serverUrl === restrictedServerUrl) {
      setFieldHint(`Restricted files records use ${restrictedServerUrl} as the base URL for WMS and WFS requests.`)
    } else {
      setFieldHint(`Public files records use ${publicServerUrl} as the base URL for WMS and WFS requests.`)
    }
  }, [serverUrl])

  return (
    <Grid>
      <GridRow>
        <GridColumn>
          <Input
            fieldPath={`${fieldPath}.wms_layer`}
            label={wms_layer.label}
            placeholder={wms_layer.placeholder}
            description={wms_layer.description}
          ></Input>
          {wmsLayerName && (
            <Segment basic>
              <WmsCheck layerName={wmsLayerName} boundingBox={boundingBox} serverUrl={serverUrl}/>
            </Segment>
          )}
          <Input
            fieldPath={`${fieldPath}.bounds`}
            label={bounds.label}
            placeholder={bounds.placeholder}
            description={bounds.description}
          ></Input>
          <Input
            fieldPath={`${fieldPath}.wfs_layer`}
            label={wfs_layer.label}
            placeholder={wfs_layer.placeholder}
            description={wfs_layer.description}
          ></Input>
          {wfsLayerName && (
            <Segment basic>
              <WfsCheck layerName={wfsLayerName} serverUrl={serverUrl}/>
            </Segment>
          )}
        </GridColumn>
      </GridRow>
    </Grid>
  );
};