import React, {Component} from "react";

import {Input} from "react-invenio-forms";

const newExperiment = {
  layer: "",
  bounds: "",
};

export class Experiments extends Component {
  render() {
    const {
      fieldPath, // injected by the custom field loader via the `field` config property
      layer,
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