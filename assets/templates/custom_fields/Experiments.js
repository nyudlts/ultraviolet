import React, {Component} from "react";

import {Input} from "react-invenio-forms";

const newExperiment = {
  title: "",
  program: "",
};

export class Experiments extends Component {
  render() {
    const {
      fieldPath, // injected by the custom field loader via the `field` config property
      title,
      program,
    } = this.props;

    const fieldPathPrefix = `${fieldPath}`;

    return (
      <>
        <Input
          fieldPath={`${fieldPathPrefix}.title`}
          label={title.label}
          placeholder={title.placeholder}
          description={title.description}
        ></Input>
        <Input
          fieldPath={`${fieldPathPrefix}.program`}
          label={program.label}
          placeholder={program.placeholder}
          description={program.description}
        ></Input>
      </>
    );
  }
}