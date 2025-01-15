import React, {Component} from "react";

import {Input, Array} from "react-invenio-forms";
import {Grid, Form, Button, Icon} from "semantic-ui-react";

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
      icon,
      addButtonLabel,
      description,
      label,
    } = this.props;

    const fieldPathPrefix = `${fieldPath}`;

    return (
      <Grid>
        <Grid.Column width="7">
          <Input
            fieldPath={`${fieldPathPrefix}.title`}
            label={title.label}
            placeholder={title.placeholder}
            description={title.description}
          ></Input>
        </Grid.Column>
        <Grid.Column width="8">
          <Input
            fieldPath={`${fieldPathPrefix}.program`}
            label={program.label}
            icon={"building"}
            placeholder={program.placeholder}
            description={program.description}
          ></Input>
        </Grid.Column>
      </Grid>
    );
  }
}