import React, {Component} from "react";

import {Input, BooleanCheckbox} from "react-invenio-forms";

const newExperiment = {
  layer: "",
  has_wms: false,
  has_wfs: false,
  bounds: "",
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
      </>
    );
  }
}