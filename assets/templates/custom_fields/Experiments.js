import React, {useEffect, useState} from "react";

import {BooleanCheckbox, Input} from "react-invenio-forms";
import {Grid, GridColumn} from 'semantic-ui-react'
import {useFormikContext} from 'formik';
import 'leaflet/dist/leaflet.css';

import {Map} from './Map'
import {LayerAttributes} from "./LayerAttributes";

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
    let custom_fields = values.custom_fields;

    if (custom_fields && custom_fields.experiments) {
      let experiments = custom_fields.experiments;

      experiments.layer ? setLayerName(experiments.layer) : setLayerName("")
      experiments.bounds ? setBoundingBox(experiments.bounds) : setBoundingBox("")

      setHasWms(!!experiments.has_wms)
      setHasWfs(!!experiments.has_wfs)
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
            <LayerAttributes layerName={layerName}/>
          </GridColumn>
        </Grid>
      )}
    </>
  );
};